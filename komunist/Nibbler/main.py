# -*- coding: utf-8 -*-
"""
    This module parsing text from full html to special type.

    More info:
    nibbler_status:
        0: no problems (default)
        1: cant recognize encoding
        2: cant parse html
        3: not topic (other kind of pages)
        4: topic without torrent-file
        5: not topic (no topic block) with torrent-file
"""
__author__ = 'Dmitry Kryukov'

import logging
import collections
import sys
import traceback
import time

import nibbler
from komunist.tools import settings, daemonize_process, init_logging
from komunist.db.interface import NibblerDataBase


def main(db_settings, sett):
    """
        Function for starting main loop.
    :param db_settings:
    :param sett:
    :return:
    """
    # ##############
    # Initialization
    # ##############
    logger = logging.getLogger('Main')
    num_pages = sett['chew_pack'] if 'chew_pack' in sett else 200
    domain_id = sett['chew_domain'] if 'chew_domain' in sett else None
    nibbler_timeout = sett['chew_timeout'] if 'chew_timeout' in sett else 10000
    # Constant of interval before avg time logging
    avg_interval_constant_timeout = sett['chew_interval_constant_timeout'] if 'chew_interval_constant_timeout' in sett else 1000

    logger.info('Nibbler running.')

    wait_for = nibbler._wait_for()
    wait_for.next()

    logger.info('Get settings: num_pages=%s, domain_id=%s' % (num_pages, domain_id))

    db_logger = logging.getLogger('Interface')
    DB = NibblerDataBase(db_settings, db_logger)

    try:
        DB.connect()
        logger.info('Connection to database established.')
    except Exception as err:
        logger.warning('Connection to database aborted. \n %s', err)

    domains = DB.get_domains()  # get the dict of namedtuples {id : Domains(id domain specific)}
    if domains:
        logger.info('I get `%s` domains for chewing.', len(domains))

    # ##########
    # Main loop
    # ##########
    html_queue = collections.deque()  # que with pack of raw pages from sources table
    parsed_queue = collections.deque()  # que with pack chewed data

    logger.info('Starting main loop.')
    nibbler_logger = logging.getLogger('Nibbler')
    pause_counter = 0
    pause_counter_all = 0

    # Counters and vars of avg times for functions.
    avg_eat_counter = 0
    avg_eat_sum = 0
    avg_upload_counter = 0
    avg_upload_sum = 0
    avg_get_encoding_counter = 0
    avg_get_encoding_sum = 0
    while True:
        # TODO: make messages listener
        # _check_messages()
        specific = dict()
        specific['statistic'] = dict()
        specific['statistic']['rel_ver'] = 'aa'
        specific['statistic']['ranged_words'] = 'a'*132
        # default nibbler_status if all is OK
        specific['nibbler_status'] = 0
        if not html_queue:
            _time_upload = DB.save_parsed(parsed_queue)
            html_queue.extend(DB.get_html(num_pages, domain_id))
            # Saving times
            avg_upload_sum += _time_upload
            avg_upload_counter += 1

        if not html_queue:
            pause_counter_all = wait_for.send(nibbler_timeout)
            pause_counter += 1
            continue
        if pause_counter:
            logger.info('Was on IDLE in `%s` seconds', pause_counter*nibbler_timeout/1000.0)
            pause_counter = 0

        source = html_queue.popleft()  # get the namedtuple Source(id domain_id http html specific)
        specific['passed_encoding'] = source.specific['meat_hook_statistic']['_get_charset']
        html = source.html
        if 'encoding' not in source.specific:
            specific['statistic']['encoding'] = specific['passed_encoding']
            try:
                html = html.decode(specific['passed_encoding'])
            except:
                logger.warning('Can\'t decode html to passed from pudge encoding.')
                source.specific['encoding'] = None
        else:
            logger.warning('Pudge couldn\'t recognize encoding. Try to recognize itself.')
            _time_get_encoding = time.time()
            encoding = nibbler._get_encoding(source)
            _time_get_encoding = time.time() - _time_get_encoding
            logger.debug('Nibbler found encoding `%s` in %3.2f seconds', encoding, _time_get_encoding)
            # Saving times
            avg_get_encoding_sum += _time_get_encoding
            avg_get_encoding_counter += 1
            specific['statistic']['encoding'] = encoding
            specific['statistic']['time_get_encoding'] = _time_get_encoding
            try:
                html = html.decode(encoding)
                logger.debug('Encode html to `%s` successfully' % encoding)
            except:
                specific['nibbler_status'] = 1
                logger.info('Can\'t encode source, id: `%s`, encoding: `%s`. Set nibbler_status to 1', source.id, encoding)

        if not specific['nibbler_status']:
            _time_eat = time.time()
            nibbler_status, parsed = nibbler._eat(html, domains[source.domain_id].specific['Nibbler'], nibbler_logger)
            _time_eat = time.time() - _time_eat
            logger.debug('Parsed source.id `%s` in %3.2f seconds with status: `%s`.', source.id, _time_eat, nibbler_status)
            # Saving times
            avg_eat_sum += _time_eat
            avg_eat_counter += 1
            specific['statistic']['time_eat'] = _time_eat
            specific['nibbler_status'] = nibbler_status
        else:
            parsed = dict()
            logger.info('Nibbler found nibbler_status 1. Save parsed without decode and pasring.')

        parsed_queue.append((source, parsed, specific))

        if avg_upload_counter == avg_interval_constant_timeout:
            logger.info('Average time for uploading into database: `%3.2f` seconds.', float(avg_upload_sum/avg_interval_constant_timeout))
            avg_upload_counter = 0
            avg_upload_sum = 0
        if avg_get_encoding_counter == avg_interval_constant_timeout:
            logger.info('Average time for detecting encoding: `%3.2f` seconds.', float(avg_get_encoding_sum/avg_interval_constant_timeout))
            avg_get_encoding_counter = 0
            avg_get_encoding_sum = 0
        if avg_eat_counter == avg_interval_constant_timeout:
            logger.info('Average time for eating one source: `%3.2f` seconds.', float(avg_eat_sum/avg_interval_constant_timeout))
            avg_eat_counter = 0
            avg_eat_sum = 0
    # ##########
    # Finishing
    # ##########
    logger.info('Initialization of exit.')
    DB.disconnect()
    logger.info('Disconnected from database')
    logger.info('Bye')
    return avg_eat_sum, avg_upload_sum, avg_get_encoding_sum


def run():
    """
        Run function read settings and prepares nibbler.

        Reading settings, checking daemonization, creating loggers,
        starting main().
    """
    # ###############
    # Initialization
    # ###############
    sett = settings()
    db_settings = sett.getgroupdictlower('database')
    sett = sett.getgroupdictlower('Nibbler')

    # ###############
    # Daemonization
    # ###############
    return_code = None
    if sett['chew_daemonize']:
        print 'Nibbler quietly works as bookworm Daemon. See ya in logs!'
        return_code = daemonize_process('nibbler.pid')

    # ###############
    # Logging config
    # ###############
    init_logging('nibbler.log', level='DEBUG')

    logger = logging.getLogger('Run')

    # ########################
    # Log about daemon if so
    # ########################
    if return_code is not None:
        logger.info('Nibbler run as Daemon!')

    # #########
    # Database
    # #########
    _time_nibbler = time.time()
    avg_upload_sum, avg_get_encoding_sum, avg_eat_sum = (0, 0, 0)
    try:
        avg_eat_sum, avg_upload_sum, avg_get_encoding_sum = main(db_settings, sett)
    except:
        trb_type = sys.exc_info()[0]
        trb = traceback.format_exc(sys.exc_info()[2])
        logger.fatal('Exception: %s\n%s' % (trb_type, trb))
        raise
    finally:
        _time_nibbler = time.time() - _time_nibbler
        avg_interval_constant_timeout = sett['chew_interval_constant_timeout'] if 'chew_interval_constant_timeout' in sett else 1000
        logger.info('#######################################')
        if avg_upload_sum:
            logger.info('Average time for uploading into database: `%3.2f` seconds.', float(avg_upload_sum/avg_interval_constant_timeout))
        if avg_get_encoding_sum:
            logger.info('Average time for detecting encoding: `%3.2f` seconds.', float(avg_get_encoding_sum/avg_interval_constant_timeout))
        if avg_eat_sum:
            logger.info('Average time for eating one source: `%3.2f` seconds.', float(avg_eat_sum/avg_interval_constant_timeout))
        logger.info('Nibbler works: `%3.2f` seconds.', _time_nibbler)
        logger.info('Nibbler going for rest. Bye.')


if __name__ == '__main__':
    run()

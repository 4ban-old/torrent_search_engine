# coding: utf-8

import os, sys, traceback
import logging
import sqlite3

from komunist.tools import (settings, daemonize_process,
                            init_logging, pickle_bytes)
from komunist.db.interface import ActuariusDataBase


def main(db, sett):
    # Initialization
    logger = logging.getLogger('Main')
    DB = ActuariusDataBase(db)
    DB.connect()


    logger.info('Connection to database established.')

    # Main loop
    while True:
        '''
        1. Check new from Pudge.
        2. Set queue to Nibbler
        3.

        '''
        break

    # Finishing
    DB.disconnect()
    logger.info('Disconnected from database')
    logger.info('Bye')

def run(sett=None):
    # Get settings
    if sett is None:
        sett = settings()
    db = sett.getgroupdictlower('databse')
    sett = sett.getgroupdictlower('Actuarius')

    # Daemonization
    return_code = None
    if sett['actuarius_daemonize']:
        print 'Actuarius quietly works as bookworm Daemon. See ya in logs!'
        return_code = daemonize_process('actuarius.pid')

    # Logging config
    init_logging('actuarius.log')

    logger = logging.getLogger('Run')

    # Log about daemon if so
    if return_code is not None:
        logger.info('Actuarius run as Daemon!')

    # Main
    try:
        main(db, sett)
    except:
        trb_type = sys.exc_info()[0]
        trb = traceback.format_exc(sys.exc_info()[2])
        logger.fatal('Exception: %s\n%s' % (trb_type, trb))
        raise

    logger.info('Actuarius going for rest. Bye.')
    if os.path.exists('actuarius.sock'):
        os.remove('actuarius.sock')
    if os.path.exists('actuarius.pid'):
        os.remove('actuarius.pid')

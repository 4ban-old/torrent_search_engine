"""
    It is light version of urlparse, with
    suggestion that all urls in http/https scheme and it
    uses more convenient structures
    Parse_url don't pretends to be standarts-oriented library.
    At least for now.
"""

import collections

ParseUrl = collections.namedtuple('ParseUrl', 'ssl, domain, '
                                              'path, args, '
                                              'fragment',
                                  verbose=False)

def unparseurl(purl):
    if not isinstance(purl, ParseUrl):
        raise AttributeError('Argument must be parsed url')
    scheme = None if purl.ssl is None else 'https' if purl.ssl else 'http'
    res = "{scheme}://{domain}{path}{args}{fragment}"
    args='?' + '&'.join(map('='.join, purl.args)) if purl.args else ''
    fragment = '#'+purl.fragment if purl.fragment else ''
    res = res.format(scheme=scheme, domain=purl.domain,
                     path=purl.path, args=args, fragment=fragment)
    return res

def parseurl(url, no_fragments=False):
    """ Parse url string

        :param url: url string
        :return: named tuple ParseUrl
            ParseUrl.ssl = True/False/None
            ParseUrl.domain = (str) domain name (netloc)
            ParseUrl.path = (str) path on site
            ParseUrl.args = tuple of (key, value) tuples,
                sorted by keys
            ParseUrl.fragment = (str) link inside page
    """
    if not url:
        pass
        # return '', '', '/', '', None
    ssl = None
    # Fragment
    url = url.partition('#')
    domain = url[0]
    fragment = '' if no_fragments else url[2]

    # Arguments
    args = ''
    if '?' in domain:
        domain, symbol, args = domain.rpartition('?')
        args = map(lambda x: tuple(x.split('=')), args.split('&'))
    args = tuple(sorted(args, key=lambda x: x[0]))

    # url scheme
    if domain.startswith('http') and '//' in domain[5:8]:
        ssl = True if 's' == domain[4] else False
        domain = domain.partition('//')[2]
    elif '://' in domain:
        raise AttributeError('not http url: {}'.format(url))
    else:
        domain = domain.lstrip('/')

    # Path
    domain, symbol, path = domain.partition('/')
    path = '/'+path if path else '/'
    if domain:
        path = _follow('Bite my shiny metal ass', path)

    # Netloc
    # domain = domain.split('.')
    # if len(domain) < 2:
    #     domain = subdomain = ''
    # else:
    #     subdomain = '.'.join(domain[:-2])
    #     domain = '.'.join(domain[-2:])
    res = ParseUrl(ssl, domain, path, args, fragment)
    return res

def _follow(path1, path2):
    """""" 
    slash = '/' if path2.endswith('/') else ''
    if path2.startswith('/'):
        path1 = ''
    if path1.startswith('.') or '/./' in path1 or '/../' in path1:
        path1 = _follow('', path1)
    path1 = filter(lambda x: x, path1.strip('/').split('/'))
    path2 = filter(lambda x: x, path2.strip('/').split('/'))[::-1]
    while path2:
        step = path2.pop()
        if step.startswith('.'):
            if step == '.': continue
            if step == '..' and path1:
                path1.pop()
        else:
            path1.append(step)
    res = '/'.join(path1)
    res = '/'+res+slash if res else '/'
    return res


def join(base, url):
    """ Join two urls
        
        :param base:
        :param url:
        :return: ParseUrl()
    """
    if not isinstance(base, ParseUrl):
        base = parseurl(base)
    if not isinstance(url, ParseUrl):
        url = parseurl(url)
    if url.domain:
        return url
    path = _follow(base.path, url.path)
    parsed_path = parseurl(path)
    return ParseUrl(base.ssl, base.domain, parsed_path.path, parsed_path.args, parsed_path.fragment)

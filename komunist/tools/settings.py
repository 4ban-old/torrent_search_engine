from komunist.tools.structures import CaseInsensitiveGroupedDict


def settings():
    sett = dict()

    # DB
    sett[("user", "database")] = 'pavel'
    sett[("database", "database")] = 'comm'
    sett[("password", "database")] = 'pavel'
    sett[("host", "database")] = 'localhost'

    # RDB
    sett[('rhost', 'rdb')] = 'localhost'
    sett[('rport', 'rdb')] = 6378

    # Actuarius
    sett[("ACTUARIUS_DAEMONIZE", "Actuarius")] = False

    # Nibbler
    sett[("CHEW_PACK", "Nibbler")] = 50
    sett[("CHEW_DOMAIN", "Nibbler")] = None
    sett[("CHEW_DAEMONIZE", "Nibbler")] = False
    sett[("CHEW_TIMEOUT", "Nibbler")] = 10000
    sett[("CHEW_INTERVAL_CONSTANT_TIMEOUT", "Nibbler")] = 100

    return CaseInsensitiveGroupedDict(sett)
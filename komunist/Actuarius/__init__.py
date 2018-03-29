""" Bookworm Daemon

    Actuarius is a service created for:
    1. Watch the data to be actual.
        a) Check time when page was obtain
        b) Check his own statistic - how often page have updates
        c) Make decision to put this page in queue to Pudge
           or to set period of next check
    2. Make relevance order for chewed pages
    3. Carefully write logs and keep order in database

"""

from main import run
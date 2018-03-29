# -*- coding: utf-8 -*-
"""
    This launcher consist of samples of blocks for relevance test.
    Calling function relevance.relevance(blocks) where blocks is dictionary
    which consist of key 'name' and value as tuple('words', coefficient, call_position)
    Dictionary blocks is all text. Each couple of key and value is one block from all text.
    For instance:
        blocks = {'name1': ('word1 word2 word3', 0.4, True),
                'name2': ('word1 word2 word3 word4', 0.3, False)}
        block = 'name1': ('word1 word2 word3', 0.4, True)
"""

import relevance

# Simple blocks
text = {'keywords': ('I am an independent software developer developer teacher living in the city of Chicago', 3, False),
        'description': ('I primarily work on programming tools and teach courses for software developers', 2, False),
        'text': ('А это простой бесполезный текст не имеющий веса', 1, False)}
# Super simple blocks for relevance checking
test = {'keywords': ('a b c a', 1, False),
        'description': ('c a d c b', 1, True),
        'text': ('a a a', 1, True)}

e = {'keywords': ('a b c a', 1, False),
        'description': ('c a d c b', 1, False),
        'text': ('a a a', 1, False)}

t = {'keywords': ('a b c a', 0.5, False),
        'description': ('c a d c b', 0.3, False),
        'text': ('a a a', 0.2, False)}

r = {'keywords': ('a b c a', 0.3, True),
    'description': ('a c d e', 0.6, True),
    'text': ('a a a a', 0.1, True)}

bl2 = {'keywords': ('a b c a', 0.3, True),
        'description': ('a c d e', 0.6, True),
        'text': ('', 0.1, True)}

bl = {'keywords': ('a', 0.3, False),
        'description': ('e', 0.6, False),
        'text': ('', 0.1, False)}

bl3 = {}

res = relevance.relevance(bl)
print 'final weights: \n', res

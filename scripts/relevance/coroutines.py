# -*- coding: utf-8 -*-
"""
    This module calculates relevance of words in text.
"""
__author__ = 'Dmitry Kryukov'

from porter import Porter


def get_words(string):
    """
        Function splits a string into words.
    :param string: a string with text from one block, for instance, 'This is a test text'.
    :return words: function return list of lowers words, for instance, ['this', 'is', 'a', 'test', 'text']
    """
    if string:
        words = string.split(' ')
        words = filter(lambda x: x != '', words)
        words = [x.lower() for x in words]
        yield words
    yield ['']


def weights_for_block(words, call_position, coefficient):
    """
        Function calculates weight for each word in list of words (in one block).
        Coefficient is tmp argument which doesn't using in this function.
        Use two formulas depending on the flag call_position.

        If call_position = True, then the formula W=L-Position/(L*(L+1)/2.0) is used,
            where W - weight, L - length of list of words, Position - position of word in list.

        If call_position = False, then the formula W=N(word)/L is used,
            where W - weight, N(word) - frequency of word in list, L - length of list of words.

    :param words: A list of words like ['word1', 'word2', 'word3']
    :param call_position: This flag is for selecting formula for calculating weights. Might be True or False
    :param coefficient: tmp variable. Not used in this function. Looks like 0.2 or 0.4
    :return weights: Return dictionary with words and their weights and tmp arg coefficient.
            For example {'word1': 450, 'word2': 500, 'word3': 50}, 0.3
            The sum of all weights is always equals 100%  or 1. Particularly for this situation sum is equals 1000.
    """
    if words:
        porter = Porter()
        words = map(porter.get, words)
        if call_position:
            # Irregular text
            weights = dict()
            for num, word in enumerate(words):
                w = (len(words)-num)/((float(len(words))*(len(words)+1))/2.0)
                weights[word] = weights[word] + round(w, 1) if word in weights else round(w, 1)
            if weights:
                yield weights, coefficient
        else:
            # Uniform text
            weights = dict()
            for word in words:
                w = words.count(word)/float(len(words))
                weights[word] = w
            if weights:
                yield weights, coefficient
    yield {'': 1.0}, coefficient


def summary_weight(weights):
    """
        Function gets a list of dictionaries with weights for each block
            weights = [[0.2, {'word1':0.1,'word2':0.9}],
                    [0.5, {'word1':0.6,'word2':0.4}],
                    [0.3, {'word1':0.6,'word2':0.4}]]


    :param weights: list of dictionaries with weights for each block and their coefficients.
    :return result: dictionary with final weights for all words in all blocks.
    """
    result = dict()
    tmp = [len(x[1]) for x in weights]  # need only for calculate full_len
    full_len = float(sum(tmp))
    for block in weights:
        coefficient = block[0]
        if coefficient == 0:
            for key, value in block[1].iteritems():
                block[1][key] = value*(len(block[1])/full_len)
        else:
            for key, value in block[1].iteritems():
                block[1][key] = value*coefficient
    for block in weights:
        for key, value in block[1].iteritems():
            result[key] = result[key]+value if key in result else value
    yield result


def relevance(blocks):
    """
        This function calls weights_for_block() for each block of text from blocks.
        Then dictionaries with weights for each block are recorded in list with their coefficients.
            For example: list = [[0.3, {'word1',0.1, 'word2':0.4, 'word3':0.5}],
                        [0.4, {'word1',0.1, 'word2':0.9}],
                        [0.3 {'word1',1.0}]]

        Then this list passed to the function summary_weight(list) and function return
        dictionary with sum of all weights for all blocks.
            For example: result = {'word1':0.14,
                                'word2':0.36,
                                'word3':0.5}
        ~~~~~~~~~~~~~~~~~ Some examples ~~~~~~~~~~~~~~~~~~
        Typical blockS looks like:
            blocks = {'keywords': ('This is keywords', 0.2, True),
                    'description': ('This is description', 0.1, True),
                    'title': ('This is title', 0.05, False)}

        Typical block looks like:
            block = ('This is keywords', 0.2, True)

        Typical arguments for function weights_for_block() looks like:
            words = ['this', 'is', 'keywords']
            call_position = True
            coefficient = 0.2

        Typical arguments for function summary_weight() looks like:
            list = [[0.3, {'this':0.1, 'is':0.4, 'keywords':0.5}],
                    [0.4, {'this':0.3, 'is':0.3, 'description':0.6}],
                    [0.3, {'this':0.2, 'is':0.7, 'title':0.1}]]

        Typical results looks like:
            result = {'this': 0.1,
                    'is': 0.3,
                    'keywords': 0.1,
                    'description': 0.3,
                    'title': 0.2}
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :param blocks: Consist of key 'name' and value as tuple('words', coefficient, call_position)
            For instance:
                blocks = {'name1': ('word1 word2 word3', 0.4, True),
                        'name2': ('word1 word2 word3 word4', 0.3, False)}
    :return result: Return to caller result of the module.
            For instance:
                result = {'word1': 0.15,'word2' 0.15:,'word3': 0.3,'word4': 0.4}
    """
    if blocks:
        weights = list()
        for block in blocks.values():
            text = block[0]
            coefficient = block[1] if len(block) == 3 else 0
            call_position = block[-1]
            if not isinstance(text, unicode):
                text = unicode(text, 'utf-8')
            words = yield get_words(text)
            block_weights, coefficient = weights_for_block(words, call_position, coefficient)
            print block_weights
            #weights.append([block_weights[1], block_weights[0]])
        #result = yield summary_weight(weights)
        #yield result
    yield {}
# -*- coding: utf-8 -*-
import re

"""
Porter's stemmer - http://snowball.tartarus.org/
"""
__author__ = 'Dmitry Kryukov'


class Porter:
    """
        Класс, представляющий обработчик передаваемого слова
        по алгоритму Стеммера Поттера.
        Экземпляр может быть создан, как со словом, так и без него.

            p = Porter('абырвалг')
            p = Porter()
        
        Передача нового слова для обработки:

            p.set('абырвалг')
        
        После передачи слова доступно свойство root:

            p.root

        Передать слово для обработки возможно командой get:

            root = p.get('абырвалг')

        команда get вызывает set и возвращает p.root
    """


    def __init__(self, word=''):

        # Constants
        self.BASE = u' абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
        self.STOPWORDS = [u'чем', u'или', u'под', u'над', u'из-под', u'кто', u'кем', u'оно', u'его', u'эти', u'эта', u'это', u'они', u'она', u'ним', u'уже', u'ему', u'что', u'нас', u'иначе']
        self.PERFECTIVEGROUND =  re.compile(u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$")
        self.REFLEXIVE = re.compile(u"(с[яь])$")
        self.ADJECTIVE = re.compile(u"(|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$")
        self.PARTICIPLE = re.compile(u"((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$")
        self.VERB = re.compile(u"((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$")
        self.NOUN = re.compile(u"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$")
        self.RVRE = re.compile(u"^(.*?[аеиоуыэюя])(.*)$")
        self.DERIVATIONAL = re.compile(u".*[^аеиоуыэюя]+[аеиоуыэюя].*ость?$")
        self.DER = re.compile(u"ость?$")
        self.SUPERLATIVE = re.compile(u"(ейше|ейш)$")
        self.I = re.compile(u"и$")
        self.P = re.compile(u"ь$")
        self.NN = re.compile(u"нн$") 
        
        self.word = ''
        self.__group = ''
        self.set(word)

    def set(self, word):
        if word == self.word:
            return

        self.word = word
        self.__word_prepare()
        self.__group = self.__stem()


    def get(self, word):
        self.set(word)
        return self.__group

    @property
    def root(self):
        return self.__group

    def __word_prepare(self):
        """
            Предварительная обработка слова
        """
        # Приведение к типу unicode
        if not isinstance(self.word, unicode):
            try:
                self.word = unicode(str(self.word), 'utf-8')
            except Exception:
                print "Exception"
                self.word = ''

        # Проверка на основные символы
        for letter in '': #self.word:
            if letter not in self.BASE:
                self.word = ''
                break
        self.word = self.word.lower()
        if not self.word:
            return

        self.word = self.word.rstrip()
        self.word = self.word.replace('*', '')
        self.word = self.word.replace(u'ё', u'е')

        #self.wg = self.word.encode('utf-8'), self.group.encode('utf-8')
        return

    def __stem(self):
        """
            Алгоритм Стемера Поттера
            реализация чужая.

            Возвращает корень слова (group)
        """
        # TODO: изучить реализацию, доделать/переделать

        word = self.word
        #if word in self.STOPWORDS or len(word) < 3:
        #    word = ''
        if not self.word: 
            return ''
        m = re.match(self.RVRE, word)
        if m is not None and m.groups():
            pre = m.group(1)
            rv = m.group(2)
            temp = self.PERFECTIVEGROUND.sub('', rv, 1)
            if temp == rv:
                rv = self.REFLEXIVE.sub('', rv, 1)
                temp = self.ADJECTIVE.sub('', rv, 1)
                if temp != rv:
                    rv = temp
                    rv = self.PARTICIPLE.sub('', rv, 1)
                else:
                    temp = self.VERB.sub('', rv, 1)
                    if temp == rv:
                        rv = self.NOUN.sub('', rv, 1)
                    else:
                        rv = temp
            else:
                rv = temp
            
            rv = self.I.sub('', rv, 1)

            if re.match(self.DERIVATIONAL, rv):
                rv = self.DER.sub('', rv, 1)

            temp = self.P.sub('', rv, 1)
            if temp == rv:
                rv = self.SUPERLATIVE.sub('', rv, 1)
                rv = self.NN.sub(u'н', rv, 1)
            else:
                rv = temp
            word = pre+rv
        return word.encode('utf-8')

if __name__ == '__main__':

    p = Porter()
    while True:
        wrd = raw_input()
        wrd = unicode(wrd, 'utf-8')

        if wrd == '1':
            break
        else:
            print wrd, '->', p.get(wrd)

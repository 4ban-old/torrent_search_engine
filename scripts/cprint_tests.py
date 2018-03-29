# -*- coding: utf-8 -*-
import unittest
import cprint


class SimpleTestsColorizeNoPrint(unittest.TestCase):
    def test_cprint_1(self):
        raw = '[red][blue][/][yellow][/][/]'
        colorize = True
        noprint = True
        result = '\x1b[31m\x1b[34m\x1b[31m\x1b[33m\x1b[31m\x1b[0m\x1b[0m'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_2(self):
        raw = '[red]red[blue]blue[/]red[green]green[black]black[/][/]red[/]'
        colorize = True
        noprint = True
        result = '\033[31mred\033[34mblue\033[31mred\033[32mgreen\033[30mblack\033[32m\033[31mred\033[0m\033[0m'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_3(self):
        raw = '[yellow]yellow[blue]blue[green]green[/]blue[/]yellow[/]'
        colorize = True
        noprint = True
        result = '\033[33myellow\033[34mblue\033[32mgreen\033[34mblue\033[33myellow\033[0m\033[0m'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_4(self):
        raw = 'white[blue]blue[red]red[/]blue[purple][underline]purple[/][/]blue[green]green[/]blue[/]white'
        colorize = True
        noprint = True
        result = 'white\033[34mblue\033[31mred\033[34mblue\033[35m\033[4mpurple\033[4m\033[24m\033[34mblue\033[32mgreen\033[34mblue\033[0mwhite\033[0m'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_5(self):
        raw = '[red]red[blue]blue[/]red[green]green[purple]purple[/]green[/]red[/]'
        colorize = True
        noprint = True
        result = '\033[31mred\033[34mblue\033[31mred\033[32mgreen\033[35mpurple\033[32mgreen\033[31mred\033[0m\033[0m'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

class SimpleTestsNotColorizeNoPrint(unittest.TestCase):
    def test_cprint_1(self):
        raw = '[red][blue][/][yellow][/][/]'
        colorize = False
        noprint=True
        result = ''
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_2(self):
        raw = '[red]red[blue]blue[/]red[green]green[black]black[/][/]red[/]'
        colorize = False
        noprint=True
        result = 'redblueredgreenblackred'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_3(self):
        raw = '[yellow]yellow[blue]blue[green]green[/]blue[/]yellow[/]'
        colorize = False
        noprint=True
        result = 'yellowbluegreenblueyellow'
        self.assertEqual(cprint.cprint(raw, colorize=colorize, noprint=noprint), result)

    def test_cprint_4(self):
        raw = 'белый[blue]синий[red]красный[/]синий[purple][underline]фиолетовый[/][/] синий [green]зеленый[/]синий[/]дефолтный'
        noprint=True
        result = 'белыйсинийкрасныйсинийфиолетовый синий зеленыйсинийдефолтный'
        self.assertEqual(cprint.cprint(raw, noprint=noprint), result)

    def test_cprint_5(self):
        raw = '[red]красный[blue]синий[/]красный[green]зеленый[purple]фиолетовый[/]зеленый[/]красный[/]'
        noprint=True
        result = 'красныйсинийкрасныйзеленыйфиолетовыйзеленыйкрасный'
        self.assertEqual(cprint.cprint(raw, noprint=noprint), result)

if __name__ == '__main__':
    unittest.main()
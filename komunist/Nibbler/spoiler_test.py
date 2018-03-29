# coding: utf-8
__author__ = 'Dmitry Kryukov'
from komunist.Nibbler.nibbler import _eat
from pprint import pprint

html = """
<divdiv>
<div id="p-60347496" class="post_body">
<span style="font-size: 24px; line-height: normal;"><span style="text-align: center;" class="post-align"><span class="post-b"><span style="color: darkred;" class="p-color"><span style="font-family: Georgia;">Янгблад / Youngblood<h1>Header</h1></span></span></span></span></span><span style="text-align: center;" class="post-align"><span style="font-size: 18px; line-height: normal;"><span class="post-i"><span style="color: darkred;" class="p-color"><span style="font-family: Georgia;"><span class="post-b">«If you live through the gang wars, the pushers, the back-alley deathtraps... YOU GONNA BE A STAR!»</span></span></span></span></span></span><span class="post-hr"><hr class="tLeft"></span><var title="http://i3.imageban.ru/out/2013/08/03/ba4ee02cc48a959479a295787f55eecc.jpg" class="postImg postImgAligned img-right"><img height="177" width="455" alt="pic" class="postImg postImgAligned img-right" src="http://i3.imageban.ru/out/2013/08/03/ba4ee02cc48a959479a295787f55eecc.jpg" title="Click image to view full size" style="cursor: move;"></var><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Страна:</span></span> США</span><br>
    <b>text inside b</b><p>text inside p</p>
    <div class="sp-wrap">
        <div class="sp-head folded"><span>[First spoiler]</span></div>
        <div class="sp-body">[AUDIO VIDEO OTHER INFO ABOUT VIDEO OR AUDIO]</div>
    </div>
    <div class="sp-wrap">
        <div class="sp-head folded"><span>[NEXT SPOILER]</span></div>
        <div class="sp-body"><span style="text-align: center;" class="post-align"><a class="postLink" href="http://imageban.ru/show/2013/08/04/011cd7b4ea1462d5b7297caca39d000c/jpg" target="_blank"><var title="http://i6.imageban.ru/thumbs/2013.08.04/011cd7b4ea1462d5b7297caca39d000c.jpg" class="postImg">
            <span>[Text inside next spoiler]</span>
            </var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/2473d57da888547404a6dc8dc7167faf/jpg" target="_blank"><var title="http://i6.imageban.ru/thumbs/2013.08.04/2473d57da888547404a6dc8dc7167faf.jpg" class="postImg">
            </var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/184b48712e618873ed1904fdb8976431/jpg" target="_blank"><var title="http://i1.imageban.ru/thumbs/2013.08.04/184b48712e618873ed1904fdb8976431.jpg" class="postImg">
            </var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/a5ce38412452d8194d55839f80c2e837/jpg" target="_blank"><var title="http://i3.imageban.ru/thumbs/2013.08.04/a5ce38412452d8194d55839f80c2e837.jpg" class="postImg">
            </var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/cc58f8564435fa102b151bbb5758674d/jpg" target="_blank"><var title="http://i3.imageban.ru/thumbs/2013.08.04/cc58f8564435fa102b151bbb5758674d.jpg" class="postImg">
            </var></a></span>
            <div class="sp-wrap">
                <div class="sp-head folded"><span>[spoiler inside spoiler]</span></div>
                <div class="sp-body">[text of spoiler]</div>
            </div>
            <div class="sp-wrap">
                <div class="sp-head folded"><span>[another spoiler inside spoiler]</span></div>
                <div class="sp-body">[another text inside spoiler]</div>
            </div>
        </div>
    </div>
    <b>other text inside b</b>
    <div> usual text <span>text inside span</span></div>
    <div class="sp-wrap">
                <div class="sp-head folded"><span>[sp]</span></div>
                <div class="sp-body">[t]</div>
            </div>
<fieldset class="attach"><legend>Download</legend><h1 class="attach_link"><a style="color: brown;" class="dl-stub" href="http://dl.rutracker.org/forum/dl.php?t=4502880&amp;guest=1">Скачать .torrent файл</a></h1><p class="attach_comment med" id="guest-dl-tip">Для раздач более 500MB необходима регистрация<br><a href="viewtopic.php?t=101298" target="_blank"><b>Как скачивать</b></a>&nbsp; · &nbsp;<a href="viewtopic.php?t=495342" target="_blank"><b>Что такое torrent (торрент)</b></a><br></p><p class="bold tCenter mrg_8">Сайт не распространяет и не хранит электронные версии произведений, а лишь предоставляет доступ к создаваемому пользователями каталогу ссылок на <a href="http://ru.wikipedia.org/wiki/BitTorrent#.D0.A4.D0.B0.D0.B9.D0.BB_.D0.BC.D0.B5.D1.82.D0.B0.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85">торрент-файлы</a>, которые содержат только списки хеш-сумм</p></fieldset>
</div></divdiv>
<td class="nav w100 pad_2 brand-bg-white"><span class="brand-bg-white">&nbsp;<a href="./index.php">Список форумов rutracker.org</a><em>»</em>&nbsp;<a href="./viewforum.php?f=7">Зарубежное кино</a><em>»</em>&nbsp;<a href="./viewforum.php?f=187">Классика зарубежного кино</a></span></td>
"""

specific = {u'rules':
                {u'b': [{u'name': u'span', u'class': u'post-b'}, {u'name': u'b'}],
                 u'h2': [{u'name': u'h2'}], u'h3': [{u'name': u'h3'}],
                 u'h1': [{u'name': u'h1'}, {u'name': u'span', u'class': u'post-align'}],
                 u'h4': [{u'name': u'h4'}],
                 u'i': [{u'name': u'fieldset', u'class': u'attach'}],
                 u'sp': [{u'name': u'div', u'class': u'sp-wrap'}]},
            u'category': {u'1': [187],
                          u'0': [0],
                          u'3': [0],
                          u'2': [0],
                          u'5': [0],
                          u'4': [0]},
            u'xpath_to_source': u'(//div[@class="post_body"])[1]',
            u'xpath_to_torrent': u'(//div[@class="post_body"])[1]/fieldset/legend',
            u'xpath_to_category': u'//span[@class="brand-bg-white"]/a[last()]/@href'}

nibbler_statut, parsed = _eat(html, specific, None)

pprint(parsed['text'])


# coding: utf-8
__author__ = 'Dmitry Kryukov'

from komunist.Nibbler.nibbler import _eat

html = """
<html><head>

<meta charset="windows-1251">
<meta content="RuTracker.org » Классика зарубежного кино » Скачать торрент Янгблад / Youngblood (Ноэль Ноззек / Noel Nosseck) [1978, США, Криминал, драма, TVRip] DVO (НТВ+)" name="description"><title>Янгблад / Youngblood (Ноэль Ноззек / Noel Nosseck) [1978, США, Криминал, драма, TVRip] DVO (НТВ+) :: RuTracker.org</title>

<link type="image/x-icon" href="http://static.rutracker.org/favicon.ico" rel="shortcut icon">
<link href="http://static.rutracker.org/opensearch.xml" title="Поиск на RuTracker.org" type="application/opensearchdescription+xml" rel="search">

<script>
window.BB = {};
window.encURL = encodeURIComponent;
</script>
<link rel="stylesheet" href="http://static.rutracker.org/templates/v1/min/150316666473f90eca25a60c20c5ff04.all.min.css">
<script src="http://static.rutracker.org/templates/v1/min/f72d5f1374505cb46b94ed3e6ec262a7.all.min.js"></script>


<script>
BB.local_link_reg = new RegExp('^http:\/\/'+ window.location.hostname +'\/', 'i');

BB.postImg_MaxWidth = screen.width - 220;
BB.postImgAligned_MaxWidth = Math.round(screen.width/3);

BB.banned_img_hosts_reg = /tinypic|imagebanana|imagevenue|imageshack|hidebehind|ipicture|centrkino|interfoto|youpic\.ru|flashrelease/i;  //
BB.trusted_img_hosts = [
	'10pix.ru',
	'amazon.com',
	'creativecommons.org',
	'directupload.net',
	'fastpic.ru',
	'firepic.org',
	'flickr.com',
	'funkyimg.com',
	'google.com',
	'hostingkartinok.com',
	'iceimg.com',
	'ii4.ru',
	'imagebam.com',
	'imageban.ru',
	'imageshack.us',
	'imageshost.ru',
	'imdb.com',
	'imgbox.com',
	'kinoafisha.ru',
	'kinopoisk.ru',
	'lostpic.net',
	'photobucket.com',
	'photoshare.ru',
	'postimage.org',
	'radikal.ru',
	'rutracker.org',
	'savepic.ru',
	'savepic.su',
	'share.te.ua',
	'speedtest.net',
	'torrent.proxylife.org',
	'ubstat.ru',
	'uploads.ru',
	'userbars.ru',
	'vfl.ru',
	'yandex.ru',
	'torrents.loc'
].join('|').replace(/\./g, '\\.');
BB.trusted_img_hosts_reg = new RegExp('^http:\/\/([^/]+\\.)?('+ BB.trusted_img_hosts +')\/', 'i');

function initPost (context)
{
	var $context = $(context);
	$('span.post-hr', $context).html('&lt;hr class="tLeft"&gt;');
	initQuotes($context);
	initPostImages($context);
	initSpoilers($context);
	initLinks($context);
}
function initQuotes ($context)
{
	if ( $context.hasClass('signature') ) {
		return;
	}
	$('div.q', $context).each(function(){
		var $q = $(this);
		var quoted_pid;
		if ( quoted_pid = $q.children('u.q-post:first').text() ) {
			var on_this_page = $('#post_'+quoted_pid).length;
			var href = (on_this_page) ? '#'+ quoted_pid : './viewtopic.php?p='+ quoted_pid +'#'+ quoted_pid;
			$q.siblings('div.q-head').append(
				' &lt;a href="'+ href +'" title="Перейти к цитируемому сообщению"&gt;&lt;img src="http://static.rutracker.org/templates/v1/images/icon_latest_reply.gif" class="icon2" alt=""&gt;&lt;/a&gt;'
			);
		}
	});
}
function initPostImages ($context)
{
			var $in_spoilers = $('div.sp-body var.postImg', $context);
		$('var.postImg', $context).not($in_spoilers).each(function(){
		var $v = $(this);
		var $img = buildPostImg($v);
		var maxW = ($v.hasClass('postImgAligned')) ? BB.postImgAligned_MaxWidth : BB.postImg_MaxWidth;
		$img.bind('click', function(){ return imgFit(this, maxW); });
		if (user.opt_js.i_aft_l) {
			$('#preload').append($img);
			var loading_icon = '&lt;a href="'+ $img[0].src +'" target="_blank"&gt;&lt;img src="http://static.rutracker.org/templates/v1/images/loading_3.gif" alt=""&gt;&lt;/a&gt;';
			$v.html(loading_icon);
			$img.one('load', function(){
				imgFit(this, maxW);
				$v.empty().append(this);
			});
		}
		else {
			$img.one('load', function(){ imgFit(this, maxW) });
			$v.empty().append($img);
		}
		var wrap_data = $img.data('wrap');
		if (wrap_data) {
			$img.wrap('&lt;a href="'+ wrap_data.href +'" target="_blank" title="'+ wrap_data.title +'"&gt;&lt;/a&gt;');
		}
	});
}
function initSpoilers ($context)
{
	if ( $context.hasClass('signature') ) {
		return;
	}
	$context.off('.spoiler');  // prevent double binding
	$context.on('click.spoiler', 'div.sp-head', function(e){
		var $sp_head = $(this);
		var $sp_body = $sp_head.next('div.sp-body');
		if (!$sp_body.hasClass('inited')) {
			initPostImages($sp_body);
			var $sp_fold_btn = $('&lt;div class="sp-fold clickable"&gt;[свернуть]&lt;/div&gt;').click(function(){
				$.scrollTo($sp_head, { duration:200, axis:'y', offset:-200 });
				$sp_head.click().animate({opacity: 0.1}, 500).animate({opacity: 1}, 700);
			});
			$sp_body.prepend('&lt;div class="clear"&gt;&lt;/div&gt;').append('&lt;div class="clear"&gt;&lt;/div&gt;').append($sp_fold_btn).addClass('inited');
		}
		// клик с Shift открывает/закрывает все спойлеры
		if (e.shiftKey) {
			$sp_head.css('user-select', 'none');
			e.stopPropagation();
			e.shiftKey = false;
			var fold = $sp_head.hasClass('unfolded');
			$('div.sp-head', $($sp_body.parents('td')[0])).filter(function(){
				return $(this).hasClass('unfolded') ? fold : !fold;
			}).click();
		}
		else {
			$sp_head.toggleClass('unfolded');
			$sp_body.slideToggle('fast');
		}
	});
}
function buildPostImg ($v)
{
	var wrap_data = null;
	var src = $v.attr('title');

	if (src.match(BB.banned_img_hosts_reg)) {
		wrap_data = { href: 'http://rutracker.org/go/2', title: 'Прочитайте правила размещения картинок!' };
		src = "http://static.rutracker.org/smiles/tr_oops.gif";
	}
	else if (typeof(window.opera) != "undefined" &amp;&amp; window.opera.version() &lt; 12.10 &amp;&amp; !src.match(BB.trusted_img_hosts_reg)) {
		wrap_data = { href: 'http://rutracker.org/go/3', title: 'Почему я вижу эту странную картинку???' };
		src = 'http://static.rutracker.org/images/misc/opera_oops_1.png';
	}
  return $('&lt;img src="'+ src +'" class="'+ $v.attr('class') +'" alt="pic"&gt;').data('wrap', wrap_data);
}
function oopsBannedPostImg ($img)
{
	var wrap_data = $img.data('wrap');
}
function initLinks ($context)
{
	var in_sig = $context.hasClass('signature');

	$('a.postLink', $context).each(function(){
		// локальная ссылка
		if (BB.local_link_reg.test(this.href)) {
			return;
		}
		var $a  = $(this);
		var url = $a.attr('href');

		// signature
		var m;
		if (in_sig) {
			build_external_link($a);
		}
		// youtube
		else if (m = url.match(/^https?:\/\/(?:www\.)?(?:youtube\.com\/|youtu\.be)(?!user)(?:.*?)(?:=|\/)([\w\-]{11})(?!\w)/i)) {
			build_video_link($a, 'YouTube', m[1]);
		}
		// vimeo
		else if (m = url.match(/^https?:\/\/vimeo\.com\/(\d+)$/i)) {
			build_video_link($a, 'Vimeo', m[1]);
		}
		// soundcloud
		else if (/^https?:\/\/soundcloud\.com\//.test(url)) {
			var $m_span = build_m_link($a);

			$a.click(function(e){
				e.preventDefault();
				if (typeof SC == 'undefined') {
					$.ajax({
						url     : "http://connect.soundcloud.com/sdk.js", dataType : "script", cache : true, global : false,
						success : function() { sc_embed($m_span, url) }
					});
				}
				else {
					sc_embed($m_span, url);
				}
			});
		}
		// внешние ссылки в новом окне
		else {
			build_external_link($a);
		}
	});
}
function build_external_link ($a)
{
	$a.attr({ target: '_blank' });
}
function build_m_link ($a)
{
	var $icon = $('&lt;a class="m-icon" target="_blank" title="Открыть в новой вкладке"&gt;&lt;/a&gt;').attr('href', $a.attr('href'));
	if ( $a.has('var.postImg').length ) {
		$icon.addClass('m-icon-over-img');
	}
	else {
		$icon.css('display', 'inline-block');
	}
	return $a.wrap('&lt;span class="m-link"&gt;&lt;/span&gt;').before($icon).parent();
}
function build_video_link ($a, provider, video_id) {
	build_m_link($a);
	$a.click(function(e){
		e.preventDefault();
		$a.modal({ mode: 'video', provider: provider, video_id: video_id });
	});
	if (/^http/.test( $a.html() )) {
		$a.html(provider +': '+ video_id);
	}
}
function sc_embed ($m_span, sc_url)
{
	var $player_div = $('&lt;div style="clear: both; margin: 8px 0 2px;"&gt;&lt;i class="loading-1"&gt;&lt;/i&gt;&lt;/div&gt;');
	$m_span.after($player_div).remove();
	SC.oEmbed(sc_url, {auto_play: false}, $player_div[0]);
}
$(function(){
	$('div.post_body, div.signature').each(function(){ initPost(this) });
});
</script>

<script>
/**
 * Wrapper for HTML5 WebStorage
 *
 * BB.localStorage.set('foo', {bar:[1,2]});
 * BB.sessionStorage.get('foo');
 * BB.localStorage.rm('foo');
 */
$.each(['localStorage', 'sessionStorage'], function(i,type){
	BB[type] = {
		supported: !!window[type],
		get: function(key){
			if (!this.supported) {
				return null;
			}
			var val_str  = window[type].getItem(key);
			var val_orig = JSON.parse(val_str);
			return val_orig;
		},
		set: function(key, value){
			if (this.supported) {
				try {
					var val_str = JSON.stringify(value);
					window[type].setItem(key, val_str);
				} catch(e) {}
			}
		},
		rm: function(key){
			if (this.supported) {
				window[type].removeItem(key);
			}
		}
	};
});

</script>

<script>
var BB_ROOT       = "./";
var cookieDomain  = ".rutracker.org";
var cookiePath    = "/forum/";
var cookieSecure  = 0;
var LOGGED_IN     = 0;
var InfoWinParams = 'width=780,height=510,resizable=yes';

var user = {
	opt_js: {},

	set: function(opt, val, days, reload) {
		this.opt_js[opt] = val;
		setCookie('opt_js', $.toJSON(this.opt_js), days);
		if (reload) {
			window.location.reload();
		}
	}
}


$(function(){
	$('a.dl-stub').each(function(){
		var $a = $(this);
		var href = $a.attr('href');
		var t_id = href.slice( href.lastIndexOf('=')+1 );
		$a.on('mousedown', function(){
			setCookie('bb_dl', t_id, 'SESSION');
		});
		$a.click(function(){
			$('#dl-form').attr('action', href);
			$('#dl-form').submit();
			return false;
		});
	});
			$("div.jumpbox").html('\
		&lt;span id="jumpbox-container"&gt; \
		&lt;select id="jumpbox"&gt; \
			&lt;option id="jumpbox-title" value="-1"&gt;&amp;nbsp;&amp;raquo;&amp;raquo; Выберите форум для перехода &amp;nbsp;&lt;/option&gt; \
		&lt;/select&gt; \
		&lt;/span&gt; \
		&lt;input id="jumpbox-submit" type="button" value="Перейти"&gt; \
	');
	$('#jumpbox-container').one('click', function(){
		$('#jumpbox-title').html('&amp;nbsp;&amp;nbsp; Загружается... &amp;nbsp;');
		var jumpbox_src = './../html/ajax/' + (0 ? 'jumpbox_user.html' : 'jumpbox_guest.html');
		$(this).load(jumpbox_src);
		$('#jumpbox-submit').click(function(){ window.location.href='./viewforum.php?f='+$('#jumpbox').val(); });
	});
	});

var ajax = new Ajax("http://rutracker.org/forum/ajax.php", 'POST', 'json');

function getElText (e)
{
	var t = '';
	if (e.textContent !== undefined) {
		t = e.textContent;
	}
	else if (e.innerText !== undefined) {
		t = e.innerText;
	}
	else {
		t = jQuery(e).text();
	}
	return t;
}
function escHTML (txt) {
	return txt.replace(/&lt;/g, '&amp;lt;');
}
function cfm (txt)
{
	return window.confirm(txt);
}
function bb_alert (txt, is_error)
{
//alert(txt);
	txt = txt +'';
	var html = txt.replace(/\n/g, '&lt;br&gt;');
	$('#bb-alert-msg').html(html);
	$('#bb-alert-box').toggleClass('bb-alert-err', is_error == true).modal();
	return false;
}
function post2url (url, params) {
	params = params || {};
	params['form_token'] = '';
	var f = document.createElement('form');
	f.setAttribute('action', url);
	f.setAttribute('method', 'post');
	f.setAttribute('target', params['target'] || '_self');
	for (var k in params) {
		var h = document.createElement('input');
		h.setAttribute('type', 'hidden');
		h.setAttribute('name', k);
		h.setAttribute('value', params[k]);
		f.appendChild(h);
	}
	document.body.appendChild(f);
	f.submit();
	return false;
}
</script>

<style>
.hidden, .menu-sub, #ajax-loading, #ajax-error, var.ajax-params, #modal-blocker, .q-post { display: none; }
#adriver-240x120 { width: 240px; height: 120px; padding-bottom: 2px; margin-right: -2px; }
#adriver-468x60, #pr-468x60  { width: 468px; height: 60px; }
#dd-900x90 { width: 900px; }
@media screen and (max-width: 1100px) {
	#dd-900x90, #dd-900x90 &gt; object { width: 620px; }
}
#latest_news table { width: 100%; }
#nav-natz img { width: 24px; height: 15px; vertical-align: text-bottom; }
#sidebar1_wrap { margin-top: -4px; }/* temp */



/* temp end */
</style>

<noscript>
	&lt;style&gt;
	.sp-body { display: block; }  /* for search bots */
	&lt;/style&gt;
</noscript>

</head>



<body class="">



<!--cse-->
<script>
BB.hl_quick_search_err = function(){
	$('#search-text').addClass('hl-err-block').focus();
};

$(function(){
	$('#cse-search-btn, #cse-search-btn-top').click(function(){
		var text_match_input_id = $(this).attr('href');
		var text_match = $('#'+text_match_input_id).val();
		if (text_match == '') {
			$('#'+text_match_input_id).addClass('hl-err-block').focus();
			return false;
		}
		$('#cse-text-match').val( text_match );
		$('#cse-submit-btn').click();
		return false;
	});

	$('#search-text').on('mousedown keypress', function(){
		if ( $(this).hasClass('hl-err-block') ) {
			$(this).removeClass('hl-err-block');
		}
	});

	$('#search-menu').on('change', function(){
		$('#quick-search').submit();
	});

	$('#quick-search').submit(function(){
		var $search_form = $(this);
		var search_type  = $('#search-menu').val();
		var search_data  = $('#search-menu option:selected').data();
		var search_query = $.trim( $('#search-text').val() );
		var url_params   = [];

		if (search_query == '' &amp;&amp; search_type != 'search-tr') {
			BB.hl_quick_search_err();
			return false;
		}
		var search_query_enc = encURL(search_query);

		switch (search_type)
		{
			case 'search-tr':
			case 'search-all':
				var search_action = search_data.action;
				if (search_data.forum_id != null) {
					url_params.push( 'f='+ search_data.forum_id );
				}
				if (search_query_enc != '') {
					url_params.push( 'nm='+ search_query_enc );
				}
				if (url_params.length) {
					search_action += '?'+ url_params.join('&amp;');
				}
				$search_form.attr({ action: search_action });
				break;

			case 'cse':
				$('#cse-search-btn-top').click();
				return false;
				break;

			case 'wiki':
				var wiki_url = 'http://wiki.rutracker.org/'+ encURL('Служебная:Search') +'?fulltext=1&amp;search='+ search_query_enc;
				post2url(wiki_url, {target: '_blank'});
				return false;
				break;

			case 'hash':
				if ( /^[a-fA-F0-9]{40}$/.test(search_query) ) {
					window.location.href = 'viewtopic.php?h='+ search_query;
				}
				else {
					BB.hl_quick_search_err();
				}
				return false;
				break;
		}
		$('#quick-search input[type="submit"]').prop({disabled: true}).css({color: '#585858'});
	});
});
</script>
<div style="display: none;" id="cse-form-holder">
<form id="cse-search-box" action="search_cse.php">
	<input type="hidden" value="014434608714260776013:ggcq1kovlga" name="cx">
	<input type="hidden" value="FORID:9" name="cof">
	<input type="hidden" value="windows-1251" name="ie">
	<input type="text" id="cse-text-match" value="" size="60" name="q">
	<input type="submit" id="cse-submit-btn" value="Поиск в Google" name="sa">
</form>
</div>
<!--/cse-->

<form style="display: none;" id="dl-form" action="#" method="post">
	<input type="hidden" name="dummy"><!-- for IE11 http://goo.gl/CA8ci0 -->
</form>


<div style="position: absolute; overflow: hidden; top: 0; left: 0; height: 1px; width: 1px;" id="preload"></div>

<div id="body_container">

<!--************************************************************************-->
<!--=COMMON_HEADER==========================================================-->

<script>
if (top != self) {
	BB.allowed_translator_hosts = /^(translate\.googleusercontent\.com)$/;
	if (!self.location.hostname.match(BB.allowed_translator_hosts)) {
		$(function(){
			$('body').html('&lt;center&gt;&lt;h1&gt;&lt;br&gt;&lt;br&gt;Похоже вас пытаются обмануть&lt;br&gt;frame\'s hostname: '+ self.location.hostname +'&lt;/h1&gt;&lt;/center&gt;');
		});
	}
}
// var clickaider_cid = "2b0f2b47-11885";
// var clickaider_track_links = "marked";

BB.begun_iframe_domain = '195.82.146.52';
BB.begun_blocks_cnt    = 0;

function begun_init_block (params)
{
	// один блок на страницу
	if (BB.begun_blocks_cnt &gt; 0) {
		return;
	}
	var iframe_file = 'iframe-begun-user-str-3.html';
	// приведение location к адресу доступному гостям (начальная страница топика)
	var loc = (params.location_href != null) ? params.location_href : '';
	if (loc.indexOf('&amp;') != -1) {
		loc = loc.substring(0, loc.indexOf('&amp;'));
	}
	var append_char = (loc.indexOf('?') == -1) ? '?' : '&amp;';
	var fix = (params.fix_style != null) ? params.fix_style : '';
	var begun_query = [
		'bid='+ params.begun_block_id,
		'bgc='+ params.bg_color,
		'ref='+ encodeURIComponent(document.referrer),
		'loc='+ encodeURIComponent(loc + append_char +'query='),
		'fix='+ encodeURIComponent(fix),
		'rnd='+ Math.random()
	];
	var frame_width  = params.frame_width  || '100%';
	var frame_height = params.frame_height || 17;
	$(function(){
		$('#'+params.container_id).html('&lt;iframe src="http://'+ BB.begun_iframe_domain +'/'+ iframe_file +'?'+ begun_query.join('&amp;') +'" frameborder=0 width="'+ frame_width +'" height="'+ frame_height +'" marginwidth=0 marginheight=0 scrolling=no&gt;&lt;/iframe&gt;');
	});
	BB.begun_blocks_cnt++;
}

$(function(){
	var rnd = Math.round(Math.random()*1000000000);
	var ref = document.referrer ? escape(document.referrer) : 'unknown';
	$('#adriver-240x120').html('&lt;iframe width=240 height=120 src="http://ad.adriver.ru/cgi-bin/erle.cgi?sid=85725&amp;sz=topic240&amp;target=blank&amp;bt=8&amp;pz=0&amp;tail256='+ ref +'&amp;rnd='+ rnd +'" frameborder=0 marginwidth=0 marginheight=0 scrolling=no&gt;&lt;/iframe&gt;');
	$('#adriver-468x60').html('&lt;iframe width=468 height=60 src="http://ad.adriver.ru/cgi-bin/erle.cgi?sid=85725&amp;sz=topic468&amp;target=blank&amp;bt=1&amp;pz=0&amp;tail256='+ ref +'&amp;rnd='+ rnd +'" frameborder=0 marginwidth=0 marginheight=0 scrolling=no&gt;&lt;/iframe&gt;');
	//$('#dd-900x90').embedSWF(900, 90, {'http://ad.ddestiny.ru/b/900x90_tera_crepost.swf' : 'http://ddestiny.ru/c/pgMJ/'});
});


</script>

<!--page_container-->
<div id="page_container">


<!--page_header-->
<div id="page_header">

<div style="background: #FFF227; padding: 8px 0 10px; text-align: center; font-size: 14px; display: none;" id="old-browser-warn">
	<b>Вы используете устаревший браузер. Сайт может отображаться некорректно.</b>
</div>
<script>
if ( (typeof(window.opera) != "undefined" &amp;&amp; window.opera.version() &lt; 12) || (window.attachEvent &amp;&amp; !window.addEventListener) /* IE &lt; 9 */ ) {
	document.getElementById('old-browser-warn').style.display = '';
}
</script>

<!--main_nav-->
<div style="height: 17px;" id="main-nav">
	<table class="w100">
	<tbody><tr>
		<td class="nowrap">
			<div>
				<a href="./index.php"><b>Главная</b></a>·
				<a href="tracker.php"><b>Трекер</b></a>·
				<a href="search.php"><b>Поиск</b></a>·
				<a href="viewtopic.php?t=1045"><b>Правила</b></a>·
				<a target="_blank" href="http://wiki.rutracker.org/"><b>FAQ</b></a>·
				<a href="groupcp.php"><b>Группы</b></a>·
				<a onclick="window.open(this.href, '', InfoWinParams); return false;" href="info.php?show=copyright_holders"><b>Для правообладателей</b></a>
			</div>
		</td>
		<td class="nowrap tRight" id="nav-natz">
			<div>
				<a href="http://kz.rutracker.org/forum/"><img src="http://static.rutracker.org/flags/89.gif" title="Казахстанский раздел" alt="KZ"></a>
				<a href="http://ua.rutracker.org/forum/"><img src="http://static.rutracker.org/flags/180.gif" title="Украинский раздел" alt="UA"></a>
				<a href="http://by.rutracker.org/forum/"><img src="http://static.rutracker.org/flags/17.gif" title="Белорусский раздел" alt="BY"></a>
			</div>
		</td>
	</tr>
	</tbody></table>
</div>
<!--/main-nav-->

<!--logo-->
<div id="logo">
	<table class="w100">
	<tbody><tr>
		<td style="padding: 5px 0 3px 6px;">
			<a class="site-logo-link" href="./index.php">
								<img alt="logo" src="http://195.82.146.52/logo/logo.gif" class="site-logo">
							</a>
		</td>
		<td style="padding: 0 4px;" class="tCenter w100">



		<div style="width: 728px; padding: 4px 0 0;" class="tCenter bCenter"><iframe height="90" frameborder="0" width="728" scrolling="no" marginheight="0" marginwidth="0" src="http://ad.ddestiny.ru/bb/rutracker_top?rnd=1402792651" class="ccbjapreunknxlzyygpt"></iframe></div>



		</td>
	</tr>
	</tbody></table>
</div>
<!--/logo-->

<!--topmenu-->
<div class="topmenu">
<table class="w100">
<tbody><tr>

		<td class="tCenter pad_2">
		<div>
			<a href="profile.php?mode=register"><b>Регистрация</b></a>
			&nbsp;·&nbsp;
			<form action="http://login.rutracker.org/forum/login.php" method="post">
						Имя: <input type="text" accesskey="l" tabindex="1" size="12" name="login_username">
			Пароль: <input type="password" tabindex="2" size="12" name="login_password">
			<input type="submit" tabindex="3" value="Вход" name="login">
			</form>
			&nbsp;·&nbsp;
			<a href="profile.php?mode=sendpassword">Забыли имя или пароль?</a>
		</div>
	</td>

	</tr>
</tbody></table>
</div><!--/topmenu-->


<!--breadcrumb-->
<!--<div id="breadcrumb"></div>-->
<!--/breadcrumb-->


</div>
<!--/page_header-->
<!--bnt-->




<!--page_content-->
<div id="page_content">
<table style="width: 100%; border: none;"><tbody><tr>


<!--main_content-->
<td id="main_content">
<div id="main_content_wrap">


<!--========================================================================-->
<!--************************************************************************-->



<!-- page_header.tpl END -->
<!-- module_xx.tpl START -->





<table class="w100">
<tbody><tr>
	<td class="w100 vBottom pad_2">
		<h1 class="maintitle"><a href="http://rutracker.org/forum/viewtopic.php?t=4502880" id="topic-title">Янгблад / Youngblood (Ноэль Ноззек / Noel Nosseck) [1978, США, Криминал, драма, TVRip] DVO (НТВ+)</a></h1>
		<p style="margin: 12px 4px 8px;" class="small"><b>Страницы: &nbsp;1</b></p>

		<table class="w100">
		<tbody><tr>
			<td class="pad_2"><a href="http://post.rutracker.org/forum/posting.php?mode=reply&amp;t=4502880"><img alt="Ответить" src="http://static.rutracker.org/templates/v1/images/reply.gif"></a></td>
			<td class="nav w100 pad_2 brand-bg-white">
				<span class="brand-bg-white">
					&nbsp;<a href="./index.php">Список форумов rutracker.org</a>
										<em>»</em>&nbsp;<a href="./viewforum.php?f=7">Зарубежное кино</a>					<em>»</em>&nbsp;<a href="./viewforum.php?f=187">Классика зарубежного кино</a>
				</span>
			</td>
		</tr>
		</tbody></table>

	</td>
	<td class="pad_2">
		<div id="adriver-240x120"><iframe height="120" frameborder="0" width="240" scrolling="no" marginheight="0" marginwidth="0" src="http://ad.adriver.ru/cgi-bin/erle.cgi?sid=85725&amp;sz=topic240&amp;target=blank&amp;bt=8&amp;pz=0&amp;tail256=http%3A//rutracker.org/forum/viewforum.php%3Ff%3D187&amp;rnd=711915804" class="ccbjapreunknxlzyygpt"></iframe></div>	</td>
</tr>
</tbody></table>





<table id="topic_main" class="topic">
<tbody><tr>
	<th class="thHead td1">Автор</th>
	<th class="thHead td2">
				Сообщение
			</th>
</tr>


</tbody><tbody class="row1" id="post_60347496">
<tr>
	<td class="poster_info td1"><a id="60347496"></a>
	<p class="nick">Lenape</p>

<br>
	</td>
	<td rowspan="2" class="message td2">


<div id="p-20862-1" class="post_wrap">
<div id="p-60347496" class="post_body">
	<span style="font-size: 24px; line-height: normal;"><span style="text-align: center;" class="post-align"><span class="post-b"><span style="color: darkred;" class="p-color"><span style="font-family: Georgia;">Янгблад / Youngblood</span></span></span></span></span><span style="text-align: center;" class="post-align"><span style="font-size: 18px; line-height: normal;"><span class="post-i"><span style="color: darkred;" class="p-color"><span style="font-family: Georgia;"><span class="post-b">«If you live through the gang wars, the pushers, the back-alley deathtraps... YOU GONNA BE A STAR!»</span></span></span></span></span></span><span class="post-hr"><hr class="tLeft"></span><var title="http://i3.imageban.ru/out/2013/08/03/ba4ee02cc48a959479a295787f55eecc.jpg" class="postImg postImgAligned img-right"><img height="177" width="455" alt="pic" class="postImg postImgAligned img-right" src="http://i3.imageban.ru/out/2013/08/03/ba4ee02cc48a959479a295787f55eecc.jpg" title="Click image to view full size" style="cursor: move;"></var><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Страна:</span></span> США</span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Жанр:</span></span> Криминал, драма</span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Год выпуска:</span></span> 1978</span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Продолжительность:</span></span> 01:23:00</span><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Перевод:</span></span> Профессиональный (двухголосый закадровый) <span class="post-b"><span style="color: darkred;" class="p-color"><span class="post-b">[НТВ+]</span></span></span></span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Cубтитры:</span></span> нет</span><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Режиссер:</span></span> Ноэль Ноззек / Noel Nosseck</span><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">В ролях:</span></span> Лоуренс Хилтон-Джакобс, Брайан О’Делл, Рен Вудс, Тони Аллен, Винс Кэннон, Арт Эванс, Джефф Холлис, Дэвид Пендлтон, Рон Трайс, Шила Уиллс</span><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Описание:</span></span> Криминальная драма о нелёгкой жизни подростка среди сплошных разборок афро-американских молодёжных банд.</span><span class="post-hr"><hr class="tLeft"></span><a class="postLink" href="http://multi-up.com/890794" target="_blank"><span class="post-b">Sample</span></a> | <a class="postLink" href="http://www.imdb.com/title/tt0181907/" target="_blank"><span class="post-b">IMDB</span></a> | <a class="postLink" href="http://www.kinopoisk.ru/film/93116/" target="_blank"><span class="post-b">КиноПоиск</span></a><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Тип релиза:</span></span> <span style="color: darkgreen;" class="p-color"><span class="post-b">TVRip</span></span> <span style="color: gray;" class="p-color">[исх. <a class="postLink" href="http://rutracker.org/forum/viewtopic.php?t=4502557"><span class="post-b"><span class="post-u">TVRip</span></span></a> спасибо <a class="postLink" href="http://rutracker.org/forum/profile.php?mode=viewprofile&amp;u=15385175"><span class="post-b"><span class="post-u">Valeronius</span></span></a>]</span></span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Формат видео:</span></span> <span style="color: darkgreen;" class="p-color"><span class="post-b">AVI</span></span></span><span class="post-hr"><hr class="tLeft"></span><span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Видео:</span></span> 720x528 (1.36:1), 25 fps, XviD build 50, 2320 kbps avg, 0.24 bit/pixel</span><br>
<span style="font-family: Georgia;"><span class="post-b"><span style="color: darkred;" class="p-color">Аудио:</span></span> 48 kHz, AC3 Dolby Digital, 2/0 (L,R) ch, 192.00 kbps avg <span style="color: darkgreen;" class="p-color"><span class="post-b">[Russian_DVO]</span></span></span><span class="post-hr"><hr class="tLeft"></span><span style="text-align: left;" class="post-align"><span style="color: darkblue;" class="p-color"><span class="post-u"><span class="post-b">Релиз группы:</span></span></span></span><span style="text-align: left;" class="post-align"><a class="postLink" href="http://rutracker.org/forum/viewtopic.php?t=1677970"><var title="http://static.rutracker.org/ranks/all_films_logo3.gif" class="postImg"><img alt="pic" class="postImg" src="http://static.rutracker.org/ranks/all_films_logo3.gif"></var></a></span><span class="post-hr"><hr class="tLeft"></span>
<div class="sp-wrap">
<div class="sp-head folded"><span>Сравнение скриншотов</span></div>
<div class="sp-body"><a class="postLink" href="http://rutracker.org/forum/viewtopic.php?t=4502920">http://rutracker.org/forum/viewtopic.php?t=4502920</a><br>
<a class="postLink" href="http://screenshotcomparison.com/comparison/34998/picture:0" target="_blank">http://screenshotcomparison.com/comparison/34998/picture:0</a><br>
<span style="font-family: Georgia;"><span style="color: #006699;" class="p-color"><span class="post-b">Перевод одинаковый</span></span></span></div>
</div>
<div class="sp-wrap">
<div class="sp-head folded"><span>MediaInfo</span></div>
<div class="sp-body"><span style="font-family: Georgia;">eneral<br>
Complete name : E:\Мои раздачи\Youngblood_TVRip_RG_All_Films.avi<br>
Format : AVI<br>
Format/Info : Audio Video Interleave<br>
File size : 1.46 GiB<br>
Duration : 1h 23mn<br>
Overall bit rate : 2 522 Kbps<br>
Writing application : VirtualDubMod 1.6.0.0 SURROUND (build 2560/release)<br>
Writing library : VirtualDubMod build 2560/release<span class="post-br"><br></span>Video<br>
ID : 0<br>
Format : MPEG-4 Visual<br>
Format profile : Advanced Simple@L5<br>
Format settings, BVOP : Yes<br>
Format settings, QPel : No<br>
Format settings, GMC : No warppoints<br>
Format settings, Matrix : Custom<br>
Codec ID : XVID<br>
Codec ID/Hint : XviD<br>
Duration : 1h 23mn<br>
Bit rate : 2 321 Kbps<br>
Width : 720 pixels<br>
Height : 528 pixels<br>
Display aspect ratio : 4:3<br>
Frame rate : 25.000 fps<br>
Color space : YUV<br>
Chroma subsampling : 4:2:0<br>
Bit depth : 8 bits<br>
Scan type : Progressive<br>
Compression mode : Lossy<br>
Bits/(Pixel*Frame) : 0.244<br>
Stream size : 1.35 GiB (92%)<br>
Writing library : XviD 1.2.1 (UTC 2008-12-04)<span class="post-br"><br></span>Audio<br>
ID : 1<br>
Format : AC-3<br>
Format/Info : Audio Coding 3<br>
Mode extension : CM (complete main)<br>
Codec ID : 2000<br>
Duration : 1h 23mn<br>
Bit rate mode : Constant<br>
Bit rate : 192 Kbps<br>
Channel(s) : 2 channels<br>
Channel positions : Front: L R<br>
Sampling rate : 48.0 KHz<br>
Bit depth : 16 bits<br>
Compression mode : Lossy<br>
Stream size : 114 MiB (8%)<br>
Alignment : Split accross interleaves<br>
Interleave, duration : 40 ms (1.00 video frame)<br>
Interleave, preload duration : 500 ms</span></div>
</div>
<div class="sp-wrap">
<div class="sp-head folded"><span>Скриншоты</span></div>
<div class="sp-body"><span style="text-align: center;" class="post-align"><a class="postLink" href="http://imageban.ru/show/2013/08/04/011cd7b4ea1462d5b7297caca39d000c/jpg" target="_blank"><var title="http://i6.imageban.ru/thumbs/2013.08.04/011cd7b4ea1462d5b7297caca39d000c.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/2473d57da888547404a6dc8dc7167faf/jpg" target="_blank"><var title="http://i6.imageban.ru/thumbs/2013.08.04/2473d57da888547404a6dc8dc7167faf.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/184b48712e618873ed1904fdb8976431/jpg" target="_blank"><var title="http://i1.imageban.ru/thumbs/2013.08.04/184b48712e618873ed1904fdb8976431.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/a5ce38412452d8194d55839f80c2e837/jpg" target="_blank"><var title="http://i3.imageban.ru/thumbs/2013.08.04/a5ce38412452d8194d55839f80c2e837.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/cc58f8564435fa102b151bbb5758674d/jpg" target="_blank"><var title="http://i3.imageban.ru/thumbs/2013.08.04/cc58f8564435fa102b151bbb5758674d.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/a091272c809b1febfdbfc1b2ad694581/jpg" target="_blank"><var title="http://i1.imageban.ru/thumbs/2013.08.04/a091272c809b1febfdbfc1b2ad694581.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/b4974e19480c3d690b092757e1fafa88/jpg" target="_blank"><var title="http://i2.imageban.ru/thumbs/2013.08.04/b4974e19480c3d690b092757e1fafa88.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/d8d1cad2d519282582c1df196332f4d4/jpg" target="_blank"><var title="http://i3.imageban.ru/thumbs/2013.08.04/d8d1cad2d519282582c1df196332f4d4.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/fd9c13f71aeecf3853f92eaf53615b16/jpg" target="_blank"><var title="http://i2.imageban.ru/thumbs/2013.08.04/fd9c13f71aeecf3853f92eaf53615b16.jpg" class="postImg">
</var></a><a class="postLink" href="http://imageban.ru/show/2013/08/04/6e8af57a1280015911c5c899d1066e8e/jpg" target="_blank"><var title="http://i6.imageban.ru/thumbs/2013.08.04/6e8af57a1280015911c5c899d1066e8e.jpg" class="postImg">
</var></a></span></div>
</div>
		<div class="clear"></div>
		<div class="spacer_8"></div>
		<fieldset class="attach">
		<legend>Download</legend>
						<h1 class="attach_link"><a style="color: brown;" class="dl-stub" href="http://dl.rutracker.org/forum/dl.php?t=4502880&amp;guest=1">Скачать .torrent файл</a></h1>
						<p class="attach_comment med" id="guest-dl-tip">Для раздач более 500MB необходима регистрация<br>
				<a href="viewtopic.php?t=101298" target="_blank"><b>Как скачивать</b></a>&nbsp; · &nbsp;<a href="viewtopic.php?t=495342" target="_blank"><b>Что такое torrent (торрент)</b></a><br>
			</p>
			<p class="bold tCenter mrg_8">Сайт не распространяет и не хранит электронные версии произведений, а лишь предоставляет доступ к создаваемому пользователями каталогу ссылок на <a href="http://ru.wikipedia.org/wiki/BitTorrent#.D0.A4.D0.B0.D0.B9.D0.BB_.D0.BC.D0.B5.D1.82.D0.B0.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85">торрент-файлы</a>, которые содержат только списки хеш-сумм</p>
		</fieldset>

				<div style="margin: 12px auto 15px;" id="dd-900x90"></div>

			</div><!--/post_body-->
</div><!--/post_wrap-->


	</td>
</tr>
<tr>
	<td class="poster_btn td3">

			&nbsp;

	</td>
</tr>
</tbody>
<tbody class="row2" id="post_67798200">
<tr>
	<td class="poster_info td1"><a id="67798200"></a>
	<p class="nick">Ремарк77</p>

<br>
	</td>
	<td rowspan="2" class="message td2">


<div id="p-20862-2" class="post_wrap">
<div id="p-67798200" class="post_body">
	большое спасибо	</div><!--/post_body-->
</div><!--/post_wrap-->


	</td>
</tr>
<tr>
	<td class="poster_btn td3">

			&nbsp;

	</td>
</tr>
</tbody>


</table><!--/topic_main-->

<script>
$('#guest-dl-tip').prepend('Для раздач более 500MB необходима регистрация&lt;br&gt;');
</script>
<script>$('img.smile').remove();</script>








	</div><!--/main_content_wrap-->
	</td><!--/main_content-->

	</tr></tbody></table>
	</div>
	<!--/page_content-->

	<!--page_footer-->
	<div id="page_footer">

<div style="margin: 12px;" id="bn-bot-wrap">


	<div style="margin: 6px 10px; padding: 8px; border: 1px solid #B7C0C5;">
					<table style="margin: 6px auto;"><tbody><tr>
				<td></td>
							</tr></tbody></table>
				<div style="width: 98%; margin: 6px auto 0; text-align: center;" id="mg-informers"><iframe height="160" frameborder="0" width="100%" scrolling="no" marginheight="0" marginwidth="0" hspace="0" vspace="0" src="http://mg.dt00.net/public/informers/torrents.2ru.html?rnd=884304" class="ccbjapreunknxlzyygpt"></iframe></div>
<script type="text/javascript">
$(function(){
	$('#mg-informers').html('&lt;iframe src="http://mg.dt00.net/public/informers/torrents.2ru.html?rnd='+ Math.round(Math.random()*1000000) +'" frameborder=0 vspace=0 hspace=0 width="100%" height=160 marginwidth=0 marginheight=0 scrolling=no&gt;&lt;/iframe&gt;');
});
</script>	</div>

</div><!--/bn-bot-wrap-->


<div class="clear"></div>

<div style="margin: 12px 6px 6px 6px;" class="med bold tCenter">
	<a onclick="window.open(this.href, '', InfoWinParams); return false;" href="info.php?show=user_agreement">Условия использования</a>
	&nbsp;·&nbsp;
	<a onclick="window.open(this.href, '', InfoWinParams); return false;" href="info.php?show=advert">Реклама на сайте</a>
		&nbsp;·&nbsp;
	<a onclick="window.open(this.href, '', InfoWinParams); return false;" href="info.php?show=copyright_holders">Для правообладателей</a>
						&nbsp;·&nbsp;
	<a onclick="window.open(this.href, '', InfoWinParams); return false;" href="info.php?show=press">Для прессы</a>
		&nbsp;·&nbsp;
	<a target="_blank" href="viewtopic.php?t=2234744">Для провайдеров</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="http://wiki.rutracker.org">Торрентопедия</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="/go/8">Кому задать вопрос</a>
</div>
<div style="margin: 6px 6px 16px 6px;" class="med bold tCenter">
	<a target="_blank" href="http://rutracker.org/forum/viewtopic.php?t=4903496">Rutracker Online</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="http://rutracker.org/forum/viewforum.php?f=1538">Авторские раздачи</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="http://rutracker.org/forum/viewforum.php?f=1289">Конкурсы</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="http://rutracker.org/forum/viewforum.php?f=489">Новости в сети</a>
	&nbsp;·&nbsp;
<!--	<a href="http://rutracker.org/forum/viewforum.php?f=2410" target="_blank"><b style="color: #0000A0;">Олимпийский раздел</b></a>-->
<!--	&nbsp;&middot;&nbsp;-->
	<a target="_blank" href="http://rutracker.org/forum/viewforum.php?f=2332">Новости "Хранителей" и "Антикваров"</a>
	&nbsp;·&nbsp;
	<a target="_blank" href="http://rutracker.org/forum/index.php?closed=1">Закрытые раздачи</a>
	&nbsp;·&nbsp;
	<a onclick="return post2url('torrent.php', {rand_rel: 1});" href="#">Случайная раздача</a>
</div>


<div style="margin: 18px 4px 4px 4px;" class="tCenter nowrap">
	<!--LiveInternet-->
	<script>
	var LI_title = '';
	document.write("&lt;a href='http://www.liveinternet.ru/stat/rutracker.org/' "+ "target=_blank&gt;&lt;img src='http://counter.yadro.ru/hit?t16.2;r"+escape(document.referrer)+((typeof(screen)=="undefined")?"":";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+";h"+escape(LI_title.substring(0,80))+";"+Math.random()+"' alt='' "+"border='0' width='88' height='31'&gt;&lt;\/a&gt;");
	</script><a target="_blank" href="http://www.liveinternet.ru/stat/rutracker.org/"><img height="31" border="0" width="88" alt="" src="http://counter.yadro.ru/hit?t16.2;rhttp%3A//rutracker.org/forum/viewforum.php%3Ff%3D187;s1366*768*24;uhttp%3A//rutracker.org/forum/viewtopic.php%3Ft%3D4502880;h;0.4050029368926161"></a>

	<!--rambler-->
	<a target="_blank" href="http://top100.rambler.ru/cgi-bin/stats_top100.cgi?1467197"><img height="31" width="88" style="border: none;" alt="" src="http://top100-images.rambler.ru/top100/banner-88x31-rambler-gray2.gif"></a>
	<script>
	new Image().src = "http://counter.rambler.ru/top100.scn?1467197&amp;rn="+Math.random()+"&amp;rf="+escape(document.referrer);
	</script>

	<!--openstat-->
	<a target="_blank" href="http://rating.openstat.ru/site/3058772"><img height="31" width="88" style="border: none;" alt="" src="https://openstat.net/i/87.gif?tc=c3c3c3"></a>
	<img height="1" width="1" alt="" src="http://openstat.net/cnt?cid=3058772&amp;rnd=1402792651">
</div>

<table class="bCenter w99">
<tbody><tr>

	<td class="nowrap w50">
		<div class="copyright">
			<a href="groupcp.php?g=104792">Администрация</a>
			&nbsp;·&nbsp;
			<a href="groupcp.php?g=104787">Модераторы</a>
			&nbsp;·&nbsp;
			<a href="groupcp.php?g=104841">Техническая помощь</a>
			&nbsp;·&nbsp;
			<a href="groupcp.php?g=105539">Редакторы Wiki</a>
			&nbsp;·&nbsp;
			<a href="viewtopic.php?t=224697">IRC канал</a>
			&nbsp;·&nbsp;
			<a href="http://blog.rutracker.org/">Блог</a>
		</div>
	</td>
	<td class="tRight nowrap w50">
		<span class="copyright"><!--&copy; Dreamtorrent Corp. 2005-2014--></span>
		<div class="med">
					</div>
	</td>

</tr>
</tbody></table>

	</div><!--/page_footer-->
	</div><!--/page_container-->



<div id="ajax-loading"><b>Loading...</b></div>
<div id="ajax-error"><b>Error</b></div>
<style>
#bb-alert-box { width: auto; max-width: 800px; line-height: 18px; display: none; }
#bb-alert-msg { min-width: 400px; max-height: 400px; margin: 50px 20px; padding: 10px; overflow: auto; text-align: center; }
.bb-alert-err { color: #7E0000; background: #FFEEEE; box-shadow: 0 0 20px #B85353; font-weight: bold; }
</style>
<div id="bb-alert-box"><div id="bb-alert-msg"></div></div>
<div id="modal-blocker"></div>


	</div><!--/body_container-->


</body></html>
"""

specific = {u'rules':
                {u'b': [{u'name': u'span', u'class': u'post-b'}, {u'name': u'b'}],
                 u'h2': [{u'name': u'h2'}], u'h3': [{u'name': u'h3'}],
                 u'h1': [{u'name': u'h1'}, {u'name': u'span', u'class': u'post-align'}],
                 u'h4': [{u'name': u'h4'}],
                 u'i': [{u'name': u'fieldset', u'class': u'attach'}],
                 u'sp': [{u'name': u'div', u'class': u'sp-wrap'}]},
            u'category': {u'1': [187],
                          u'0': [23],
                          u'3': [18],
                          u'2': [43],
                          u'5': [445],
                          u'4': [556,565,54,43,4455,4532]},
            u'xpath_to_source': u'(//div[@class="post_body"])[1]',
            u'xpath_to_torrent': u'(//div[@class="post_body"])[1]/fieldset/legend',
            u'xpath_to_category': u'//span[@class="brand-bg-white"]/a[last()]/@href'}

nibbler_status, parsed = _eat(html, specific, None)
print '=>', nibbler_status
print '=>', parsed['category']






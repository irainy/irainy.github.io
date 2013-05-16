/* Load this script using conditional IE comments if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon\'">' + entity + '</span>' + html;
	}
	var icons = {
			'icon-twitter' : '&#xe000;',
			'icon-google-plus' : '&#xe001;',
			'icon-facebook' : '&#xe002;',
			'icon-github' : '&#xe003;',
			'icon-quill' : '&#xe004;',
			'icon-tags' : '&#xe005;',
			'icon-calendar' : '&#xe006;',
			'icon-bubble' : '&#xe007;',
			'icon-qrcode' : '&#xe008;',
			'icon-home' : '&#xe009;',
			'icon-gift' : '&#xe00a;',
			'icon-bug' : '&#xe00b;',
			'icon-evil' : '&#xe00c;',
			'icon-evil-2' : '&#xe00d;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};
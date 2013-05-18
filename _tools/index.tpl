<!doctype html>
<head>
	<meta charset="UTF-8" />
	<meta name="description" content="雨生的blog" />
	<title>it's rainy</title>
	<link rel="stylesheet" href="/ui/css/g.css" media="all" />
	<link rel="stylesheet" href="/ui/css/icon.css" media="all" />
	<link rel="shortcut icon" href="/ui/imgs/rainy.ico"/>
	<script src="/ui/js/jquery-1.9.1.min.js"></script>
	<script src="/ui/js/g.js"></script>
	<!--[if lte IE 7]><script src="lte-ie7.js"></script><![endif]-->
</head>
<body>
	<header>
		<div id="logo">
			<a href="/" alt="Home" title="Home"><div id="s">i</div><div id="niky">t's rainy</div></a>
		</div>
		<div id="menu-list">
		</div>
	</header>
	<div id="main">
		<ul id="articles">
			{% for article in articles %}
			<li>
				<div class="article-time" datetime="{{ article.datetime }}">
					<span>{{ article.date }}</span>
					<span>{{ article.time }}</span>
				</div>
				<div class="article-table">
					<h2><a href="{{ article.permalink }}" alt="{{ article.title }}" title="{{ article.title }}" >{{ article.title }}</a></h2>
					<div class="brief">
					<p>
						{{ article.brief }}
					</p>
					</div>
				</div>
				<div class="clr"></div>
			</li>
			{% endfor %}
		<!-- Article list, in this <li> tag
			<li>
				<div class="article-time" datetime="2013-04-15 13:15">
					<span>13 Mar 2013</span>
					<span>16:20</span>
				</div>
				<div class="article-table">
					<h2>你好！</h2>
					<div class="brief">
					<p>
						Hello, GitHub!
					</p>
					<p>
						这时第一篇！
					</p>
					</div>
				</div>
				<div class="clr"></div>
			</li>
		-->

		</ul>
	</div>
	
{% include "footer.html" %}

</body>
</html>

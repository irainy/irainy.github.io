<!doctype html>
<head>
	<meta charset="UTF-8" />
	<title>{{ title }}</title>

	<meta name="keywords" content="{{ keywords }}"/>
    <meta name="description" content="{{ title }}" />
	<link rel="stylesheet" href="/ui/css/g.css" media="all" />
	<link rel="stylesheet" href="/ui/css/desert.css" media="all" />
	<link rel="stylesheet" href="/ui/css/icon.css" media="all" />
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


<!--Article template add here-->
		<article>

			<h2>{{ title }}</h2>

			<div id="info">
			<i class="icon-calendar"></i><span>{{ date }}</span>
			<i class="icon-tags"></i><span>{{ keywords }}</span>
			<i class="icon-feather"></i><span>rainy</span>
			</div>

			{{ blogbody }}

		</article>
<!--Article template done-->
<div class='article-nav'>
	<span class='prev' ><a id='pervLink' href="{{ prevLink }}" ><i class="icon-undo"></i></a></span>
	<span class='next' ><a id='nextLink' href="{{ nextLink }}" ><i class="icon-redo"></i></a></span>
	<div class='clr' ></div>
</div>
<div class='add-comments' >
<div id="disqus_thread"></div>
    <script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'snikyblog'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    <a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
</div>
</div>
	</div>

{% include "footer.html" %}

	<a href="#">
	<i class="icon-arrow-up-3 scroll-up"></i>
	</a>
<script src="/ui/js/jquery-1.9.1.min.js"></script>
<script src="/ui/js/g.js"></script>
<script type='text/javascript' src='/ui/js/prettify.js'></script>
<script>prettyPrint();</script>  
</body>
</html>
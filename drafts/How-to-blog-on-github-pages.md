<conf style='display:none'>
title: 在Github Pages上搭建静态博客站点
cate: magic
permalink: http://sniky.github.com/magic/How-blog-on-github-pages.html
tags: git, python
author: me
</conf>

在Github Pages上搭建静态博客站点
====
{{ subInfo }}

Github Pages 提供展示静态 HTML 页面的服务，即完全自由的 blog 搭建，只需在 github 上新建一个名为username.github.com 的 Repository，就可以通过 git 上传、管理 blog 页面，可以实现“像程序员一样写作”，that's cool！

实作过程其实主要是在本地实现静态站点生成的功能，有他人写好的 Jekyll 软件提供这一功能，并深度结合 github ，可以根据网页源码生成静态页面。可惜是基于 ruby 环境，不太想用，所以干脆根据自己所需，定做 python 版本，又一次重造轮子了…

**于是几天过去了**

事实证明，重造的轮子可能不是圆形的，甚至称不上椭圆，极有可能是一个长了很只多脚的多边形。其实思路还是比较明确的，目标就是用简洁无干扰的 markdown 写 blog body，用模板引擎渲染到 html 框架中，然后更新整个站点，上传。用 python 来完成这些工作，需要一些相关的 Module，如下：

* misaka: 解析Markdown，转化为HTML;
* PyYaml: 解析yaml格式的config档;
* Jinja2: Template engine;

Blog body的部分大概就是这些了，哦，还有代码高亮显示，没有用 pygments，javascript 的 prettyprint 也是不错的选择。最后 python 的源码放在 github 博客目录下的 drafts 下，大概两百来行，还重构过一遍，简直惨不忍睹…不过勉强可以用。

然后是 markdown 以及编辑器，基本上 Mac 用 Mou，Ubuntu 用 Retex，Win 用 MarkdownPad，都试试，还是 Mac 最风骚(黑白二分，与 Jekyll 主页的风格一致，仿照它做了一个临时的 [About Me](/ext/about.html) 页)；Win 下面以一次下载 MarkdownPad2 小红伞竟然报毒 -_-!，实时预览也总是崩溃，尤其是有中文的情况，勉强还是用着第一版，不过也看到有牛人用 Rstudio [1](#footnote1)，结合了 R 语言环境，感觉不够纯，但是大一统的折腾精神可嘉！至于 markdown 的语法其实原本就没多少规则，只是对 html 的简化，适合写作，用一下就习惯了(又想起初学用 vim 时用 vim 翻译变态心理学作业的场景，用着用着就上瘾了…)。

最后是 UI 部分，也是比较费时不讨好的部分，其实原本就是做来玩的，秉承大一统的折腾精神，应该把能想得到的很 cool 的东西全部加进去，比如 node.js 、 lesscss 、bootstrap 什么的，甚至跟上移动互联网的风潮，搞搞 responsive web design ，结果发现有点太费时间了，玩不起…,最后页面上甚至连 js 代码都没有。这样一说，其实还有很多可以加上去的，tag 系统，disqus 评论，等等 等等 等等… …除了这些基础的，像是页面优化(现在的也变背景是一张几百 k 的 PNG 图片，简直说不定都加载不动…)、SEO 什么的，有空的时候可以逐一玩一遍，或者再重构一下我那个多边形的轮子，把这些能加的再加进去看看，囧rz

哦 对，还有一直不冷不热的 ifttt ，因为前段时间看到 Yahoo 的 [huginn](https://github.com/cantino/huginn)，心痒难耐，可惜又是 ruby，想顺便试一下，于是先绑定个新浪微博，时间仓促，来不及细致深入，先 mark 一下。

<br/>
----
<p id='footnote1'>1. [Markdown写作浅谈](http://www.yangzhiping.com/tech/r-markdown-knitr.html)</p>(然后又发现 misaka 不支持 footnotes…)
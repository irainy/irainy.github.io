<conf style='display:none'>
title: 在Github Pages上搭建静态博客站点
cate: magic
permalink: http://sniky.github.com/magic/How-to-blog-on-github-pages.html
tags: git, python
author: me
</conf>

在Github Pages上搭建静态博客站点
====
{{ subInfo }}

Github Pages提供展示静态HTML页面的服务，即完全自由的blog搭建，只需在github上新建一个名为username.github.com的Repository，就可以通过git上传、管理blog页面，可以实现“像程序员一样写作”，that's cool！

实作过程其实主要是在本地实现静态站点生成的功能，有他人写好的Jekyll软件提供这一功能，并深度结合github，可以根据网页源码生成静态页面。可惜是基于ruby环境，不太想用，所以干脆根据自己所需，定做python版本，又一次重造轮子:P
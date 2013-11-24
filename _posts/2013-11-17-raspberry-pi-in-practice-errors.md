---
layout: post
title: "Raspberry Pi 实作记录"
description: "整理、记录折腾 Raspberry Pi 过程中遇到的问题、错误，及其解决方案。"
tags: [Pi]
---

###1. Rasbian network interface

{% highlight sh linenos%}
sudo leafpad /etc/network/interface # vim & vi are dead...

auto eth0
iface eth0 inet static
	address 10.*.*.* #lab ip
	netmask	255.255.255.0
	gateway	10.*.*.*
{% endhighlight %}


###2. apt-get update error
 
> <span style='color:red'>W: GPG error: </span>http://mirrors.zju.edu.cn wheezy Release: 
> The following signatures couldn't be verified because the public key is not available: 
> NO\_PUBKEY 8B48AD6246925553 NO\_PUBKEY 6FB2A1C265FFB764

可能是因为开始的时候修改了`/etc/apt/source.list`：

{% highlight sh linenos%}
#deb http://mirrordirector.raspbian.org/raspbian/ wheezy main contrib non-free
deb http://mirrors.zju.edu.cn/debian/ wheezy main contrib non-free
{% endhighlight %}
同时移除了`/etc/apt/sources.list.d`。解决方案：

`su -c 'apt-get --reinstall install debian-archive-keyring'`

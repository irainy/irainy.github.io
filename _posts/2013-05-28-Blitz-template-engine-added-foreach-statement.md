---
layout: post
title: "C语言PHP扩展模板引擎Blitz加入FOREACH特性"
description: "Blitz是一个快速的PHP模板引擎，由C语言编写，通过PHP插件安装，通过改进加入了PHP常用的foreach循环语句。"
tags: [PHP, C]
category: main
keywords: PHP,C,Blitz,模板引擎,PHP插件
---

常用的PHP模板引擎（如[Smarty](http://www.smarty.net/)）大多为PHP写成，而PHP的执行效率较低；C语言开发的PHP扩展用作模板引擎效率可以得到显著提升，[Blitz](http://alexeyrybak.com/blitz/blitz_en.html)就是一个C语言开发的PHP模板引擎扩展，废话不多，先做一个简单的测试（测试代码在[这里](https://github.com/sniky/Blitz-featured/blob/master/benchmark/index.php)）:

{% highlight php linenos%}
<?php
$list = array();

$alpha = join(range('a', 'z'));
for($i=0;$i<1000;$i++){
	$nameStr = '';
	for($j=0; $j&lt;count(range(0, rand(5, 7))); $j++){
		$nameStr .= $alpha[rand(0,25)];
	}
	array_push($list, $nameStr);
}
?>
{% endhighlight %}

构建一个长为1000的简单字符串数组`$list`，字符串长5~7，然后将数组assign到模板引擎里，比较运行时间：


{% highlight php linenos%}
<?php
function blitz_render(){
	Global $list;
	$View = new Blitz('index.blz');
	$View->display(array('name'=>'Blitz', 'list'=>$list));
}
function smarty_render(){
	Global $list;
	require('/usr/lib/php/Smarty/Smarty.class.php');
	$smarty = new Smarty();
	$smarty->assign(array('name'=>'Smarty', 'list'=>$list));
	$smarty->display('index.tpl');
}
$t1 = microtime(true);
blitz_render();
$t2 = microtime(true);
smarty_render();
$t3 = microtime(true);

echo "Blitz used: ".(($t2-$t1)*1000)."ms\n";
echo "Smarty used: ".(($t3-$t2)*1000)."ms\n";
?>
{% endhighlight %}

选取几次比较结果如下：

{% highlight bash linenos%}
Blitz used: 1.6891956329346ms
Smarty used: 13.232946395874ms

Blitz used: 3.6599636077881ms
Smarty used: 18.430948257446ms
{% endhighlight %}

误差应该主要来源于虚构的数组`$list`字符串长度随机，将数组长度降为10再比较：

{% highlight bash linenos%}
Blitz used: 0.27894973754883ms
Smarty used: 11.041879653931ms

Blitz used: 0.52690505981445ms
Smarty used: 11.965036392212ms
{% endhighlight %}

结果如此，大概就不需要进行显著性检验了。


另，原本的Blitz中不支持for或者foreach循环，取而代之的是block进行遍历、迭代数组，但传入模板引擎的变量必须在PHP代码中格式化成嵌套数组的形式，这对于对于简单的数组（如上例中的一维数组）是很不方便的，将其稍加改动，在Blitz中加入foreach的属性([这里](https://github.com/sniky/Blitz-featured))。实际上Blitz(v0.8.6)设计已经相当完善，改动内容一共也只有十几行，并没有对原本结构有所改动，但是阅读6000+行C源码，理清其错综复杂的数据结构、函数调用以及神出鬼没的指针传递的确不是件容易的事。


最后，Blitz或者说C扩展确实快，其速度相当于C vs PHP，其缺点也恰恰相当于PHP vs C，无论PHP设计好与坏，开发PHP程序显然要比开发C更快速，因为它基于（集成于）C但更灵活，所以Smarty等PHP程序相较于C扩展也是类似的道理，速度'稍慢'，但灵活度更高，只在取舍。

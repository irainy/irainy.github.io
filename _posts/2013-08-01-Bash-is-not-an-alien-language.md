---
layout: post
title: "Bash不是外星语"
description: ""
tags: [Bash]
---
bash对于我来说一直都像一门外星语，因为从一开始接触到它的时候，它看起来更像是操作系统的化身而不是一门编程语言，而且事实上这样凭直觉的理解并没有什么错，因为大部分情况下用到bash的目的都是为了与操作系统进行交流。

<!--
bash script容易令人疑惑的地方除了与操作系统之间千丝万缕的关系（包括环境变量等），像`if...fi`这样拗口的语法看起来也很像外星语，还有一点比较重要的是用户容易觉得bash script其实就是一堆command line的堆砌（虽然这样认为也没错），所以只要掌握特定用途的command就ok了。这里的`用户`指的就是我自己，正因为这些原因，平日里拿到别人写好的script就直接执行，作批量测试的时候大多数情况用python，“成功”地避开一行一行研究外星语一样的bash script也照样侥幸活到现在~

当然随着时间的推移，会慢慢发现一门语言的语法虽然是其可见的最鲜明的特征，但从某种（学习的）角度来说，它却是最不要紧的因素。
-->

比较经常会用到bash script的场景除了把简单堆砌的command写进一个脚本然后丢进可执行的目录下方便使用外，大多数情况下是进行一些批量执行或测试，或者是一些自动化执行过程。以前都是用python来代替，甚至觉得`os.system(cmd)`这样的调用也能满足绝大部分需求，最近以来一是由于很多configure过程报错被逼着不得不去找出错误的原因，另一方面也是由于实在受够了python的`os.walk()`了，所以从头开始再学习一次bash这门不是外星语的外星语。

* **Intro**
Shell本身是一种用C语言编写的程序，常见的Shell种类众多，从本质上说bash并没有什么特别，但它是大多数linux系统默认的shell，即使用户不用也会有许多os后台程序在让它不停地奔跑，所以不用也是浪费。
	
* **环境变量**
bash中的变量，既可以被bash本身所应用，而更常见的是作为环境变量存在。常见遵循如下几种规则：

{% highlight bash linenos%}
var=123 # '=' 左右两侧均不可有空格，变量值为单个字串(不含空白字符)则可省略引号；
var='hello world!' NOT var="hello world!" # 双引号与单引号不同；
echo hello ${var}world! # '${VAR_NAME}'中'{}'用于消除变量名的边界歧义；
export PATH; unset PATH # export & unset 将变量输出(销毁)至环境变量；
{% endhighlight %}

其中，第2条，bash引用变量所储存的内容用到特殊符号$，$var被称为变量扩展(variable expansion)，有点像C语言中指针的含义，而在bash中双引号会保留扩展的特性，而单引号则会将特殊字符当做普通字符来看待，例如：
{% highlight bash linenos%}
var=rainy
echo 'hello $var.' # 输出 hello $var.
echo "hello $var." # 输出 hello rainy.
{% endhighlight %}

bash中另外一类变量是当执行脚本时从命令行中读取的参数(c语言中的`int argc, char* argv[]`)，`$0, $1, $2, …, $#, $@`，其中类比关系如下：
{% highlight bash linenos%}
$# ~= int argc; $@ ~= argv[]; $i ~= argv[i]; $* ~= argv[1:]
{% endhighlight %}
	
* **字符串截取**
bash中对(字符串)变量的截取是非常常见的操作，常见操作如下：
{% highlight bash linenos%}
var=abcdefghijklmnopqrstuvwxyz
echo ${var:0:3} #abc
echo ${var:0} #a-z
echo ${var:3} #d-z
echo ${var:${#var}-3} #xyz - ${#var} is the len of $var.
var=fofoofooobar
echo ${var#\*fo} # foofooobar 返回从左侧开始匹配'\*fo'最小位置之后的字符串；
echo ${var##\*fo} # oobar 返回从左侧开始匹配'\*fo'最大位置之后的字符串；
echo ${var%foo\*} # fofoo 返回从右侧开始匹配'fo\*'最小位置之前的字符串；
echo ${var%%foo\*} # fo 返回从右侧开始匹配'foo\*'最大位置之前的字符串；
{% endhighlight %}

* **流程控制**
IF:
{% highlight bash linenos%}
if [ condition ]# whitespace不能省；
then 
	action
elif [ conditin2 ]
then
	action2
	.
else actionx
fi
{% endhighlight %}
* FOR:
{% highlight bash linenos%}
for arg in $@;do
	echo $arg
done
{% endhighlight %}
* **More**
	* 还有更多细节如function定义、更详细的流程控制等，最好的学习方法是在实际应用中去操作。

	* 一些上古神器[awk](http://coolshell.cn/articles/9070.html)、[sed](http://coolshell.cn/articles/9104.html)的快速入门。


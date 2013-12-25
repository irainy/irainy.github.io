---

layout: post
title: "Lisp初学之暗礁（一）: APPLY 与 MAPCAR"
description: ""
tags: [Lisp]
category: main

---

{% highlight cl %}
(TOPIC-ABOUT ((COMP LIST CONS) (COMP APPLY MAPCAR)))
{% endhighlight %}

关于lisp的争论太多了，有人对其赞美到了无以复加的地步，也有人觉得不以为然，但是作为一个没有深入学习过的人来说，就只能做一个不明真相的围观群众。而对于那些跃跃欲试想要参与进来的初学者来说，想要入门却并非易事，一方面面对高手们扑面而来的那些玄之又玄的大道，另一方面还要面对lisp本身“奇异”的表达形式以及最致命的环环相扣的括号。因而选择一个合适的入门材料就显得更为重要[**&rarr;**](http://www.zhihu.com/question/19621539)，有人推荐[SICP](http://mitpress.mit.edu/sicp/full-text/book/book.html)等一些大部头著作，但是这些作为深入学习研究来说比较适合，如果作为熟悉语法特性等，还是直接动手开始coding比较合适，[Common Lisp Koans](https://github.com/google/lisp-koans)就是一个很好的选择，这个项目模仿Ruby Koans通过填补代码来熟悉Lisp的语法及特性。

在`mapcar-and-reduce.lsp`一节，用 apply 与 mapcar 实现转置矩阵的功能，在Lisp中函数也可以当做参数传递给其它函数使用，其中内置可以以函数作为参数的函数有：
{% highlight cl %}
> (funcall #'+ 3 4)
7
> (apply #'+ 3 4 '(3 4))
14
> (mapcar #'not '(t nil t nil t nil))
(NIL T NIL T NIL T)
{% endhighlight %}

[Funcall, Apply, and Mapcar](http://www.n-a-n-o.com/lisp/cmucl-tutorials/LISP-tutorial-20.html)

* funcall 的第一个参数为执行函数（将第一个参数称为“执行函数”），剩余参数作为该函数的参数；
* apply 与 funcall 的作用一样，只是其最后一个参数必须为list；
* mapcar 接受第一个参数作为执行函数，然后将第二个list中的每一个参数依次传递给执行函数，并将执行结果依次合并为一个list输出。

奇怪的是 apply 与 funcall 之间的区别仅仅是 apply 的参数必须是 list，那么 apply 的功能是[如何实现](http://blog.csdn.net/ryuali2010/article/details/7816559)的？

原来 apply 先对执行函数以外参数调用 list* 方法，然后再对生成的列表调用 values-list 方法，最终再将 values-list 输出的结果依次传入执行函数中。这里 (list* args) 的执行过程如下：

* 如果 args 是 list 类型，则返回 args;
* 如果 args 是单个数字，则返回 args;
* 如果 args 是多个元素（非 list 形式），则将倒数第二个元素与最后一个元素以 dot-list 的形式结合并返回整个列表。

{% highlight cl %}
> (list* '(1 2 3))
(1 2 3)
> (list* 1 2 3)
(1 2 . 3)
> (list* 1)
1
{% endhighlight %}

这里又涉及到[点状列表](https://acl.readthedocs.org/en/latest/zhCN/ch3-cn.html)（Dotted Lists）的概念：
> 调用 list 所构造的列表，这种列表精确地说称之为正规列表(properlist )。一个正规列表可以是 NIL 或是 cdr 是正规列表的 Cons 对象…一个非正规列表的 Cons 对象称之为点状列表 (dotted list)。

可以看到，list* 的作用主要在最后一个参数上，它将最后一个元素以 append 的方式连接到前面的元素所组成的列表中（这样做的意义待考？），而 values-list 执行的操作则是将参数列表中的每一个元素依次返回，但传入参数不能是dot-list，这就导致了 apply 的最后一个参数必须是 list 类型的特性（这样做的意义也待考？）。

apply 与 mapcar 的组合如何完成转置矩阵的功能呢？还要依赖于 Lisp 函数参数的参数列表（Parameter Lists）机制，
{% highlight cl %}
> ((lambda (&rest r) r) '(1 2 3))
((1 2 3))
> ((lambda (&rest r) r) 1 2 3)
(1 2 3)
{% endhighlight %}

形参中的 &rest 关键词收集所有剩余参数，并存放到一个列表里`(list r)`。将 mapcar 与上面的匿名函数相结合会得到什么样的结果呢？
{% highlight cl %}
> (mapcar (lambda (&rest r) r) '(1 2 3))
((1) (2) (3))
> (mapcar (lambda (&rest r) r) '(1 2 3) '(4 5 6))
((1 4) (2 5) (3 6))
{% endhighlight %}

上面的方法已经得到了转置的效果，mapcar 将后续列表中的元素逐一传入匿名函数，而匿名函数通过 &rest 接收多余的参数，这样就可以无限制地添加参数，而通过 mapcar 遍历每个参数列表的元素，经由匿名函数`(list r)`组装后返回，从而实现转置的效果。而 apply 的作用则是利用 list* 与 values-list 将矩阵的每一行作为输入列表依次传递给上面的过程：

{% highlight cl %}
> (apply #'mapcar (lambda (&rest r) r) '((1 2 3) (4 5 6) (7 8 9)))
((1 4 7) (2 5 8) (3 6 9))
{% endhighlight %}

**总结**

Lisp Koans 很适合学习，实际上有人整理了一个 Koans 系列：[Learn a New Programming Language Today with Koans](http://www.lauradhamilton.com/learn-a-new-programming-language-today-with-koans)，涵盖了许多编程语言。另外，关于 Lisp，有一篇[The Nature of Lisp](http://www.defmacro.org/ramblings/lisp.html)（翻译版：[Lisp的本质](http://www.csdn.net/article/2012-11-22/2812113-The-Nature-Of-Lisp)）很值得初学者拜读。

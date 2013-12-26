---
layout: post
title: "Lisp初学之（二）: 线性递归 与 线性迭代"
description: "Lisp学习，迭代与递归"
tags: [SICP; Lisp]
category: main
keywords: 迭代, 递归
---

{% highlight cl %}
(TOPIC-ABOUT (COMP 'linear-recursive-process 'linear-iterative-process))
{% endhighlight %}

在学习使用其他语言时，迭代(iterative)或者循环是流程控制中非常重要的一个环节，但是与之功能类似递归(recursive)却往往不被提及或总是一带而过，原因大多是出于机器执行效率或消耗层面的考量，在这里我们抛开这些不去考虑，单纯从计算过程的角度出发去看 Lisp 中的迭代与递归（SICP [1.2.1  Linear Recursion and Iteration](http://sniky.github.io/extra/sicp/book-Z-H-11.html#%_sec_1.2.1)），发现之前所理解的递归与迭代还是太肤浅，只是从语法形式层面判断“调用了自身”的是递归、`for/while/do`的是循环迭代，结果就触礁了。

仍然从考虑阶乘函数开始：

![](http://latex.codecogs.com/svg.latex?n%21%20%3D%20n%20%5Ccdot%20%28n%20-%201%29%20%5Ccdot%20%28n%20-%202%29%20%5Ccdot%20%5Ccdot%20%5Ccdot%203%20%5Ccdot%202%5Ccdot%201)

用语言描述阶乘的定义为：当`n=1`时，`n!=1`；否则`n!=n*(n-1)!`。很自然地，将定义转换成 Lisp 代码：

{% highlight cl linenos%}
(defun fac (n)
	(if (= n 1)
		1
		(* n (fac (- n 1)))
	)
)
{% endhighlight %}

单从语法形式上(syntactic)看上面的代码，`(fac n)`在定义时调用了它自身，这一语法形式上的事实我们称之为“递归过程(recursive procedure)”；而从实际的计算过程来看，也就是说看`(fac n)`在实际执行的过程中做了那些计算，结果是只有当调用到`(fac 1)`时才返回了明确的结果 1，在此之前，`(fac (- n 1))`只是作为展开过程中的助记符，推进程序的前进，如下图：

![](http://sniky.github.io/extra/sicp/ch1-Z-G-7.gif)

`(fac n)`产生了一个递归的计算过程(recursive process)，为了完成这一计算过程，它在形式上调用了自身，在计算过程中将自身作为推进（展开）计算的标识符，作为计算代价，我们不得不记住展开过程中所有`(fac (- n 1))`经过的地方，直到`(fac 1)`给出明确的返回值，再沿原路返回回去，得到`(fac n)`的值；又因为阶乘计算过程中，我们所要记住的`(fac (- n 1))`经过的路径与 n 的大小存在线性相关，因而称这样的计算过程为“<span class='emp'>线性递归过程(Linear Recursive Process)</span>”。

再考虑迭代的算法，所谓迭代，在计算阶乘的过程中可以看做是对 `n` 与 `(n - 1)` 的乘积在 `n = 1, 2, ..., n` 的范围内重复、累积：

{% highlight cl linenos%}
(defun fac-iter (n)
	(defun iter (i product)
		(if (> i n)
			product
			(iter (+ i 1) (* product i))
		)
	)
	(iter 1 1)
)
{% endhighlight %}

上面的程序从语法形式上来看，仍然是一个递归的过程：`(iter i product)` 内部调用了 `(iter (+ i 1) (* product i))`，但是从实际的计算过程来看，我们不需要像递归计算那样记住整个递归过程的推进路线，而是通过迭代更新每次调用时所用的参数，这样计算过程中我们需要记住的只有迭代计数变量 `i`、迭代乘积 `product`、以及 `n`；又因为阶乘计算过程中，所用的计算步骤或者所要记住的迭代变量的迭代次数与 n 的大小线性相关，因而称这样的计算过程为“<span class="emp">线性迭代过程(Linear Iterative Process)</span>”。这种用递归的过程实现的迭代的计算过程也称为<span class="emp">尾递归</span>。

**总结**

总的来说，区分线性递归与尾递归、递归与迭代要从语法描述的过程与实际的计算过程去考虑。

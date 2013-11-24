---
layout: post
title: "BP神经网络实践 - 代码识别器"
description: ""
tags: [ANN; BP; Python]
---

[神经网络介绍](http://www.ibm.com/developerworks/cn/linux/other/l-neural/index.html)一文介绍了用神经网络算法进行代码识别的方法，即:

> 假设给出 500 个字符的代码段，您知道它们是 C、C++、Java 或者 Python。现在构造一个程序，来识别编写这段代码的语言。

所用代码来自：[代码识别](http://gnosis.cx/download/neural_net_1.zip)，主要实现一个神经网络[NN](https://github.com/sniky/A-N-N/blob/master/bp_net_code_recognizer/bpnn.py)，于是从 github 上分别抓取了C、Java、Python的代码，来做一下测试，其中：

> C语言：1759个文件，Java：3333个文件，Python：1909个文件。

首先统计分析代码中20个特殊字符出现的频率，作为输入节点([统计代码见这里](https://github.com/sniky/A-N-N/blob/master/bp_net_code_recognizer/statistic.py))，并重载了test方法，输出测试准确率：

{% highlight python linenos%}
def test(self, testPat):
		cor = 0
		for p in testPat:
			output = self.update(p[0])
			output = self.mask(output)
			if p[1] == output:
				flag = "CORR"
				cor += 1
			else:
				flag = "INCORR"
			print "Output -> ", output , flag
		print "Test result: %.2f%%" % (float(cor) / len(testPat) * 100)
{% endhighlight %}

**测试结果**

通过调整`TRAIN_SIZE`、`TEST_SIZE`从[dataSet](https://github.com/sniky/A-N-N/tree/master/bp_net_code_recognizer/dataSet)下的统计结果中抽取一定数量的数据作为训练和测试：

1. `TRAIN_SIZE = 20, TEST_SIZE = 600`:

    迭代次数为8000，最终训练差误收敛至<span style="color:red">0.046145</span>，测试准确率为<span style="color:green">88.50%</span>；

2. `TRAIN_SIZE = 10, TEST_SIZE = 600`:

    最终训练差误收敛至<span style="color:red">0.016267</span>，测试准确率为<span style="color:green">85.83%</span>；

3. `TRAIN_SIZE = 50, TEST_SIZE = 600`:

    最终训练差误收敛至<span style="color:red">2.203505</span>，测试准确率为<span style="color:green">65.44%</span>；

4. `TRAIN_SIZE = 10, TEST_SIZE = 1200`:

    最终训练差误收敛至<span style="color:red">0.015848</span>，测试准确率为<span style="color:green">85.97%</span>；

**总结**

从测试结果来看，训练数量越小，误差可以收敛到越小；增加测试数量，也可以提高最终准确率。或者说所选取的特征能否作为甄别、分类的有效指标，也需要做预先的判别。

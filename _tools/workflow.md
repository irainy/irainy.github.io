怎样使用SSNP.PY
====

1. SSNP 是简化版的静态页面生成脚本，所维护的[sniky.github.io](http://sniky.github.io)主要有两类页面：index即首页、article即内容页；

2. 一般流程为：现在/_draft/目录下依据_init_blog.md新建article，主要涵盖标签为:

    * p[class="img"]
    * a
    * img
    * blockquote
    * pre class="prettyprint"
    * ul | ol > li
    * hr
    * strong
    * span
完成后到/_tools/目录下执行<pre>python ssnp.py ../_draft/blog.md</pre>

3. 具体api接口或模板约定格式见[/_tools/ssnp.py](https://github.com/sniky/sniky.github.com/blob/master/_tools/ssnp.py)注释。
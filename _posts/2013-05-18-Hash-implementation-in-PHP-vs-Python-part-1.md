---
layout: post
title: "PHP与Python实现Hash比较（一）"
description: "分析 PHP、Python 源代码，比较其 Hash 结构的实现算法及涉及到的数据结构。"
tags: [PHP; Python]
category: main
keywords: PHP,Python,源代码,Hash 结构
---

PHP中的array，python中的dict都是通过hash表(哈希表或散列表)实现的，或者说array与dict本身就是hash结构，本文及后续文章将分别比较PHP与python源代码中对哈希表的实现算法，一来学习其设计思想，另外可用于避免开发过程中一些可能会降低效率或易引发bug的操作。

先来PHP。一切源于PHP的内置数据类型zval(见[PHP_X_X/Zend/zend.h](http://lxr.php.net/xref/PHP_5_4/Zend/zend.h)):
{% highlight c linenos%}
typedef union _zvalue_value {
    long lval;                  //long value
    double dval;                //double value
    struct {
        char *val;
        int len;
    } str;
    HashTable *ht;              //hash table value
    zend_object_value obj;
} zvalue_value;
struct _zval_struct {
    //Variable information
    zvalue_value value;     //value
    zend_uint refcount_gc;
    zend_uchar type;    //active type
    zend_uchar is_ref_gc;
};
{% endhighlight %}

其中HashTable \*ht即是PHP中用于表示Array类型的结构，在深究HashTable结构之前先了解哈希表的原理，在C语言中数组是通过自然数作为数组索引来存储数据的，而在PHP或python等这些语言中，哈希表是以key - value的方式存取的，要实现这一存储方式，则需要将任意可能的key对应或映射到数组或者内存的自然数序列索引上，即实现

>index = hash(key)

hash()即为哈希函数。理想状态下的hash()可以将任意的key映射到均匀分布且不重叠的自然数集合中，但由于key的不确定性，这显然是不可能的，因而一个好的哈希函数应该可以尽可能地避免重叠或碰撞(collisions)，而在PHP中实现这一功能的哈希函数采纳的是DJBX33A算法。源码中实现代码如下：
{% highlight c linenos%}
static inline ulong zend_inline_hash_func(const char *arKey, uint nKeyLength)
{
    register ulong hash = 5381;
    /* variant with the hash unrolled eight times */
    for (; nKeyLength >= 8; nKeyLength -= 8) {
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
        hash = ((hash << 5) + hash) + *arKey++;
    }
    switch (nKeyLength) {
        case 7: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 6: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 5: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 4: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 3: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 2: hash = ((hash << 5) + hash) + *arKey++; /* fallthrough... */
        case 1: hash = ((hash << 5) + hash) + *arKey++; break;
        case 0: break;
EMPTY_SWITCH_DEFAULT_CASE()
    }
    return hash;
}
{% endhighlight %}
据其注释中所解释的来看，DJBX33A (Daniel J. Bernstein, Times 33 with Addition)算法可简单描述为

> hash(i) = hash(i-1) * 33 + str[i]

至于为何取33而不是其它数，解释说是对1 ~ 256进行分别进行测试后择优选择的结果，并没有理论上的支撑，而且初始的hash值为5381应该也没有什么特别特别的特别之处吧？到这里为止，首先可以确定的一条规则就是，<span style="color: #3498db">在PHP中定义使用数组时key的长度以最好不要超过7为妙</span>，便可省掉第一步的for循环，因而在考虑效率的前提下，道长当年所说的为了增加代码的可读性将变量名定为几十个字符甚至一句话显然是不可取的咯:P

通过巧妙的算法，hash碰撞得以减少，但是并没有完全避免(例如：[PHP哈希表碰撞攻击原理](http://blog.codinglabs.org/articles/hash-collisions-attack-on-php.html)），既然冲突是不可避免的，那就只能想办法解决冲突，算法书里面对冲突的处理方案有很多，PHP采用的是[拉链法](http://www.nowamagic.net/academy/detail/3008060g)，具体实现方法还是要先追寻其定义(见[PHP_X_X/Zend/zend_hash.h](http://lxr.php.net/xref/PHP_5_4/Zend/zend_hash.h))：
{% highlight c linenos%}
typedef struct bucket {
    ulong h;                        //Used for numeric indexing
    uint nKeyLength;
    void *pData;
    void *pDataPtr;
    struct bucket *pListNext;
    struct bucket *pListLast;
    struct bucket *pNext;
    struct bucket *pLast;
    const char *arKey;
} Bucket;
typedef struct _hashtable {
    uint nTableSize;
    uint nTableMask;
    uint nNumOfElements;
    ulong nNextFreeElement;
    Bucket *pInternalPointer;   //Used for element traversal
    Bucket *pListHead;
    Bucket *pListTail;
    Bucket **arBuckets;
    dtor_func_t pDestructor;
    zend_bool persistent;
    unsigned char nApplyCount;
    zend_bool bApplyProtection;
#if ZEND_DEBUG
    int inconsistent;
#endif
} HashTable;
{% endhighlight %}

最终hash表的key保存在Bucket.arKey，key长为Bucket.nKeyLength，哈希函数计算得到的哈希值存为Bucket.h，当冲突时通过引出一条静态链表来解决，其实现如下：
{% highlight c linenos%}
ZEND_API int zend_hash_exists(const HashTable *ht, const char *arKey, uint nKeyLength)
{
    ulong h;
    uint nIndex;
    Bucket *p;
    IS_CONSISTENT(ht);
    h = zend_inline_hash_func(arKey, nKeyLength);
    nIndex = h & ht->nTableMask;
    p = ht->arBuckets[nIndex];
    while (p != NULL) {
        if (p->arKey == arKey ||
            ((p->h == h) && (p->nKeyLength == nKeyLength) 
            && !memcmp(p->arKey, arKey, nKeyLength))) {
                return 1;
        }
        p = p->pNext;
    }
    return 0;
}
{% endhighlight %}
p = p->pNext即在已有元素之上开辟出新的位置存储冲突的下一个元素。至此，PHP中HashTable实现的基本思想就介绍完了，有空再把python的部分补上。

###构建动态结构体的小trick
Bucket结构体的最后一个元素arKey被定义为char *arKey;也有看到char arKey[1]，有人解释说利用变长结构体，加上有看到注释

> char arKey[1]; /\* Must be last element \*/

更是如坠云里雾里，还以为说arKey必须存放HashTable里面key字符串的最后一个字符…经过一番挣扎，发现原来不是这个意思，shit！(见[what-is-your-favorite-c-programming-trick](http://stackoverflow.com/questions/599365/what-is-your-favorite-c-programming-trick))，所谓的变长结构体只是说在考虑到内存连续性条件下，为了实现结构体内部元素的动态分配，利用struct的性质，将需要动态分配的变量放在结构体最后，如此以来通过malloc动态分配给struct的内存超出结构体本身所需的部分(sizeof(struct))可以顺其自然地被最后一个元素所访问，从而实现了可变长的结构体，所以说，注释中的*Must be last element*不是说存放的是key的最后一个字符，而是必须放在结构体的最后一个元素！shit again(but a good trick:P)!


**参考**

1. [PHP哈希表结构的深入剖析](http://www.nowamagic.net/academy/detail/1201011)

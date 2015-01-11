TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

一个简单而高效的短文本分类工具，基于LibLinear


示例代码
-------

```python
>> from tgrocery import Grocery
# 新开张一个杂货铺，别忘了取名！
>> grocery = Grocery('sample')
# 训练文本可以用列表传入
>> train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
>> grocery.train(train_src)
# 也可以用文件传入
>> grocery.train('train_ch.txt')
# 预测
>> grocery.predict('考生必读：新托福写作考试评分标准')
education
```

更多示例: [sample/](sample/)

安装
----

    $ pip install tgrocery 

> 目前仅在Unix系统下测试通过
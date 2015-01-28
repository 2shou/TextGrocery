TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

一个高效易用的短文本分类工具，基于[LibLinear](http://www.csie.ntu.edu.tw/~cjlin/liblinear)

TextGrocery整合了[结巴分词](https://github.com/fxsjy/jieba)作为默认的分词单元，以支持中文的短文本分类

性能
----

- 训练集：来自32个类别的4.8万条新闻标题
- 测试集：来自32个类别的1.6万条新闻标题
- 与[scikit-learn](https://github.com/scikit-learn/scikit-learn)的svm和朴素贝叶斯算法做横向对比

|         分类器            | 准确率    |  计算时间（秒）   |
|:------------------------:|:---------:|:--------------:|
|     scikit-learn(nb)     |   76.8%   |     134        |
|     scikit-learn(svm)    |   76.9%   |     121        |
|     **TextGrocery**      | **79.6%** |    **49**      |

示例代码
-------

```python
>>> from tgrocery import Grocery
# 新开张一个杂货铺，别忘了取名！
>>> grocery = Grocery('sample')
# 训练文本可以用列表传入
>>> train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
>>> grocery.train(train_src)
# 也可以用文件传入
>>> grocery.train('train_ch.txt')
# 保存模型
>>> grocery.save()
# 加载模型（名字和保存的一样）
>>> new_grocery = Grocery('sample')
>>> new_grocery.load()
# 预测
>>> new_grocery.predict('考生必读：新托福写作考试评分标准')
education
# 测试
>>> test_src = [
    ('education', '福建春季公务员考试报名18日截止 2月6日考试'),
    ('sports', '意甲首轮补赛交战记录:米兰客场8战不败国米10年连胜'),
]
>>> new_grocery.test(test_src)
# 准确率
0.5
# 同样可以用文本传入
>>> new_grocery.test('test_ch.txt')
# 自定义分词器
>>> custom_grocery = Grocery('custom', custom_tokenize=list)
```

更多示例: [sample/](sample/)

安装
----

    $ pip install tgrocery 

> 目前仅在Unix系统下测试通过
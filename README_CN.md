TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

一个简单而高效的短文本分类工具，基于LibLinear

安装依赖
-------

    $ cd tgrocery/learner 
    $ make

> 目前仅在Unix系统下测试通过

示例代码
-------

```python
>> from tgrocery import Grocery
# 新开张一个杂货铺，别忘了取名！
>> grocery = Grocery('sample')
# 训练
>> grocery.train('train_ch.txt')
# 预测
>> grocery.predict('考生必读：新托福写作考试评分标准')
education
```

更多示例: [sample/](sample/)

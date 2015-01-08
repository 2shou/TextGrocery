TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

一个傻瓜化的短文本分类工具，基于LibShortText

安装依赖
-------

    $ cd external/libshorttext
    $ python setup.py install

示例代码
-------

```python
>> from tgrocery import Grocery
>> grocery = Grocery('sample')
# Train
>> grocery.train('train_ch.txt')
# Predict
grocery.predict('考生必读：新托福写作考试评分标准')
# Test
grocery.test('test_ch.txt')
```

更多示例: [sample/](sample/)

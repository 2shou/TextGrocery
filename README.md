TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

A simple, efficient short-text classification tool based on LibLinear

Other languages: [中文文档](README_CN.md)

Prepare
-------

    $ cd tgrocery/learner 
    $ make

> Only test under Unix-based System

Sample Code
-----------

```python
>> from tgrocery import Grocery
# create a grocery(don't forget to set a name)
>> grocery = Grocery('sample')
# Train
>> grocery.train('train_ch.txt')
# Predict
>> grocery.predict('考生必读：新托福写作考试评分标准')
education
```

More examples: [sample/](sample/)

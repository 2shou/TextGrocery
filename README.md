TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

A simple short-text classification tool based on LibShortText

Prepare
-------

    $ cd external/libshorttext
    $ python setup.py install

Sample Code
-----------

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

More examples: [sample/](sample/)

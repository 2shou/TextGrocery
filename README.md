TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

A simple short-text classification tool based on LibShortText

Prepare
-------

    $ cd extern; python setup.py install

Create Grocery
--------------

```python
from tgrocery import Grocery

grocery = Grocery('sample')
```

Train
--------

```python
grocery.train('train_ch.txt')
```

Predict
-------

```python
grocery.predict('考生必读：新托福写作考试评分标准')
```

Test
----

```python
grocery.test('test_ch.txt')
```

More examples: [sample/](sample/)

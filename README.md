TextGrocery
===========

A simple short-text classification tool based on LibShortText

Prepare
-------

    $ cd extern; python setup.py install

Create Grocery
--------------

```python
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

Install
-----------

    $ python setup.py install

More examples: [sample/](sample/)

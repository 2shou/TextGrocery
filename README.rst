TextGrocery
-----------

A simple, efficient short-text classification tool based on LibLinear.

Sample Usage
````````````
.. code:: python

    >> from tgrocery import Grocery
    # Create a grocery(don't forget to set a name)
    >> grocery = Grocery('sample')
    # Train from list
    >> train_src = [
        ('education', '名师指导托福语法技巧：名词的复数形式'),
        ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
        ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
        ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
    ]
    >> grocery.train(train_src)
    # TrVain from file
    >> grocery.train('train_ch.txt')
    # Predict
    >> grocery.predict('考生必读：新托福写作考试评分标准')
    education

Installation
````````````
.. code:: bash

    $ pip install tgrocery

Links
`````

* `Code on Github <https://github.com/2shou/TextGrocery'>`_
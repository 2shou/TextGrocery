TextGrocery
-----------

A simple, efficient short-text classification tool based on LibLinear.

Sample Usage
````````````
.. code:: python

    >>> from tgrocery import Grocery
    # Create a grocery(don't forget to set a name)
    >>> grocery = Grocery('sample')
    # Train from list
    >>> train_src = [
        ('education', 'Student debt to cost Britain billions within decades'),
        ('education', 'Chinese education for TV experiment'),
        ('sports', 'Middle East and Asia boost investment in top level sports'),
        ('sports', 'Summit Series look launches HBO Canada sports doc series: Mudhar')
    ]
    >>> grocery.train(train_src)
    # Or train from file
    >>> grocery.train('train_ch.txt')
    # Save model
    >>> grocery.save()
    # Load model(the same name as previous)
    >>> new_grocery = Grocery('sample')
    >>> new_grocery.load()
    # Predict
    >>> new_grocery.predict('Abbott government spends $8 million on higher education media blitz')
    education
    # Test from list
    >>> test_src = [
        ('education', 'Abbott government spends $8 million on higher education media blitz'),
        ('sports', 'Middle East and Asia boost investment in top level sports'),
    ]
    >>> new_grocery.test(test_src)
    # Return Accuracy
    1.0
    # Or test from file
    >>> new_grocery.test('test_ch.txt')
    # Custom tokenize
    >>> custom_grocery = Grocery('custom', custom_tokenize=list)

Installation
````````````
.. code:: bash

    $ pip install tgrocery

Links
`````

* `Code on Github <https://github.com/2shou/TextGrocery>`_
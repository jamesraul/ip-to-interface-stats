$ python

>>> ip_address = '10.1.1.1'
>>> type(ip_address)
<type 'str'>
>>>

>>> a = 10
>>> b = 20
>>> type(a)
<type 'int'>
>>> c = a + b
>>> c
30
>>> type(c)
<type 'int'>

>>> print "Adding {} and {} together = {}".format(a,b,c)
Adding 10 and 20 together = 30

>>> my_list = [a,b,c]
>>> my_list
[10, 20, 30]
>>> my_list[1]
20


>>> my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
>>>
>>>
>>> my_dict
{'key3': 'value3', 'key2': 'value2', 'key1': 'value1'}
>>>
>>> my_dict['key1']
'value1'

>>> name = raw_input('What is you name?: ')
What is you name?: James
>>> name
'James'

>>> if a == 10 and c == 30:
...     print "a is 10 and c is 30"
...
a is 10 and c is 30


>>> if a == 9 and c == 30:
...     print "a is 9 and c is 30"
... elif c == 30:
...     print "only c has a match of 30"
...
only c has a match of 30




modules
>>> from os import path
>>> path.isfile('test.py')
True

>>> import time
>>> time.sleep(3)
>>>

>>> import os.path
>>> os.path.isfile('test.py')
True
>>> os.path.isfile('test.py2')
False
>>>

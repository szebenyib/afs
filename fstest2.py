Python 2.7.2 (default, Jun 12 2011, 15:08:59) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import pyuipc
>>> open(7)

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    open(7)
TypeError: coercing to Unicode: need string or buffer, int found
>>> pyuipc.open(7)
>>> toread = pyuipc.prepare_data((0x034E, "integer"), True)

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    toread = pyuipc.prepare_data((0x034E, "integer"), True)
TypeError: list is expected
>>> toread = pyuipc.prepare_data([0x034E, "integer"]), True)
SyntaxError: invalid syntax
>>> toread = pyuipc.prepare_data([0x034E, "integer"], True)

Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    toread = pyuipc.prepare_data([0x034E, "integer"], True)
TypeError: list element 0: should be a tuple of a length of at least 2
>>> toread = pyuipc.prepare_data([(0x034E, "integer"),], True)

Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    toread = pyuipc.prepare_data([(0x034E, "integer"),], True)
TypeError: list element 0: type string be of length 1
>>> toread = pyuipc.prepare_data([(0x034E, "i"),], True)

Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    toread = pyuipc.prepare_data([(0x034E, "i"),], True)
TypeError: list element 0: invalid type letter: i
>>> toread = pyuipc.prepare_data([(0x034E, "h"),], True)
>>> read(toread)

Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    read(toread)
NameError: name 'read' is not defined
>>> pyuipc.read(toread)
[8853]
>>> toread = pyuipc.prepare_data([(0x034E, "H"),], True)
>>> pyuipc.read(toread)
[8853]
>>> nav1 = pyuipc.prepare_data([(0x0350, "H"),], True)
>>> pyuipc.read(nav1)
[4144]
>>> pyuipc.read([(0x0350, "H"),], True)

Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    pyuipc.read([(0x0350, "H"),], True)
ValueError: exactly one argument is expected
>>> pyuipc.read([(0x0350, "H"),])
[4144]
>>> 

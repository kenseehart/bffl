Examples
========

Struct Definition
-----------------

.. code-block:: python

    @struct
    class eric:
        a: uint[3]
        b: uint[4]

    # Alternatively:
    eric2 = struct('eric2', [('a', uint[3]), ('b', uint[4])])

Working with Decimals
---------------------

.. code-block:: python

    money = decimal(16, 2)(123.45)
    assert money == 123.45
    assert money.n_ == 12345
    assert money + 1.0 == 124.45

Expressions
-----------

.. code-block:: python

    @struct
    class seven_type:
        a: uint[3]
        b: uint[4]

    seven = seven_type()
    ab = seven['a * b']

    seven.a = 5
    seven.b = 11

    assert seven.a == 5
    assert ab == 55

System Verilog Registers
------------------------

.. code-block:: python

    r = svreg(28)(0xabadbee)
    r2 = r[15:4]
    assert r2 == 0xbad
    r2.v_ = 0xead
    r[3:0] = 0xd
    assert r == 0xdeadbee

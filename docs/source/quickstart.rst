Quickstart
==========

Here's a quick example to get you started with `bffl`:

.. code-block:: python

    from bffl import struct, uint

    @struct
    class parrot_struct:
        status: uint(2, {'dead': 0, 'pining': 1, 'resting': 2})
        plumage_rgb: uint(5)[3]

    @struct
    class quest_struct:
        quest: uint(3, {'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3, 'gourd': 4})
        knights: knight_struct[3]
        holy: uint[1]
        parrot: parrot_struct

    def get_dead_parrot_quests(raw_data_source):
        data = quest_struct()
        status = data.parrot.status

        for data.n_ in raw_data_source:
            if status == 'dead':
                yield data.json_

    for jstr in get_dead_parrot_quests(sequence_of_integers_from_somewhere()):
        print(jstr)

This example demonstrates how to define structures, use enums, and work with bit fields.


# bffl
**Bit Fields For Lumberjacks**

![lumberjack](https://raw.githubusercontent.com/kenseehart/bffl/main/images/bffl800.png)

`bffl` is a high-performance bit field protocol framework for working with packed binary data. It's ideal for scenarios requiring precise control of bit arrangements, such as verilog interfaces and arbitrary bitfield manipulations.

## Quickstart

#### Standard installation:

``` bash
pip install bffl
```

#### Development installation (if you want to work on bffl):

``` bash
git clone git@github.com:kenseehart/bffl.git
cd bffl
pip install -e .
pytest
```

## Reporting Bugs and Suggesting Features

If you encounter any bugs or unexpected behavior, please [open an issue](https://github.com/kenseehart/bffl/issues/new?template=bug_report.md).

If you have a suggestion to make `bffl` even more useful, please [open a feature request](https://github.com/kenseehart/bffl/issues/new?template=feature_request.md).

## Expressive type system

Your protocol is expressed concisely using compositions of types.
 
#### atomic types
- signed/unsigned ints of any size
- enumerations
- floating point in any format (you can define custom floats)
- fixed point
- decimal
- *future:* quantization

#### compound types
- struct
- array
- *future:* union

#### custom types

The typing system is highly customizable. You define evaluation, packing logic, and any other behaviors you need.

## Comparison to [ctypes](https://docs.python.org/3/library/ctypes.html)

While `bffl` and `ctypes` both handle binary data in Python, their primary purposes differ. `ctypes` maps to C structs, whereas `bffl` maps to bit vectors.
Note that `ctypes` supports C++ style bitfields, which are suitable for some use cases, but due to characteristics of C++ bitfields, `ctypes` cannot gurantee predictable behavior (because packing logic depends on hardware architecture).
If your use case doesn't require binary compatibility, this consideration might not matter.

| **Tool** | **Model** | **Primary Purpose** | **Implementation** |
|----------|-----------|---------------------|--------------------|
| `ctypes` | C/C++ types | Interface with C/C++ code, model C/C++ datatypes | Python, C++ |
| `bffl`   | Bit fields | Model arbitrary bit-aligned datatypes and interfaces | Python |

#### Use Cases:
- **`ctypes`**:
  - Interfacing with C/C++ libraries.
  - System-level programming.
  - Handling performance-critical applications using C/C++.
  - Optimal for compute-bound tasks where hardware-specific optimizations are beneficial.
  - Memory mapping optimized your hardware

- **`bffl`**:
  - Protocol implementation requiring precise bit-level control.
  - Verilog interface testing.
  - Custom binary data formats with exact bit alignment.
  - Consistent behavior across different hardware architectures.
  - Ideal for IO-bound tasks and memory transfers, where exact bit-level management is crucial.
  - Memory mapping is portable (independent of hardware architecture)

## Comparison to Bitfields in C++

C++ typically controls bit allocation for optimal performance, respecting byte or word boundaries, which can hinder precise bit-level control. `bffl` offers explicit control over bit allocation, with no implicit padding. This is crucial for protocol implementations and verilog interfaces, where predictable bitwise allocation is required.

In `bffl`, a struct with a 5-bit integer and a 13-bit integer is exactly 18 bits, and an array of 5 such structs is 90 bits. Python's `int` type supports unbounded bit fields, allowing flexible manipulation without byte misalignment issues.

## Ease of Use

```python
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

def get_dead_parrot_quests(raw_data_source: Sequence[int]) -> Iterator[str]:
    data = quest_struct()
    status = data.parrot.status

    for data.n_ in raw_data_source:
        if status == 'dead':
            yield data.json_

for jstr in get_dead_parrot_quests(sequence_of_integers_from_somewhere()):
    print(jstr)
```

## Special attributes

Fields in `bffl` have read/write properties exposing data:

| Attribute | Description |
|-----------|-------------|
| `n_`      | Raw bits as an int (unbounded size) |
| `v_`      | Data value as basic types (int, float, str, list, dict) |
| `json_`   | Data value as a JSON string |

#### Trailing Underscore Convention

Non-field attributes in `bffl` are marked with a trailing underscore to distinguish them from fields. This allows full use of the field namespace.

## Performance

`bffl` achieves performance by performing symbolic processing during interface allocation, reducing runtime overhead. Bound field computations typically involve simple `shift-and` operations.

```python
@struct
class Quest:
    qtype: uint(2, {'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3})
    count: uint[3]
    alive: uint[1]

@struct
class MyProtocol:
    header: uint[5]
    a: Quest
    b: Quest
    c: Quest

def look_for_fives(datastream: Sequence[int]):
    buffer = MyProtocol()
    bcount = buffer.b.count # sybolic overhead outside the loop
    for n in datastream:
        buffer.n_ = n
        if bcount == 5: # low overhead (simple shift-and operation)
            do_something()
```

Expression jit converts python expressions into a low level C expressions.

*`future`* This will support high performance integration with `pytorch`, `numpy`, `bcolz`, etc.

```python
    @struct
    class seven_type:
        a: uint[3]
        b: uint[4]

    seven = seven_type()

    assert seven.a.expr_() == '(n >> 4 & 0x7)'
    assert seven.b.expr_() == '(n & 0xf)'

    ab = seven['a * b']

    seven.a = 5
    seven.b = 11

    assert seven.a == 5
    assert ab == 55

    assert ab.expr_() == '(n >> 4 & 0x7) * (n & 0xf)'
```


### Metatypes, Field Types, and Fields

`bffl` uses metatypes to define complex datatypes. For example, `uint(5)` defines a 5-bit unsigned integer field type. Fields are instantiated and assigned values via the `v_` or `n_` attributes.

## Struct Syntax

There are two ways to define a new struct type:

#### Class Syntax

*This is the typical was to declare a new struct type.*

```python
@struct
class struct_name:
    field_name: field_type
    ...
```

#### Inline Syntax

*This syntax can be useful for programatic generation of new types. This mirrors the repr of a struct instance.*

```python
struct_name = struct('struct_name', [('field_name', field_type), ...])
```

## System Verilog Semantics (optional)

Normally, `bffl` uses pythonic index semantics. However, if you are working heavily with System Verilog, you might find it more intuitive to use System Verilog slice semantics.vaa

If a field is of type `svreg`, ranges are `[high:low]` and are inclusive of both high and low indexes.

Please note that while `bffl` is structurally ideal for this kind of thing, this feature set for System Verilog needs more work. If you are intending to use `bffl` for a verilog application, please contact us so we know it's a priority. [open a feature request](https://github.com/kenseehart/bffl/issues/new?template=feature_request.md)

```python
r = svreg(28)(0xabadbee)
r2 = r[15:4]
assert r2 == 0xbad
r2.v_ = 0xead
r[3:0] = 0xd
assert r == 0xdeadbee
```

## Related Projects

Here is a comparison grid of various bitfield-related libraries with verified licenses:

| **Library** | **Description** | **Primary Purpose** |
|-------------|-----------------|---------------------|
| **[bitvector](https://github.com/JnyJny/bitvector)** | Bit vector implementation with BitField descriptor for sub-byte bit addressing | Address and manipulate bits in integer words |
| **[bfield](https://pypi.org/project/bfield)** | Convenient bit fields for int subclasses | Define and manipulate bitfields |
| **[ctypes-bitfield](https://pypi.org/project/ctypes-bitfield/)** | Bitfields with ctypes integration | Interface with C/C++ bitfields |
| **[sparsebitfield](https://pypi.org/project/sparsebitfield/)** | Manage sparse sets of large integers | Efficiently manage large sets of bits | JavaScript |
| **[bitfield](https://github.com/stestagg/bitfield)** | Sparse sets of large integers optimized for sequential integers | Handle large, sparse integer sets |
| **[named_bitfield](https://github.com/not-napoleon/named_bitfield)** | Define named bitfields for easier access and manipulation | Named bitfields |
| **[bitstring](https://github.com/scott-griffiths/bitstring)** | Supports slicing and manipulating bit strings | Handle and manipulate bit strings |


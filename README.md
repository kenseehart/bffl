
# bffl
**Bit Fields For Lumberjacks**

![lumberjack](https://raw.githubusercontent.com/kenseehart/bffl/main/images/bffl800.png)

`bffl` is a high-performance bit field protocol framework for working with packed binary data. It's ideal for scenarios requiring precise control of bit arrangements, such as verilog interfaces and arbitrary bitfield manipulations. Your protocol is expressed concisely using compositions of ints, structs, arrays, and user-defined types.

### Quickstart

#### Standard installation:

``` bash
pip install bffl
```

#### Development installation (if you want to work on bffl):

``` bash
git clone git@github.com:kenseehart/bffl.git
cd bffl
pip install -e .
```


### Comparison to [ctypes](https://docs.python.org/3/library/ctypes.html)

While `bffl` and `ctypes` both handle binary data in Python, their primary purposes differ. `ctypes` maps to C structs, whereas `bffl` maps to bit vectors.

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

### Comparison to Bitfields in C++

C++ typically controls bit allocation for optimal performance, respecting byte or word boundaries, which can hinder precise bit-level control. `bffl` offers explicit control over bit allocation, with no implicit padding. This is crucial for protocol implementations and verilog interfaces, where predictable bitwise allocation is required.

In `bffl`, a struct with a 5-bit integer and a 13-bit integer is exactly 18 bits, and an array of 5 such structs is 90 bits. Python's `int` type supports unbounded bit fields, allowing flexible manipulation without byte misalignment issues.

### Ease of Use

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

### Interoperability

Fields in `bffl` have read/write properties exposing data:

| Attribute | Description |
|-----------|-------------|
| `n_`      | Raw bits as an int (unbounded size) |
| `v_`      | Data value as basic types (int, float, str, list, dict) |
| `json_`   | Data value as a JSON string |

### Performance

`bffl` achieves performance by performing symbolic processing during interface allocation, reducing runtime overhead. Bound field computations typically involve simple `shift-and` operations.

```python
@struct
class MyRegister:
    rtype: uint(2, {'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3})
    stuff: uint(3)
    junk: uint(1)

@struct
class MyProtocol:
    header: uint(5)
    a: MyRegister
    b: MyRegister
    c: MyRegister

def look_for_fives(datastream: Sequence[int]):
    buffer = MyProtocol()
    bstuff = buffer.b.stuff
    for n in datastream:
        buffer.n_ = n
        if bstuff == 5:
            handle_5()
```

### Trailing Underscore Convention

Fields in `bffl` are marked with a trailing underscore to distinguish them from non-field attributes. This allows full use of the field namespace.

### Metatypes, Field Types, and Fields

`bffl` uses metatypes to define complex datatypes. For example, `uint(5)` defines a 5-bit unsigned integer field type. Fields are instantiated and assigned values via the `v_` or `n_` attributes.

### Struct Syntax

#### Inline Syntax
```python
struct_name = struct('struct_name', [('field_name', field_type), ...])
```

#### Class Syntax
```python
class struct_name(metaclass=metastruct):
    field_name: field_type
    ...
```

### System Verilog Support

`bffl` includes an `svreg` type for System Verilog slice semantics.

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


simple-struct
=======

Define structures with default values that play well with IDE code completion and can be loaded from or exported to python dictionaries.

---

+ [Quick start](#quick-start)
+ [Installation](#installation)
+ [Usage](#usage)
    + [Create a structure](#create-a-structure)
    + [Instantiating a structure](#instantiating-a-structure)
    + [Setting and getting values](#setting-and-getting-values)

---


Quick start
---

    import simple_struct
    
    
    @simple_struct.structure
    class Job:
        id = None
        created = None
        status = "pending"
    
        @simple_struct.structure
        class config:
            url = None
            retries = 5
    
    
    my_job = Job()
    my_job.id = "job#456758"
    my_job.created = "2021-03-21T18:11:02+00:00"
    my_job.config.url = "http://service/query"


Installation
----

Install the `simple-struct` package via pip by issuing the following command with the desired release `X.X.X`: 

- `pip install git+https://github.com/y-du/simple-struct.git@X.X.X` 

Upgrade to new version: 

- `pip install --upgrade git+https://github.com/y-du/simple-struct.git@X.X.X`

Uninstall: 

- `pip uninstall simple-struct`


Usage
----

#### Create a structure

Structures are created as nested or separate classes that subclass `Structure`:

    from simple_struct import Structure
    
    
    class MyStruct(Structure):
        attribute_a = "default value a"
        
        class attribute_b(Structure):
            attribute_c = None
            attribute_d = None
---
    class AttributeB(Structure):
        attribute_c = None
        attribute_d = None
    
    
    class MyStruct(Structure):
        attribute_a = "default value a"
        attribute_b = AttributeB
---
    class MyStruct(Structure):

        class __AttributeB(Structure):
            attribute_c = None
            attribute_d = None

        attribute_a = "default value a"
        attribute_b = __AttributeB

Or by using the `@structure` decorator:

    from simple_struct import structure
    
    
    @structure
    class MyStruct:
        attribute_a = "default value a"
    
        @structure
        class attribute_b:
            attribute_c = None
            attribute_d = None

#### Instantiating a structure

With default values only:

    my_struct = MyStruct()
    print(my_struct.attribute_a)                # -> default value a
    print(my_struct.attribute_b.attribute_c)    # -> None

With values from a dictionary (attributes can be omitted):

    my_struct = MyStruct({"attribute_b": {"attribute_c": "new value"}})
    print(my_struct.attribute_a)                # -> default value a
    print(my_struct.attribute_b.attribute_c)    # -> new value

With keyword arguments:

    MyStruct(attribute_b={"attribute_c": "new value"})
    print(my_struct.attribute_a)                # -> default value a
    print(my_struct.attribute_b.attribute_c)    # -> new value

With values from a dictionary and keyword arguments:
    
    my_struct = MyStruct({"attribute_b": {"attribute_c": "new value"}}, attribute_a="some value")
    print(my_struct.attribute_a)                # -> some value
    print(my_struct.attribute_b.attribute_c)    # -> new value

#### Setting and getting values

Setting values via attribute:

    my_struct.attribute_a = "some value"
    print(my_struct.attribute_a)                # -> some value

Setting values from a dictionary (attributes can be omitted):

    my_struct.from_dict({"attribute_a": "some value"})
    print(my_struct.attribute_a)                # -> some value

Getting values via attribute:

    value = my_struct.attribute_a
    print(value)                                # -> some value

Getting values as a dictionary:

    values = my_struct.to_dict()
    print(values)                               # -> {'attribute_a': 'some value', 'attribute_b': {'attribute_c': None, 'attribute_d': None}}
    
    # OR
    
    values = dict(my_struct)
    print(values)                               # -> {'attribute_a': 'some value', 'attribute_b': {'attribute_c': None, 'attribute_d': None}}
    
Getting values via iterator:

    for key, value in my_struct:
        print("%s: %s" % (key, value))
    
    # -> attribute_a: some value
    # -> attribute_b: {'attribute_c': None, 'attribute_d': None}

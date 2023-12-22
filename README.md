# python-metaprogramming-exercise

The goals here is to implement a record structure that allows for an easy declarative programming structure. This is a toy exercise but utilizes techniques similar to projects like the Django ORM to allow for the behavior and structure of classes to be defined very declaratively. You must implement the Record class such that the fields are defined declaratively. The fields define a human readably label as well as a precondition which can check properties of a field on construction. The type of a field is defined by the attribute type annotation. An example is below:

```python
class Person(Record):
    """
    A simple person record
    """ 
    name: str = Field(label="The name") 
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)
```

The requirements of the Record are:
* It must generate a constructor that takes the appropriate keyword arguments.
* If an argument is missing it must raise a TypeError
* If an extra argument is given it must raise a TypeError
* If the argument is given with the incorrect type it must raise a TypeError
* The arguments must check the precondition is one is given, and raise a TypeError if the precondition is violated
* It must expose the fields as readonly properties, and raise an AttributeError if an attempt is made to set them after construction.
* It must customize the `__str__` method to create a pretty representation as shown below.
* Inheritance should work in a sensible way.

Example usage of the Person class would be:
```python

# This should work
james = Person(name="James", age=34, income=24000.0)

# This should raise a error
james.age = 32
```

`print(str(james))` should output:

```
Person(
  # The name
  name='James'

  # The person's age
  age=34

  # The person's income
  income=24000.0
)
```

With inheritance the following should be possible:

```python
class Named(Record):
    """
    A base class for things with names
    """
    name: str = Field(label="The name") 

class Animal(Named):
    """
    An animal
    """
    habitat: str = Field(label="The habitat", precondition=lambda x: x in ["air", "land","water"])
    weight: float = Field(label="The animals weight (kg)", precondition=lambda x: 0 <= x)

class Dog(Animal):
    """
    A type of animal
    """
    bark: str = Field(label="Sound of bark")

mike = Dog(name="mike", habitat="land", weight=50., bark="ARF")
```

There are probably a number of ways to skin this problem, but the solution must use metaclasses. Metaclasses allow for the programmer to intersect the class creation process. This is done through setting the metaclass attribute of a class, the outline would be:

```python
class RecordMeta(type):
    def __new__(cls, name, bases, attr):
        # Implement the class creation by manipulating the attr dictionary
        return super(RecordMeta, cls).__new__(cls, name, bases, new_attr)

# Set the metaclass of the Record class
class Record(metaclass=RecordMeta):
    pass
```

Inorder to get inheritance to work correctly you will need to use the Method Resolution Order (MRO) with the `cls.mro()` method. You can access the annotations with the `cls.__annotations__`. dictionary.

A test suite is given in the tests.py file. This can be run with `python tests.py`. You should implement the Th Record and related classes in that file at the appropriate location.  All the test should pass.

There are a bunch of concepts you will need to use:
* Metaclasses
* property()
* cls.mro()
* Type annotations
* getattr/setattr
* `__str__`

It is not expected that you will know all these language features, but you should be able to figure them out. There is a wealth of information online about how these work. If anything is unclear please contact me. The implementation should not take more than 100 lines. 
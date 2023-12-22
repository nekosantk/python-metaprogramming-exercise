from unittest import TestCase
import unittest
from textwrap import dedent
from dataclasses import dataclass
from typing import Callable, Any, Dict


@dataclass
class Field:
    """
    Defines a field with a label and preconditions
    """
    label: str
    precondition: Callable[[Any], bool] = None



class RecordMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in bases[::-1]:
            if hasattr(base, '_fields'):
                fields.update(base._fields)

        fields.update({key: value for key, value in attrs.items() if isinstance(value, Field)})

        for field_name, field_value in fields.items():
            attrs[field_name] = property(
                fget=lambda self, name=field_name: self.get_value(name)
            )

        attrs['_fields'] = fields
        return super().__new__(cls, name, bases, attrs)


# Record and supporting classes here
class Record(metaclass=RecordMeta):
    """
    Base class for records with fields and preconditions.
    """
    def __init__(self, **kwargs):

        required_keys = set(self._fields.keys())
        incoming_keys = set(kwargs.keys())

        if len(required_keys - incoming_keys) > 0: raise TypeError("Required keys are missing.")
        if len(incoming_keys - required_keys) > 0: raise TypeError("Too many keys were provided.")

        for field_name, field_value in kwargs.items():
            precondition = getattr(self._fields.get(field_name), 'precondition', None)
            if precondition and not precondition(field_value):
                raise TypeError(f"Precondition for field '{field_name}' is violated")

            setattr(self, "_" + field_name, field_value)

    def get_value(self, name):
        return getattr(self, "_" + name)

    def __str__(self):
        fields_str = "\n".join(
            [f"  # {self._fields[key].label}\n  {key}='{getattr(self, key)}'\n" if isinstance(getattr(self, key), str)
             else f"  # {self._fields[key].label}\n  {key}={getattr(self, key)}\n" for key in self._fields])
        return f"{self.__class__.__name__}(\n{fields_str})"


# Usage of Record
class Person(Record):
    """
    A simple person record
    """
    name: str = Field(label="The name")
    age: int = Field(label="The person's age", precondition=lambda x: 0 <= x <= 150)
    income: float = Field(label="The person's income", precondition=lambda x: 0 <= x)


class Named(Record):
    """
    A base class for things with names
    """
    name: str = Field(label="The name")


class Animal(Named):
    """
    An animal
    """
    habitat: str = Field(label="The habitat", precondition=lambda x: x in ["air", "land", "water"])
    weight: float = Field(label="The animals weight (kg)", precondition=lambda x: 0 <= x)


class Dog(Animal):
    """
    A type of animal
    """
    bark: str = Field(label="Sound of bark")


# Tests
class RecordTests(TestCase):
    # def test_creation(self):
    #     Person(name="JAMES", age=110, income=24000.0)
    #     with self.assertRaises(TypeError):
    #         Person(name="JAMES", age=160, income=24000.0)
    #     with self.assertRaises(TypeError):
    #         Person(name="JAMES")
    #     with self.assertRaises(TypeError):
    #         Person(name="JAMES", age=-1, income=24000.0)
    #     with self.assertRaises(TypeError):
    #         Person(name="JAMES", age="150", income=24000.0)
    #     with self.assertRaises(TypeError):
    #         Person(name="JAMES", age="150", wealth=24000.0)

    def test_properties(self):
        james = Person(name="JAMES", age=34, income=24000.0)
        print("TEST", james.age)
        print("TEST", james.name)
        self.assertEqual(james.age, 34)
        with self.assertRaises(AttributeError):
            james.age = 32

    # def test_str(self):
    #     james = Person(name="JAMES", age=34, income=24000.0)
    #     correct = dedent("""
    #     Person(
    #       # The name
    #       name='JAMES'
    #
    #       # The person's age
    #       age=34
    #
    #       # The person's income
    #       income=24000.0
    #     )
    #     """).strip()
    #     self.assertEqual(str(james), correct)

    # def test_dog(self):
    #     mike = Dog(name="mike", habitat="land", weight=50., bark="ARF")
    #     self.assertEqual(mike.weight, 50)


if __name__ == '__main__':
    unittest.main()
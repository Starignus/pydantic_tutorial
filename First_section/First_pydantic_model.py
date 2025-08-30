"""
Creating our first Pydantic model examples

Basic Data Models Pydatic
"""

# Importing BaseModel - to enforce type hints at runtime
from pydantic import BaseModel


# Type hints are required for the attributes
class User(BaseModel):
    name: str
    age: int
    is_active: bool


# We can also set default values
class Student(BaseModel):
    name: str
    age: int = 18
    subject: str


def first_simple_example():
    # Create an instance
    user = User(name="Bob", age=30, is_active=True)
    print(user)
    # We can also print it like this, resulting in a dictionary
    print(user.model_dump())


def set_default_values_example():
    # Here, we don't need to pass in the age; if we do, it will overwrite the default
    student = Student(name="Jeff", age=16, subject="Mathematics")
    print(student)


def type_validation_example():
    # String age gets converted to int - AUTOMATIC!
    user = User(name="Bob", age="25", is_active=True)
    # name='Bob' age=25 is_active=True
    print(user)
    print(type(user.age))

    # Invalid case
    try:
        User(name="Charlie", age="twenty", is_active=False)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    first_simple_example()
    set_default_values_example()
    type_validation_example()

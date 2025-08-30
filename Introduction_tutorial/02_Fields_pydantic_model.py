"""
In Pydantic, Field() lets us add metadata, validation rules,
and custom behaviour to a model field.

For further information, you can use the documentation:
https://docs.pydantic.dev/latest/concepts/fields/

The metadata might be useful for agents (LMM) to know what
each variable is for, but I would argue that it is also useful for
humans that information.
"""

# Basic example using Field()
from pydantic import BaseModel, Field, ValidationError


class FieldUser(BaseModel):
    # this does not mean it is default!, it is just a description
    name: str = Field(description="The user's full name")


# if we want defaults, we can add on this parameter
class FieldUserDefault(BaseModel):
    name: str = Field(description="The user's full name", default="John")


class FlawUser(BaseModel):
    age: int = Field(default="twelve")


class ProperUser(BaseModel):
    # Force validation
    age: int = Field(default="twelve", validate_default=True)


def simple_field():
    field_user = FieldUser(name="Vaibhav")
    print(field_user)


def field_default_value():
    # did not pass anything this time!
    field_user2 = FieldUserDefault()
    print(field_user2)


def default_value_not_validated():
    """
    Now we are going to explore a problem: Pydantic does
    NOT validate the default value by default.
    This happens because Pydantic only validates
    user input by default.
    """
    user = FlawUser()
    # This gives: "twelve" which is wrong!
    print(user.age)
    print(type(user.age))


def force_validation():
    try:
        user = ProperUser()
    except ValidationError as e:
        print(e)
    print(user.age)


if __name__ == "__main__":
    simple_field()
    field_default_value()
    default_value_not_validated()
    force_validation()

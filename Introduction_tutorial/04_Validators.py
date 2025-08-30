"""
Exercise

First:

We need to create a Book model which has:

Required title (string, 1-100 chars)
Required author (string)
Optional isbn
price (positive float ≤1000)
in_stock (boolean, default True)

Note: ISBN (International Standard Book Number) is normally exactly 13 digits, so to be able to
include that in our class, we would need to use regex expressions.

These regex expressions provide constraints. In this example, we would have to define ISBN as:

isbn: str = Field(default = None, regex=r"^\d{13}$")
However, this is beyond the scope of this tutorial, as it requires prior knowledge of regular expressions (regex).

There is another way to do this, though.

Second:
Validation is one of the biggest reasons we use Pydantic. We will explore it in this section.
https://docs.pydantic.dev/latest/concepts/validators/

@model_validator is used when we want to:

- Validate multiple fields together
- To perform logic that involves the whole model
- Run code before or after normal field validation

@model_validator has 2 options:

1. before - before validation
2. after - after validation

Before (Data still might be wrong) --> Object Installation and Validation --> After (Data is clean and correct)

Example:
class User(BaseModel):
    age: int

User(age="25")
Before validation: age is "25" --> still a string
After validation: age is 25 --> now an integer
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str
    author: str = Field(default=None)
    price: float = Field(gt=0, lt=1000)
    in_stock: bool = Field(default=True)


def valid_book():
    book: Book = Book(title="Invisible Women", author="The Author", price=100)
    print(book.model_dump())


# Model Validator


# After validators: run after the whole model has been validated.
class Event(BaseModel):
    name: str
    start_hour: int
    end_hour: int

    @model_validator(mode="after")  # Use a decorator
    def check_time(self):
        if self.end_hour <= self.start_hour:
            raise ValueError(
                "end_hour must be greater than start_hour. Please fix this!"
            )

        return self


def after_validation_event():
    # How can start an hour be before the end time (we are working in 24-hour clock)
    event = Event(name="Hackathon", start_hour=10, end_hour=9)
    print("Before model validation:", event.model_dump())


class Delivery(BaseModel):
    pickup: int
    drop: int

    # Before validators: They are run before the model is instantiated.
    @model_validator(mode="before")
    @classmethod
    def fix_input(cls, data):
        print("Before validator sees raw input:", data)
        # Let's swap them if they are reversed
        if int(data["drop"]) < int(data["pickup"]):
            data["pickup"], data["drop"] = data["drop"], data["pickup"]
        return data


def after_validation_delivery():
    order = Delivery(pickup=15, drop=13)
    print("After model validation:", order.model_dump())


# @model_validator() can handle multiple fields
# @field_validator is focused on only one field.
class Product(BaseModel):
    price: float

    # After validators: run after Pydantic's internal validation.
    # They are generally more type safe and thus easier to implement.
    # Pydantic runs to check if it is a float, and then de field validator
    # which assumes it is already a float and not a string, for example.
    @field_validator("price", mode="after")
    @classmethod
    def must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value


def after_field_validation():
    # This can also be achieved using the `Field`
    product1 = Product(price=-10)
    print(product1.model_dump())


class EnsureList(BaseModel):
    numbers: list[int]

    # Before validators: run before Pydantic's internal parsing and validation
    # (e.g. coercion of a str to an int). These are more flexible than after validators,
    # but they also have to deal with the raw input, which in theory could be
    # any arbitrary object.
    # Here, the field_validator runs before, and after Pydantic runs to see if it is a List of Int
    @field_validator("numbers", mode="before")
    @classmethod
    def ensure_list(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return [value]
        else:
            return value


def before_field_validation():
    list_example = EnsureList(numbers=2)
    print(list_example.model_dump())
    list_two = EnsureList(numbers=[1, 3, "4"])
    print(list_two.model_dump())


if __name__ == "__main__":
    valid_book()
    after_validation_event()
    after_validation_delivery()
    after_field_validation()
    before_field_validation()

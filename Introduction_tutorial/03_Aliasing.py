"""
An alias is a different name that our model can use to:

Accept input (validation)
Give output (serialisation)
This is helpful when the external name ≠ does not equal the internal variable name.

Let's explore a real-world example together:

Suppose we are working with a logistics API:

JSON from the API:

{
  "pkg_weight_kg": 4.5,
  "pkg_dest": "Singapore",
  "pkg_is_fragile": true
}
But in our Python backend code, we would prefer:

weight
destination
is_fragile
"""

from pydantic import BaseModel, Field, ValidationError


class Package(BaseModel):
    weight: float = Field(alias="pkg_weight_kg")
    destination: str = Field(alias="pkg_dest")
    is_fragile: bool = Field(alias="pkg_is_fragile")


def package_example():
    data = {"pkg_weight_kg": 4.5, "pkg_is_fragile": True, "pkg_dest": "Singapore"}

    # Unpacking the Dictionary - takes each key-value pair
    # and passes them as named arguments. You can see that
    # you do not need to pass them in the same order as created
    # in the class
    package = Package(**data)

    # We can access using our own field names
    print(package.weight)
    # print(package.pkg_weight_kg) # No such thing!
    print(package.destination)
    print(package.is_fragile)

    # Exporting with original alias names
    print(package.model_dump(by_alias=True))


class Student(BaseModel):
    # email is the internal variable
    # The validation name is what is expected as input from API
    # The serialization name is what is expected as the output variable for Back-End
    email: str = Field(
        validation_alias="student_email",  # Accepts this as input
        serialization_alias="studentEmail",  # Outputs this name
    )


def student_example():
    # Incoming data (e.g. from an API)
    incoming_data = {"student_email": "hi@gmail.com"}

    student = Student(**incoming_data)
    print(student.email)

    print(student.model_dump())  # {'email': 'hi@gmail.com'}
    print(
        student.model_dump(by_alias=True)
    )  # {'studentEmail': 'hi@gmail.com'} - uses serialization alias!


class Book(BaseModel):
    title: str = Field(
        validation_alias="book_title",  # Input will use this
        serialization_alias="bookTitle",  # Output will use this
    )
    author: str = Field(
        validation_alias="author_name",  # Input will use this
        serialization_alias="authorName",  # Output will use this
    )


def book_example():
    backend_data = {"book_title": "Pydantic Guide", "author_name": "DataCamp"}

    book = Book(**backend_data)

    print(book.title)
    print(book.author)
    print(book.model_dump())  # {'title': 'Pydantic Guide', 'author': 'DataCamp'}
    print(
        book.model_dump(by_alias=True)
    )  # 'bookTitle': 'Pydantic Guide', 'authorName': 'DataCamp'}


class Product(BaseModel):
    # Numeric Limits - part of Validation which we will be covering soon
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)  # gt:greater than
    description: str | None = Field(default=None, max_length=300)


def numeric_validation_example():
    # Example usage
    valid_product = Product(name="Laptop", price=999.99, description="Very cool laptop")
    print(valid_product)

    try:
        # Now let's try to create an invalid product
        invalid_product = Product(
            name="", price=-10
        )  # This will trigger 2 validation errors
        print(invalid_product)
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    package_example()
    student_example()
    book_example()
    numeric_validation_example()

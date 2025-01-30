# CK Recursive Dataclass

A Python library that extends Python's dataclasses to support recursive serialization and deserialization of nested dataclass structures. This library makes it easy to work with complex, nested data structures while maintaining type safety and providing convenient conversion methods between dataclasses and dictionaries.

## Features

- 🔄 Recursive conversion between dataclasses and dictionaries
- 🌳 Support for multiple nested dataclass structures
- 📦 Handle dictionaries and lists of dataclasses
- 📝 Type-safe with full mypy support
- ✨ Optional field support with None handling
- 🔍 Type preservation with __type__ field
- 🚀 Easy serialization for API responses
- 🐍 Compatible with Python 3.11 and 3.12

## Installation

```bash
pip install ck-recursive-dataclass
```

## Quick Start

Here's a simple example of how to use recursive dataclasses:

```python
from dataclasses import dataclass
from ck_recursive_dataclass import RecursiveDataclass
from typing import Optional, Dict

@dataclass
class Address(RecursiveDataclass):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None

@dataclass
class Occupation(RecursiveDataclass):
    title: str
    company: str
    years_experience: int
    department: Optional[str] = None

@dataclass
class Person(RecursiveDataclass):
    name: str
    age: int
    addresses: Dict[str, Address]
    occupation: Occupation
    email: Optional[str] = None

# Create instances
home_address = Address(
    street="123 Home St",
    city="Hometown",
    country="Homeland",
    postal_code="12345"
)

work_address = Address(
    street="456 Work Ave",
    city="Workville",
    country="Workland"
)

occupation = Occupation(
    title="Senior Developer",
    company="Tech Corp",
    years_experience=5,
    department="Engineering"
)

person = Person(
    name="John Doe",
    age=30,
    addresses={"home": home_address, "work": work_address},
    occupation=occupation,
    email="john@example.com"
)

# Convert to dictionary
person_dict = person.to_dict()
print("Person as dictionary:")
print(person_dict)
# Output:
# {
#     'name': 'John Doe',
#     'age': 30,
#     'addresses': {
#         'home': {
#             'street': '123 Home St',
#             'city': 'Hometown',
#             'country': 'Homeland',
#             'postal_code': '12345',
#             '__type__': 'Address'
#         },
#         'work': {
#             'street': '456 Work Ave',
#             'city': 'Workville',
#             'country': 'Workland',
#             'postal_code': None,
#             '__type__': 'Address'
#         }
#     },
#     'occupation': {
#         'title': 'Senior Developer',
#         'company': 'Tech Corp',
#         'years_experience': 5,
#         'department': 'Engineering',
#         '__type__': 'Occupation'
#     },
#     'email': 'john@example.com',
#     '__type__': 'Person'
# }

# Create from dictionary
new_person = Person.from_dict(person_dict)
```

## Features in Detail

### Multiple Nested Dataclasses

The library handles multiple levels of nested dataclass structures automatically. For example, a `Person` can have both `addresses` and `occupation` as nested dataclasses:

```python
person = Person(
    name="John Doe",
    addresses={"home": home_address},  # Address dataclass
    occupation=occupation,             # Occupation dataclass
    age=30
)
```

### Dictionary of Dataclasses

You can use dictionaries with dataclass values, and the library will handle the conversion properly:

```python
addresses = {
    "home": Address("123 Home St", "Hometown", "Homeland"),
    "work": Address("456 Work Ave", "Workville", "Workland")
}
```

### Nested Dataclass Support

The library handles nested dataclass structures automatically, maintaining type information and validation throughout the conversion process.

### Optional Fields

Fields marked as Optional will be properly handled during conversion:

```python
@dataclass
class User(RecursiveDataclass):
    username: str
    email: Optional[str] = None
```

### Type Safety

The library is fully type-hinted and works well with mypy for static type checking. During conversion:

- Type information is preserved using the `__type__` field
- Required fields are validated
- Type mismatches are caught during deserialization

```python
# Type validation during deserialization
try:
    # This will raise ValueError due to missing required field 'street'
    invalid_address = Address.from_dict({
        "city": "New York",
        "country": "USA"
    })
except ValueError as e:
    print(f"Validation error: {e}")  # Missing required field street

try:
    # This will raise TypeError due to invalid input type
    invalid_person = Person.from_dict("not a dictionary")
except TypeError as e:
    print(f"Type error: {e}")  # Expected dict, got str
```

### Serialization Support

The library is particularly useful for API development where you need to:
- Serialize complex objects to JSON-compatible dictionaries
- Deserialize nested JSON data into typed Python objects
- Maintain type safety throughout the process

For example:
```python
# API response serialization
@app.get("/user/{user_id}")
def get_user(user_id: str):
    user = get_user_from_db(user_id)  # Returns Person object
    return user.to_dict()  # Returns JSON-serializable dictionary

# API request deserialization
@app.post("/user")
def create_user(user_data: dict):
    user = Person.from_dict(user_data)  # Converts dictionary to Person object
    save_user_to_db(user)
    return {"status": "success"}
```

## Development

### Prerequisites

- Python 3.11 or higher
- tox for running tests

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/kimcharli/ck_recursive_dataclass.git
cd ck_recursive_dataclass
```

2. Install development dependencies:
```bash
pip install tox
```

3. Run tests:
```bash
tox
```

### Running Tests

The project uses tox to run tests across different Python versions and environments:

- Python 3.11 and 3.12 environments for compatibility testing
- Type checking with mypy
- Linting with ruff

Run all tests with:
```bash
tox
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Charlie Kim (kimcharli@gmail.com)
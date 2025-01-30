# CK Recursive Dataclass

A Python library that extends Python's dataclasses to support recursive serialization and deserialization of nested dataclass structures. This library makes it easy to work with complex, nested data structures while maintaining type safety and providing convenient conversion methods between dataclasses and dictionaries.

## Features

- 🔄 Recursive conversion between dataclasses and dictionaries
- 🌳 Support for nested dataclass structures
- 📦 Handle dictionaries of dataclasses
- 📝 Type-safe with full mypy support
- ✨ Optional field support
- 📋 List and tuple support for collections of dataclasses
- 🔍 Comprehensive validation during conversion
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
class Person(RecursiveDataclass):
    name: str
    age: int
    addresses: Dict[str, Address]
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

person = Person(
    name="John Doe",
    age=30,
    addresses={"home": home_address, "work": work_address},
    email="john@example.com"
)

# Convert to dictionary
person_dict = person.to_dict()

# Create from dictionary
new_person = Person.from_dict(person_dict)
```

## Features in Detail

### Nested Dataclass Support

The library handles nested dataclass structures automatically, maintaining type information and validation throughout the conversion process.

### Dictionary of Dataclasses

You can use dictionaries with dataclass values, and the library will handle the conversion properly:

```python
addresses = {
    "home": Address("123 Home St", "Hometown", "Homeland"),
    "work": Address("456 Work Ave", "Workville", "Workland")
}
```

### Optional Fields

Fields marked as Optional will be properly handled during conversion:

```python
@dataclass
class User(RecursiveDataclass):
    username: str
    email: Optional[str] = None
```

### Type Safety

The library is fully type-hinted and works well with mypy for static type checking.

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
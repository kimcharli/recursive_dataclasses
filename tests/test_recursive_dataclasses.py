from dataclasses import dataclass
from typing import List, Dict
from recursive_dataclasses import from_dict, update_dataclass


@dataclass
class Address:
    street: str = ""
    city: str = ""
    country: str = ""


@dataclass
class Contact:
    email: str = ""
    phone: str = ""


@dataclass
class Person:
    name: str = ""
    age: int = 0
    address: Address = None
    contacts: List[Contact] = None
    metadata: Dict[str, str] = None


def test_nested_dataclass():
    # Test data
    data = {
        "name": "John Doe",
        "age": 30,
        "address": {"street": "123 Main St", "city": "New York", "country": "USA"},
        "contacts": [
            {"email": "john@example.com", "phone": "123-456-7890"},
            {"email": "john.doe@work.com", "phone": "098-765-4321"},
        ],
        "metadata": {"department": "Engineering", "role": "Developer"},
    }

    # Test from_dict function
    person = from_dict(Person, data)

    # Verify the data
    assert person.name == "John Doe"
    assert person.age == 30
    assert isinstance(person.address, Address)
    assert person.address.street == "123 Main St"
    assert person.address.city == "New York"
    assert isinstance(person.contacts, list)
    assert len(person.contacts) == 2
    assert isinstance(person.contacts[0], Contact)
    assert person.contacts[0].email == "john@example.com"
    assert isinstance(person.metadata, dict)
    assert person.metadata["department"] == "Engineering"

    # Test updating existing instance
    update_data = {
        "age": 31,
        "address": {"city": "Boston"},
        "contacts": [{"email": "new@example.com", "phone": "555-555-5555"}],
    }

    # Test update_dataclass function
    person = update_dataclass(person, update_data)

    # Verify updates
    assert person.age == 31
    assert person.address.city == "Boston"
    # Original data should be preserved when not updated
    assert person.address.street == "123 Main St"
    assert person.contacts[0].email == "new@example.com"

    # Test None handling
    null_data = {"address": None, "contacts": None, "metadata": None}
    person = update_dataclass(person, null_data)
    assert person.address is None
    assert person.contacts is None
    assert person.metadata is None

    # Test error handling
    try:
        update_dataclass("not a dataclass", {})
        assert False, "Should raise TypeError"
    except TypeError:
        pass

    try:
        update_dataclass(person, "not a dict")
        assert False, "Should raise TypeError"
    except TypeError:
        pass


if __name__ == "__main__":
    test_nested_dataclass()
    print("All tests passed!")

from typing import Optional, List, Dict
from dataclasses import dataclass
import pytest

from ck_recursive_dataclass import RecursiveDataclass


@dataclass
class Address(RecursiveDataclass):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None


@dataclass
class Contact(RecursiveDataclass):
    email: str
    phone: Optional[str] = None


@dataclass
class Person(RecursiveDataclass):
    name: str
    age: int
    addresses: Dict[str, Address]
    contacts: List[Contact]
    notes: Optional[str] = None


def test_simple_dataclass():
    """Test basic dataclass functionality."""
    address = Address(
        street="123 Main St", city="New York", country="USA", postal_code="10001"
    )

    # Test to_dict
    address_dict = address.to_dict()
    assert address_dict["street"] == "123 Main St"
    assert address_dict["city"] == "New York"
    assert address_dict["country"] == "USA"
    assert address_dict["postal_code"] == "10001"
    assert address_dict["__type__"] == "Address"

    # Test from_dict
    new_address = Address.from_dict(address_dict)
    assert new_address.street == "123 Main St"
    assert new_address.city == "New York"
    assert new_address.country == "USA"
    assert new_address.postal_code == "10001"


def test_optional_fields():
    """Test handling of optional fields."""
    # Test with all fields
    contact1 = Contact(email="test@example.com", phone="+1-555-555-5555")
    assert contact1.phone == "+1-555-555-5555"

    # Test without optional field
    contact2 = Contact(email="test@example.com")
    assert contact2.phone is None

    # Test conversion to/from dict
    contact_dict = contact2.to_dict()
    assert contact_dict["phone"] is None

    new_contact = Contact.from_dict(contact_dict)
    assert new_contact.phone is None


def test_nested_dataclass():
    """Test nested dataclass structures."""
    person_data = {
        "name": "John Doe",
        "age": 30,
        "addresses": {
            "home": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA",
                "postal_code": "10001",
            },
            "work": {
                "street": "456 Business Ave",
                "city": "Manhattan",
                "country": "USA",
                "postal_code": "10002",
            },
        },
        "contacts": [
            {"email": "john@example.com", "phone": "+1-555-555-5555"},
            {"email": "john.doe@work.com"},
        ],
        "notes": "Test notes",
    }

    # Test from_dict with nested structure
    person = Person.from_dict(person_data)
    assert person.name == "John Doe"
    assert person.age == 30
    assert len(person.addresses) == 2
    assert person.addresses["home"].street == "123 Main St"
    assert person.addresses["work"].city == "Manhattan"
    assert len(person.contacts) == 2
    assert person.contacts[0].email == "john@example.com"
    assert person.contacts[1].phone is None

    # Test to_dict with nested structure
    person_dict = person.to_dict()
    assert person_dict["name"] == "John Doe"
    assert person_dict["addresses"]["home"]["street"] == "123 Main St"
    assert person_dict["contacts"][0]["phone"] == "+1-555-555-5555"
    assert person_dict["contacts"][1]["phone"] is None


def test_validation():
    """Test input validation."""
    # Test invalid input type
    with pytest.raises(TypeError, match="Expected dict"):
        Address.from_dict("not a dict")

    # Test missing required field
    with pytest.raises(ValueError, match="Missing required field"):
        Address.from_dict({"city": "New York", "country": "USA"})

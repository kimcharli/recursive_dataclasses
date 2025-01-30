from typing import Optional, List, Dict
from dataclasses import dataclass
from recursive_dataclasses import RecursiveDataclass

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
    addresses: Dict[str, Address]  # Map of address type (e.g., 'home', 'work') to Address
    contacts: List[Contact]
    notes: Optional[str] = None

# Example usage
if __name__ == "__main__":
    # Create a nested dictionary
    person_data = {
        "name": "John Doe",
        "age": 30,
        "addresses": {
            "home": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA",
                "postal_code": "10001"
            },
            "work": {
                "street": "456 Business Ave",
                "city": "Manhattan",
                "country": "USA",
                "postal_code": "10002"
            }
        },
        "contacts": [
            {
                "email": "john@example.com",
                "phone": "+1-555-555-5555"
            },
            {
                "email": "john.doe@work.com"
            }
        ],
        "notes": "Prefers email communication"
    }

    # Load the dictionary into a Person instance
    person = Person.from_dict(person_data)
    print("\nLoaded Person instance:")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print("Addresses:")
    for addr_type, addr in person.addresses.items():
        print(f"  {addr_type.title()}: {addr.street}, {addr.city}")
    print(f"Contacts: {[contact.email for contact in person.contacts]}")
    print(f"Notes: {person.notes}")

    # Convert back to dictionary
    person_dict = person.to_dict()
    print("\nDumped dictionary:")
    print(person_dict)

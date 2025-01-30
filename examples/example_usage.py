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


def main():
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

    # Create a person with multiple addresses and occupation
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
    print("\nPerson's occupation:")
    print(person_dict["occupation"])

    # Create from dictionary
    new_person = Person.from_dict(person_dict)
    print("\nRecreated person's occupation:")
    print(f"Title: {new_person.occupation.title}")
    print(f"Company: {new_person.occupation.company}")
    print(f"Years Experience: {new_person.occupation.years_experience}")
    print(f"Department: {new_person.occupation.department}")


if __name__ == "__main__":
    main()

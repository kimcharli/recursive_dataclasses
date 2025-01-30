from dataclasses import dataclass, fields, is_dataclass, MISSING
from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    get_type_hints,
    Union,
    get_args,
    get_origin,
    ClassVar,
    cast,
)

T = TypeVar("T", bound="RecursiveDataclass")


@dataclass
class RecursiveDataclass:
    """A base class for dataclasses that can be recursively converted to/from dictionaries."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        result: Dict[str, Any] = {}
        type_hints = get_type_hints(self.__class__)

        for field in fields(self.__class__):  # type: ignore
            value = getattr(self, field.name)
            field_type = type_hints.get(field.name, Any)

            # Skip ClassVar fields
            if get_origin(field_type) is ClassVar:
                continue

            # Handle None values
            if value is None:
                result[field.name] = None
                continue

            # Handle Union/Optional types
            if get_origin(field_type) is Union:
                field_args = get_args(field_type)
                if type(None) in field_args:
                    # This is an Optional type
                    field_type = next(t for t in field_args if t is not type(None))

            # Handle nested dataclasses
            if is_dataclass(type(value)):
                if isinstance(value, RecursiveDataclass):
                    result[field.name] = value.to_dict()
                else:
                    result[field.name] = {k: v for k, v in value.__dict__.items()}

            # Handle dictionaries of dataclasses
            elif isinstance(value, dict):
                result[field.name] = {
                    k: v.to_dict()
                    if isinstance(v, RecursiveDataclass)
                    else {k2: v2 for k2, v2 in v.__dict__.items()}
                    if is_dataclass(type(v))
                    else v
                    for k, v in value.items()
                }

            # Handle lists/tuples of dataclasses
            elif isinstance(value, (list, tuple)):
                result[field.name] = [
                    v.to_dict()
                    if isinstance(v, RecursiveDataclass)
                    else {k: v2 for k, v2 in v.__dict__.items()}
                    if is_dataclass(type(v))
                    else v
                    for v in value
                ]

            # Handle basic types
            else:
                result[field.name] = value

        # Add type information
        result["__type__"] = self.__class__.__name__
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a new instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data)}")

        field_values: Dict[str, Any] = {}
        type_hints = get_type_hints(cls)

        for field in fields(cls):  # type: ignore
            if field.name not in data:
                if field.default is MISSING and field.default_factory is MISSING:  # type: ignore
                    raise ValueError(f"Missing required field {field.name}")
                continue

            value = data[field.name]
            if value is None:
                field_values[field.name] = None
                continue

            field_type = type_hints.get(field.name, Any)

            # Handle Union/Optional types
            if get_origin(field_type) is Union:
                field_args = get_args(field_type)
                if type(None) in field_args:
                    # This is an Optional type
                    field_type = next(t for t in field_args if t is not type(None))

            # Handle nested dataclasses
            if is_dataclass(field_type):
                field_type = cast(
                    Type[Any], field_type
                )  # Help mypy understand this is a type
                if issubclass(field_type, RecursiveDataclass):
                    field_values[field.name] = field_type.from_dict(value)
                else:
                    field_values[field.name] = field_type(**value)

            # Handle dictionaries
            elif get_origin(field_type) is dict:
                key_type, val_type = get_args(field_type)
                if is_dataclass(val_type):
                    val_type = cast(
                        Type[Any], val_type
                    )  # Help mypy understand this is a type
                    if issubclass(val_type, RecursiveDataclass):
                        field_values[field.name] = {
                            k: val_type.from_dict(v) for k, v in value.items()
                        }
                    else:
                        field_values[field.name] = {
                            k: val_type(**v) for k, v in value.items()
                        }
                else:
                    field_values[field.name] = value

            # Handle lists/tuples
            elif get_origin(field_type) in (list, tuple):
                item_type = get_args(field_type)[0]
                if is_dataclass(item_type):
                    item_type = cast(
                        Type[Any], item_type
                    )  # Help mypy understand this is a type
                    if issubclass(item_type, RecursiveDataclass):
                        field_values[field.name] = [
                            item_type.from_dict(item) for item in value
                        ]
                    else:
                        field_values[field.name] = [item_type(**item) for item in value]
                else:
                    field_values[field.name] = value

            # Handle basic types
            else:
                field_values[field.name] = value

        return cls(**field_values)

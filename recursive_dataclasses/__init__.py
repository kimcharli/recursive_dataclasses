from dataclasses import fields, is_dataclass
from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    get_type_hints,
    Mapping,
    Generic,
    List,
    TypeGuard,
    Protocol,
    cast,
    TypeAlias,
    runtime_checkable,
)
from typing_extensions import get_origin, get_args

T = TypeVar("T")


@runtime_checkable
class DataclassProtocol(Protocol):
    """Protocol for dataclass instances."""

    __dataclass_fields__: Dict[str, Any]


DataclassType: TypeAlias = Type[DataclassProtocol]
DataclassInstance: TypeAlias = DataclassProtocol


def is_dataclass_type(cls: Any) -> TypeGuard[DataclassType]:
    """Type guard to check if a class is a dataclass."""
    return isinstance(cls, type) and is_dataclass(cls)


def is_dataclass_instance(obj: Any) -> TypeGuard[DataclassInstance]:
    """Type guard to check if an object is a dataclass instance."""
    return is_dataclass(obj) and not isinstance(obj, type)


class DataclassUpdater(Generic[T]):
    """Helper class for updating dataclass instances."""

    @staticmethod
    def update(instance: T, data: Dict[str, Any]) -> T:
        """
        Recursively update a dataclass instance with values from a dictionary.

        Args:
            instance: A dataclass instance to update
            data: A dictionary containing the values to update with

        Returns:
            Updated dataclass instance
        """
        if not is_dataclass_instance(instance):
            raise TypeError("Instance must be a dataclass instance")
        if not isinstance(data, Mapping):
            raise TypeError("Data must be a mapping (dict-like object)")

        type_hints = get_type_hints(instance.__class__)

        for field in fields(instance):
            field_name = field.name
            if field_name not in data:
                continue

            field_value = data[field_name]
            field_type = type_hints[field_name]

            # Handle None values
            if field_value is None:
                setattr(instance, field_name, None)
                continue

            origin_type = get_origin(field_type) or field_type

            if is_dataclass_type(origin_type):
                # Handle nested dataclass
                if field_value is not None:
                    current_value = getattr(instance, field_name)
                    if current_value is None:
                        current_value = origin_type()
                    updated_value = DataclassUpdater[Any].update(
                        current_value, field_value
                    )
                    setattr(instance, field_name, updated_value)
                else:
                    setattr(instance, field_name, field_value)

            elif origin_type in (list, tuple, set):
                # Handle collections
                item_type = get_args(field_type)[0]
                if is_dataclass_type(item_type):
                    # Handle collection of dataclasses
                    current_items: List[Any] = []
                    for item in field_value:
                        if item is None:
                            current_items.append(None)
                        else:
                            new_instance = item_type()
                            updated_instance = DataclassUpdater[Any].update(
                                new_instance, item
                            )
                            current_items.append(updated_instance)
                    setattr(instance, field_name, origin_type(current_items))
                else:
                    # Handle collection of simple types
                    setattr(instance, field_name, origin_type(field_value))

            elif origin_type is dict:
                # Handle dictionaries
                key_type, value_type = get_args(field_type)
                if is_dataclass_type(value_type):
                    # Handle dict with dataclass values
                    current_dict: Dict[Any, Any] = {}
                    for k, v in field_value.items():
                        if v is None:
                            current_dict[k] = None
                        else:
                            new_instance = value_type()
                            updated_instance = DataclassUpdater[Any].update(
                                new_instance, v
                            )
                            current_dict[k] = updated_instance
                    setattr(instance, field_name, current_dict)
                else:
                    # Handle dict with simple types
                    setattr(instance, field_name, field_value)

            else:
                # Handle simple types
                setattr(instance, field_name, field_value)

        return instance


def update_dataclass(instance: T, data: Dict[str, Any]) -> T:
    """
    Recursively update a dataclass instance with values from a dictionary.

    Args:
        instance: A dataclass instance to update
        data: A dictionary containing the values to update with

    Returns:
        Updated dataclass instance
    """
    if not is_dataclass(instance):
        raise TypeError("Instance must be a dataclass")
    return cast(T, DataclassUpdater[Any].update(instance, data))


def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    """
    Create a new dataclass instance from a dictionary.

    Args:
        cls: The dataclass type to create
        data: A dictionary containing the values to create the dataclass with

    Returns:
        New dataclass instance
    """
    if not is_dataclass(cls):
        raise TypeError("Class must be a dataclass")

    instance = cls()
    return update_dataclass(instance, data)

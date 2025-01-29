from dataclasses import fields, is_dataclass
from typing import Any, Dict, Type, TypeVar, get_type_hints, Mapping, cast, Generic
from typing_extensions import get_origin, get_args

T = TypeVar("T")


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
        if not is_dataclass(instance):
            raise TypeError("Instance must be a dataclass")
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

            # Get the origin type (e.g., List from List[str])
            origin_type = get_origin(field_type) or field_type

            if is_dataclass(origin_type):
                # Handle nested dataclass
                current_value = getattr(instance, field_name)
                if current_value is None:
                    current_value = origin_type()
                if isinstance(field_value, dict):
                    updated_value = DataclassUpdater.update(current_value, field_value)
                    setattr(instance, field_name, updated_value)
                else:
                    setattr(instance, field_name, field_value)

            elif origin_type in (list, tuple, set):
                # Handle collections
                item_type = get_args(field_type)[0]
                if is_dataclass(item_type):
                    # Handle collection of dataclasses
                    new_value = []
                    for item in field_value:
                        if isinstance(item, dict):
                            new_item = item_type()
                            updated_item = DataclassUpdater.update(new_item, item)
                            new_value.append(updated_item)
                        else:
                            new_value.append(item)
                    setattr(instance, field_name, origin_type(new_value))
                else:
                    # Handle collection of simple types
                    setattr(instance, field_name, origin_type(field_value))

            elif origin_type is dict:
                # Handle dictionaries
                key_type, value_type = get_args(field_type)
                if is_dataclass(value_type):
                    # Handle dict with dataclass values
                    new_dict = {}
                    for k, v in field_value.items():
                        if isinstance(v, dict):
                            new_item = value_type()
                            updated_item = DataclassUpdater.update(new_item, v)
                            new_dict[k] = updated_item
                        else:
                            new_dict[k] = v
                    setattr(instance, field_name, new_dict)
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
    return DataclassUpdater.update(instance, data)


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

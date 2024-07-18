import inspect
from typing import Optional

from pydantic import (
    BaseModel,
    create_model
)


def optional(*fields):
    """
    Декоратор для маркировки полей необязательными
    """
    def dec(_cls):
        fields_dict = {}
        for field in fields:
            field_info = _cls.model_fields.get(field)
            if field_info is not None:
                fields_dict[field] = (Optional[field_info.annotation], None)

        OptionalModel = create_model(_cls.__name__, **fields_dict)
        OptionalModel.__module__ = _cls.__module__
        return OptionalModel

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.model_fields
        return dec(cls)
    return dec

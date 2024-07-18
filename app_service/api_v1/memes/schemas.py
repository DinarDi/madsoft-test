import re

from pydantic import (
    BaseModel,
    model_validator,
    ConfigDict,
    Field,
    field_validator,
)
from pydantic_core import from_json
from typing import Any
from fastapi import (
    HTTPException,
    status,
)

from utils import optional


class MemeBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=300)

    @field_validator('title')
    @classmethod
    def title_only_letters_and_num(cls, value):
        pattern = re.compile('^[a-z0-9]+$')
        if pattern.fullmatch(value) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    'error_message': 'Title must contain only a-z and 0-9'
                }
            )
        return value


class MemeWithImg(MemeBase):
    img_url: str


@optional
class MemeUpdate(MemeBase):
    pass


class MemeRequest(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def convert_to_dict(cls, data: Any):
        if isinstance(data, str):
            return from_json(data)
        return data


class MemeCreateRequest(MemeRequest, MemeBase):
    pass


class MemeUpdateRequest(MemeUpdate, MemeRequest):
    pass


class MemeResponse(MemeWithImg):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel):
    pass


class ApiMemeResponse(ApiResponse):
    data: MemeResponse


class ApiMemeListResponse(ApiResponse):
    page: int
    limit: int
    data: list[MemeResponse]


class ApiMemeCreateResponse(ApiResponse):
    data: MemeResponse


class ApiMemeUpdateResponse(ApiResponse):
    data: MemeResponse

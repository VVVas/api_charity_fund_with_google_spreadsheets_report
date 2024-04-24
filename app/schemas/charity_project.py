from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, NonNegativeInt, PositiveInt, validator
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description', 'full_amount')
    def cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя, описание или сумма не могут быть пустыми')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True

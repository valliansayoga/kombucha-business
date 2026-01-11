from pydantic import BaseModel, Field
from datetime import datetime


class FlavourCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    created_date: datetime = Field(default_factory=datetime.now)
    price: int = Field(..., gt=0)


class SalesCreate(BaseModel):
    transaction_date: datetime
    customer_id: int
    flavour_id: int

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    created_date: datetime = Field(default_factory=datetime.now)
    price: int = Field(..., gt=0)
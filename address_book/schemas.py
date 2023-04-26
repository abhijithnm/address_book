from pydantic import BaseModel


class AddressBook(BaseModel):
    """Schema will help with the validations for CRUD operations"""

    name: str
    email: str
    address_line1: str
    address_line2: str
    city: str
    pincode: int
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    name: str
    phone: str
    email: str


class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
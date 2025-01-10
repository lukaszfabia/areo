from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr

    # reads:


class UserResponse(UserBase):

    class Config:
        orm_mode = True

from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class OrderCreate(BaseModel):
    customer_name: str


class OrderUpdate(BaseModel):
    status: str
    version: int


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    version: int
    locked_by: str | None = None
    lock_expires_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
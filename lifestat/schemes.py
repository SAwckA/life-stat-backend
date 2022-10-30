from pydantic import BaseModel


class Message(BaseModel):
    message: str
    status_code: int = 0


class RegisterForm(BaseModel):
    username: str
    password: str

class LoginForm(BaseModel):
    username: str
    password: str

class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
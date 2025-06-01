from pydantic import BaseModel, EmailStr, Field, ValidationInfo, model_validator


class BaseFields(BaseModel):
    email: EmailStr = Field(description="User email", examples=["test_hillel_api_mailing@ukr.net"])
    name: str = Field(description="User nickname", examples=["Casper"])


class PasswordField(BaseModel):
    password: str = Field(min_length=8)

    @model_validator(mode="before")
    def validate_password(cls, values: dict, info: ValidationInfo) -> dict:
        password = (values.get("password") or "").strip()
        if not password:
            raise ValueError("Password required")

        if len(password) < 8:
            raise ValueError("Too short password")

        if " " in password:
            raise ValueError("No spaces in password, please")

        return values


class RegisterUserFields(BaseFields, PasswordField):
    pass


class BaseUserInfo(BaseFields):
    id: int

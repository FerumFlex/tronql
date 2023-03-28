import strawberry
from common.datatypes import User, UserInfo
from pydantic import BaseModel, EmailStr, SecretStr, validator


class LoginForm(BaseModel):
    email: EmailStr
    password: SecretStr


@strawberry.experimental.pydantic.input(model=LoginForm, all_fields=True)
class LoginFormInput:
    pass


class SignupForm(BaseModel):
    email: EmailStr
    password: SecretStr


@strawberry.experimental.pydantic.input(model=SignupForm, all_fields=True)
class SignupFormInput:
    pass


class SignupForm(BaseModel):
    email: EmailStr
    password: SecretStr

    @validator("password", always=True)
    def validate_password(cls, value):
        password = value.get_secret_value()
        min_length = 8

        errors = ""
        if len(password) < min_length:
            errors += "Password must be at least 8 characters long. "
        if not any(character.islower() for character in password):
            errors += "Password should contain at least one lowercase character."
        if errors:
            raise ValueError(errors)

        return value


@strawberry.experimental.pydantic.input(model=SignupForm, all_fields=True)
class SignupFormInput:
    pass


class ResendForm(BaseModel):
    email: EmailStr


@strawberry.experimental.pydantic.input(model=ResendForm, all_fields=True)
class ResendFormInput:
    pass


class VerifyForm(BaseModel):
    verification_id: str


@strawberry.experimental.pydantic.input(model=VerifyForm, all_fields=True)
class VerifyFormInput:
    pass


@strawberry.experimental.pydantic.type(model=UserInfo, all_fields=True)
class UserInfoResponse:
    pass


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserResponse:
    pass


class LoginInfo(BaseModel):
    token: str
    tokenExpirationInstant: str
    refreshToken: str
    user: User


@strawberry.experimental.pydantic.type(model=LoginInfo, all_fields=True)
class LoginInfoResponse:
    pass


class ResendVerifyEmail(BaseModel):
    email: EmailStr


@strawberry.experimental.pydantic.input(model=ResendVerifyEmail, all_fields=True)
class ResendVerifyEmailInput:
    pass


class SignupInfo(BaseModel):
    refreshToken: str
    token: str
    tokenExpirationInstant: str
    user: User


@strawberry.experimental.pydantic.type(model=SignupInfo, all_fields=True)
class SignupInfoResponse:
    pass


class VerifyEmailForm(BaseModel):
    verification_id: str


@strawberry.experimental.pydantic.input(model=VerifyEmailForm, all_fields=True)
class VerifyEmailFormInput:
    pass


class ForgotPasswordForm(BaseModel):
    email: EmailStr


@strawberry.experimental.pydantic.input(model=ForgotPasswordForm, all_fields=True)
class ForgotPasswordFormInput:
    pass


class ChangePasswordForm(BaseModel):
    change_id: str
    password: SecretStr


@strawberry.experimental.pydantic.input(model=ChangePasswordForm, all_fields=True)
class ChangePasswordFormInput:
    pass


class RefreshTokenForm(BaseModel):
    refresh_token: str


@strawberry.experimental.pydantic.input(model=RefreshTokenForm, all_fields=True)
class RefreshTokenFormInput:
    pass


class RefreshToken(BaseModel):
    refreshToken: str
    token: str


@strawberry.experimental.pydantic.type(model=RefreshToken, all_fields=True)
class RefreshTokenResponse:
    pass

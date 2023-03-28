import strawberry
from auth.config import settings
from auth.datatypes import (
    ChangePasswordFormInput,
    ForgotPasswordFormInput,
    LoginFormInput,
    LoginInfo,
    LoginInfoResponse,
    RefreshTokenFormInput,
    RefreshTokenResponse,
    ResendVerifyEmailInput,
    SignupFormInput,
    SignupInfoResponse,
    UserResponse,
    VerifyEmailFormInput,
)
from common.datatypes import User
from common.errors import ValidationError
from common.permissions import IsAuthenticated
from services.fusionauth import FusionAuthService
from strawberry.types import Info


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(info: Info) -> UserResponse:
        return UserResponse.from_pydantic(info.context.user)


@strawberry.type
class Mutation:
    @strawberry.mutation()
    async def login(self, form: LoginFormInput) -> LoginInfoResponse:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            login_data = await fusion.login(form.email, form.password)
            if not login_data:
                raise ValidationError("Email and password combination is not valid")

            login = LoginInfo.parse_obj(login_data)
            return login

    @strawberry.mutation()
    async def resend_verify_email(self, form: ResendVerifyEmailInput) -> bool:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            await fusion.resend_verify_email(form.email)
            return True

    @strawberry.mutation()
    async def signup(self, form: SignupFormInput) -> SignupInfoResponse:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            result = await fusion.signup(form.email, form.password)
            result.pop("registration")
            user = UserResponse.from_pydantic(User(**result.pop("user")))
            return SignupInfoResponse(user=user, **result)

    @strawberry.mutation()
    async def forgot_password(self, form: ForgotPasswordFormInput) -> bool:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            result = await fusion.forgot_password(form.email)
            if not result:
                raise ValidationError("Can not restore password")
            return True

    @strawberry.mutation()
    async def verify_email(self, form: VerifyEmailFormInput) -> bool:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            result = await fusion.verify_email(form.verification_id)
            if not result:
                raise ValidationError("Verification id is not found or already used.")
            return True

    @strawberry.mutation()
    async def change_password(self, form: ChangePasswordFormInput) -> bool:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            await fusion.change_password(form.change_id, form.password)
            return True

    @strawberry.mutation()
    async def refresh_token(self, form: RefreshTokenFormInput) -> RefreshTokenResponse:
        async with FusionAuthService(
            settings.fusion_api_url,
            settings.fusion_api_key,
            settings.fusion_app_id,
        ) as fusion:
            result = await fusion.refresh_token(form.refresh_token)
            return RefreshTokenResponse(
                refreshToken=result["refreshToken"],
                token=result["token"],
            )

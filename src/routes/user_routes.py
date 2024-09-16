from dependency_injector.wiring import Provide

from fastapi import APIRouter
from containers.users_di import UserDI
from routes.depends import get_service
from schemas.user_schemas import SignUpSchema, SignUpResponseSchema
from schemas.user_schemas import UserSchema
from services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/sign-up", response_model=SignUpResponseSchema)
async def sign_up(
        user_dta: SignUpSchema, service: UserService = get_service(Provide[UserDI.service])
):
    user = await service.create_user(user_dta)
    return SignUpResponseSchema.from_orm(user)


@user_router.get("/", response_model=list[UserSchema])
async def get_users(
        service: UserService = get_service(Provide[UserDI.service])
):
    users = await service.get_users()
    return [UserSchema.from_orm(user) for user in users]


@user_router.get("/{pk}", response_model=UserSchema)
async def get_user(
        pk: int, service: UserService = get_service(Provide[UserDI.service])
):
    user = await service.get_user(pk)
    return UserSchema.from_orm(user)

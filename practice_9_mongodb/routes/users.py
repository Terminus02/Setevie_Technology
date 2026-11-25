from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.users import User, UserCreate, UserSignIn


user_router = APIRouter(tags=["Users"])
user_database = Database(User)


# Регистрация нового пользователя
@user_router.post("/signup", status_code=201)
async def sign_user_up(user: UserCreate):
    existing_user = await User.find_one(User.email == user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )

    new_user = User(
        email=user.email,
        password=user.password,
        events=[]
    )

    await user_database.save(new_user)

    return {
        "message": "User created successfully"
    }


# Вход пользователя
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn):
    existing_user = await User.find_one(User.email == user.email)

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )

    if existing_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed."
        )

    return {
        "message": "User signed in successfully."
    }

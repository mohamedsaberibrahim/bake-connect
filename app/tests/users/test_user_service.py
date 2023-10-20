import pytest
from fastapi import HTTPException
from app.api.users.models import User
from app.api.users.services import UserService
from asyncmock import AsyncMock
from app.api.users.schemas import CreateUserSchema, UserRole


@pytest.fixture
def user_service():
    return UserService()


@pytest.mark.asyncio
async def test_create_user(user_service):
    # Test case: Create User
    payload = CreateUserSchema(
        email="test@example.com",
        password="123456",
        name="Test User",
        role=UserRole.MEMBER.value
    )

    user_service.user_dao.get_user_by_email = AsyncMock(return_value=None)
    user_service.user_dao.create_user_model = AsyncMock()
    user_service.auth_handler.get_password_hash = AsyncMock(
        return_value="hashed_password")

    result = await user_service.create_user(payload)

    assert isinstance(result, User)
    assert result.email == "test@example.com"

    # Case: Email already registered
    user_service.user_dao.get_user_by_email = AsyncMock(
        return_value=User(id=2, email="test@example.com"))

    with pytest.raises(HTTPException) as exc:
        await user_service.create_user(payload)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"


@pytest.mark.asyncio
async def test_get_user_profile(user_service):
    # Test case: Get User Profile
    user_id = 1

    user_service.user_dao.get_user_by_id = AsyncMock(
        return_value=User(id=user_id, email="test@example.com"))

    result = await user_service.get_user_profile(user_id)

    assert isinstance(result, User)
    assert result.id == user_id
    assert result.email == "test@example.com"

    # Case: User not found
    user_service.user_dao.get_user_by_id = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc:
        await user_service.get_user_profile(user_id)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

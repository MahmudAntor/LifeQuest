from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import uuid
import boto3

def get_user_router(dynamodb_client: boto3.resource):
    """
    User Management API Router 
    """
    router = APIRouter(prefix="/users", tags=["Users"])
    user_table = dynamodb_client.Table("LifeQuest_Users")

    class UserCreate(BaseModel):
        """
        Request model for creating a new user.
        """
        name: str = Field(..., example="John Doe")

    class UserResponse(UserCreate):
        """
        Response model for returning user details.
        """
        user_id: str = Field(..., example="550e8400-e29b-41d4-a716-446655440000")

    @router.get(
        "/",
        response_model=list[UserResponse],
        summary="Get all users",
        description="Retrieve a list of all registered users in the LifeQuest database.",
    )
    async def get_all_users():
        """
        Retrieve all users.
        """
        response = user_table.scan()
        users = response.get("Items", [])
        return [{"user_id": user["UserID"], "name": user["Name"]} for user in users]

    @router.post(
        "/",
        response_model=UserResponse,
        status_code=201,
        summary="Create a new user",
        description="Creates a new user and stores it in the database.",
    )
    async def create_user(user: UserCreate):
        """
        Create a new user.
        """
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        item = {
            "UserID": user_id,
            "Name": user.name,
            "Level": 1,
            "XP": 0
        }
        user_table.put_item(Item=item)
        return {"user_id": user_id, "name": user.name}

    @router.get(
        "/{user_id}",
        response_model=UserResponse,
        summary="Get user by ID",
        description="Retrieve user details using a unique user ID.",
    )
    async def get_user(user_id: str):
        """
        Retrieve user details by ID.
        """
        response = user_table.get_item(Key={"UserID": user_id})
        user = response.get("Item")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": user["UserID"], "name": user["Name"]}

    @router.delete(
        "/{user_id}",
        status_code=204,
        summary="Delete user by ID",
        description="Deletes a user from the database using a unique user ID.",
    )
    async def delete_user(user_id: str):
        """
        Delete a user by ID.
        """
        response = user_table.get_item(Key={"UserID": user_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_table.delete_item(Key={"UserID": user_id})

    return router
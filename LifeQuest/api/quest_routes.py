from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import uuid
import boto3

def get_quest_router(dynamodb_client: boto3.resource):
    """
    Quest Management API Router
    """
    router = APIRouter(prefix="/quests", tags=["Quests"])
    quest_table = dynamodb_client.Table("LifeQuest_Quests")

    class QuestCreate(BaseModel):
        """
        Request model for creating a new quest.
        """
        name: str = Field(..., example="Read a Book")
        description: str = Field(..., example="Read for 30 minutes")
        xp_reward: int = Field(..., example=50)

    class QuestResponse(QuestCreate):
        """
        Response model for returning quest details.
        """
        quest_id: str = Field(..., example="3fa85f64-5717-4562-b3fc-2c963f66afa6")

    @router.get(
        "/",
        response_model=list[QuestResponse],
        summary="Get all quests",
        description="Retrieve a list of all available quests in LifeQuest.",
    )
    async def get_all_quests():
        """
        Fetches all quests from the database.
        """
        response = quest_table.scan()
        quests = response.get("Items", [])
        return [{"quest_id": quest["QuestID"], "name": quest["Name"], "description": quest["Description"], "xp_reward": quest["XP_Reward"]} for quest in quests]

    @router.post(
        "/",
        response_model=QuestResponse,
        status_code=201,
        summary="Create a new quest",
        description="Creates a new quest and stores it in the database.",
    )
    async def create_quest(quest: QuestCreate):
        """
        Creates a new quest in the database.
        """
        quest_id = str(uuid.uuid4())  
        item = {
            "QuestID": quest_id,
            "Name": quest.name,
            "Description": quest.description,
            "XP_Reward": quest.xp_reward
        }
        quest_table.put_item(Item=item)
        return {"quest_id": quest_id, "name": quest.name, "description": quest.description, "xp_reward": quest.xp_reward}

    @router.get(
        "/{quest_id}",
        response_model=QuestResponse,
        summary="Get quest by ID",
        description="Retrieve quest details using a unique quest ID.",
    )
    async def get_quest(quest_id: str):
        """
        Fetches quest details using its ID.
        """
        response = quest_table.get_item(Key={"QuestID": quest_id})
        quest = response.get("Item")
        if not quest:
            raise HTTPException(status_code=404, detail="Quest not found")
        return {"quest_id": quest["QuestID"], "name": quest["Name"], "description": quest["Description"], "xp_reward": quest["XP_Reward"]}

    return router
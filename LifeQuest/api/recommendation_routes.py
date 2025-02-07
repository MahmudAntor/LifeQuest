import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import boto3
from utils.dynamodb_client import DynamoDBClient
from config import Config
from ml.task_recommendation import TaskRecommendationService

def get_recommendation_router(dynamodb_client: boto3.resource) -> APIRouter:
    """
    AI Task Recommendation API Router
    Generates personalized quest/task recommendations using OpenRouter's DeepSeek model.
    """
    router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
    user_table = dynamodb_client.Table("LifeQuest_Users")
    quest_table = dynamodb_client.Table("LifeQuest_UserQuests")
    task_recommender = TaskRecommendationService()

    class RecommendationRequest(BaseModel):
        """
        Request model for task recommendations.
        """
        user_id: str

    class RecommendationResponse(BaseModel):
        """
        Response model for task recommendations.
        """
        recommendations: List[str]

    @router.post(
        "/",
        response_model=RecommendationResponse,
        summary="Get AI-powered task recommendations",
        description="Fetch personalized task suggestions using OpenRouter's DeepSeek model based on user progress."
    )
    async def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
        """
        Generate task recommendations for a given user.
        """
        # Retrieve user data
        response = user_table.get_item(Key={"UserID": request.user_id})
        user = response.get("Item")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Retrieve completed tasks
        completed_tasks = []
        quest_response = quest_table.scan()
        for quest in quest_response.get("Items", []):
            if quest["UserID"] == request.user_id and quest.get("Status") == "Completed":
                completed_tasks.append(quest["QuestID"])

        # Prepare player data for task recommendation
        player_data = {
            "level": user["Level"],
            "xp": user["XP"],
            "completed_tasks": completed_tasks
        }

        # Fetch task recommendations
        try:
            recommendations = task_recommender.recommend_tasks(player_data)
            return RecommendationResponse(recommendations=recommendations)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")

    return router
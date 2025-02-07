from fastapi import FastAPI
from api.user_routes import get_user_router
from api.quest_routes import get_quest_router
from api.recommendation_routes import get_recommendation_router
from utils.dynamodb_client import DynamoDBClient

app = FastAPI(
    title="LifeQuest API",
    version="1.0",
    description="""
LifeQuest API allows users to manage quests, track progress, and receive AI-powered task recommendations.

## Features:
- 🧑‍🎓 **User Management**: Create, retrieve, and delete users.
- 🎯 **Quest Management**: Add, retrieve, and manage quests.
- 🔮 **AI-Powered Task Recommendations**: Get personalized quest suggestions.

📌 **Use the `/docs` or `/redoc` endpoints for API documentation!**
""",
)

# Initialize a single DynamoDB client
dynamodb_client = DynamoDBClient("configs/aws_config.ini").get_client()

# Register routers with shared DynamoDB client
app.include_router(get_user_router(dynamodb_client))
app.include_router(get_quest_router(dynamodb_client))
app.include_router(get_recommendation_router(dynamodb_client))

@app.get("/")
def root():
    return {"message": "Welcome to the LifeQuest API!"}
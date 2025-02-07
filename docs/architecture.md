# LifeQuest Architecture

## Current Module Structure

1. **Player Module (`player/player.py`)**
   - Manages player attributes such as name, level, XP, and interaction with quests.
   - Saves and loads player data from DynamoDB using the `User` model.

2. **Quest Manager Module (`Quest/quest_manager.py`)**
   - Handles all quest-related operations including retrieving, adding, and assigning quests.
   - Uses `Quest` and `UserQuest` models for persistent storage.

3. **Quest Models**
   - **`models/quest.py`**: Represents global quest data like `name`, `description`, and `XP reward`.
   - **`models/user_quest.py`**: Tracks user-specific quest progress (e.g., status, completion).

4. **API Layer (FastAPI)**
   - **`api/api.py`**: Initializes FastAPI, registers routers, and shares a global DynamoDB client.
   - **`api/user_routes.py`**: Handles user-related API requests (create, retrieve, delete).
   - **`api/quest_routes.py`**: Manages quests (create, retrieve, list).
   - **`api/recommendation_routes.py`**: Provides AI-powered task recommendations.

5. **AI Task Recommendation Module (`ml/task_recommendation.py`)**
   - Interacts with the LLM API to fetch personalized task recommendations based on user progress.

6. **Configuration**
   - **`config.py`**: Contains configuration settings for the application.
   - **`configs/aws_config.ini`**: Stores AWS credentials and configuration.

7. **Database Integration**
   - AWS DynamoDB is used for persistent storage of player data, quest definitions, and user-specific quest progress.
   - The **DynamoDB client is initialized once in `api/api.py`** and shared across route handlers.

8. **Utilities (`utils`)**
   - Contains utility functions and classes, such as the `DynamoDBClient` for managing DynamoDB connections.

9. **Main Entry Point (`main.py`)**
   - The main entry point of the application, responsible for starting the FastAPI server.

10. **Testing (`tests`)**
    - Contains test cases for the application to ensure functionality and reliability.

## Interaction Flow
Player ---> QuestManager ---> (Quest Definitions & User Quests)  
FastAPI ---> DynamoDB ---> (Persistent Data Storage)  
FastAPI ---> TaskRecommendationService ---> LLM API (AI Task Recommendations)
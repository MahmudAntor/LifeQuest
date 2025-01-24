# LifeQuest Architecture

## Current Module Structure

1. **Player Module (`player.py`)**
   - Manages player attributes such as name, level, XP, and interaction with quests.
   - Saves and loads player data from DynamoDB using the `User` model.

2. **Quest Manager Module (`quest_manager.py`)**
   - Handles all quest-related operations including retrieving, adding, and assigning quests.
   - Uses `Quest` and `UserQuest` models for persistent storage.

3. **Quest Models**
   - **`quest.py`**: Represents global quest data like `name`, `description`, and `XP reward`.
   - **`user_quest.py`**: Tracks user-specific quest progress (e.g., status, completion).

4. **Database Integration**
   - AWS DynamoDB is used for persistent storage of player data, quest definitions, and user-specific quest progress.

## Interaction Flow
Player ---> QuestManager ---> (Quest Definitions & User Quests)

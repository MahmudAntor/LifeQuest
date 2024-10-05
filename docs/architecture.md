# LifeQuest Architecture

## Current Module Structure

1. **Player Module (`player.py`)**
   - Manages player attributes such as name, level, XP, and interaction with quests.

2. **Quest Manager Module (`quest_manager.py`)**
   - Handles all quest-related operations including retrieving, adding, and removing quests.

3. **Daily Quest Module (`daily_quest.py`)**
   - Represents individual quests with properties like `name`, `description`, `XP`, and completion status.

## Interaction Flow
Player ---> QuestManager ---> (Base Daily Quests & Custom Quests)

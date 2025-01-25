from player.player import Player
from Quest.quest_manager import QuestManager
from utils.dynamodb_client import DynamoDBClient
from ml.task_recommendation import TaskRecommendationService

# Initialize the DynamoDB client
dynamo_client = DynamoDBClient("./configs/aws_config.ini").get_client()

# Initialize the Quest Manager and Task Recommendation Service
quest_manager = QuestManager()
task_recommender = TaskRecommendationService()

# Sample player and quest data
PLAYER_ID = "123"
PLAYER_NAME = "Hero"
QUEST_ID = "Q001"

def add_sample_quest():
    """
    Add a sample quest to the database.
    """
    quest_manager.add_custom_quest(
        quest_id=QUEST_ID,
        name="Read a book for 10 minutes",
        description="Improve your knowledge by reading for 10 minutes.",
        xp_reward=50
    )
    print("Sample quest added to the database.")

def assign_quest_to_player():
    """
    Assign a quest to a player.
    """
    player = Player(user_id=PLAYER_ID, name=PLAYER_NAME)
    quest_manager.assign_quest_to_user(user_id=PLAYER_ID, quest_id=QUEST_ID)
    print(f"Quest {QUEST_ID} assigned to player {PLAYER_NAME}.")

def display_player_stats():
    """
    Display the player's stats and quests.
    """
    player = Player.load(user_id=PLAYER_ID)
    if player:
        print("\n--- Player Stats ---")
        player.display_stats()
        print("\n--- Player Quests ---")
        player.show_all_quests()
    else:
        print("Player not found in the database.")

def complete_quest():
    """
    Mark a quest as completed and update the player's progress.
    """
    player = Player.load(user_id=PLAYER_ID)
    if player:
        print("\n--- Completing the Quest ---")
        player.complete_quest(QUEST_ID)
        player.save()
        print("Quest completed and progress saved.")
    else:
        print("Player not found. Cannot complete quest.")

def fetch_task_recommendations():
    """
    Fetch task recommendations for the player using the LLM API.
    """
    player = Player.load(user_id=PLAYER_ID)
    if player:
        print("\n--- Fetching Task Recommendations ---")
        player_data = {
            "level": player.level,
            "xp": player.xp,
            "completed_tasks": [
                quest.name for quest in quest_manager.get_user_quests(user_id=PLAYER_ID) if quest.status == "Completed"
            ]
        }
        print("Player Data:")
        print(player_data)
        recommendations = task_recommender.recommend_tasks(player_data)
        if recommendations:
            print("Recommended Tasks:")
            for task in recommendations:
                print(f"- {task}")
        else:
            print("No recommendations available at this time.")
    else:
        print("Player not found. Cannot fetch recommendations.")

def main():
    """
    Main menu to choose a task to execute.
    """
    tasks = {
        "1": ("Add a sample quest", add_sample_quest),
        "2": ("Assign a quest to the player", assign_quest_to_player),
        "3": ("Display player stats and quests", display_player_stats),
        "4": ("Complete a quest", complete_quest),
        "5": ("Fetch task recommendations", fetch_task_recommendations),
    }

    print("\n--- LifeQuest Task Menu ---")
    for key, (desc, _) in tasks.items():
        print(f"{key}. {desc}")
    
    choice = input("\nEnter the number of the task you want to execute: ")
    task = tasks.get(choice)
    if task:
        print(f"\n--- Executing: {task[0]} ---")
        task[1]()  # Execute the selected task
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

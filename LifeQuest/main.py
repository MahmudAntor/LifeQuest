from player.player import Player
from Quest.quest_manager import QuestManager
from utils.dynamodb_client import DynamoDBClient

# Initialize the DynamoDB client
dynamo_client = DynamoDBClient("./configs/aws_config.ini").get_client()

# Create a quest manager
quest_manager = QuestManager()

# Add a sample quest
quest_id = "Q001"
quest_manager.add_custom_quest(
    quest_id=quest_id,
    name="Read a book for 10 minutes",
    description="Improve your knowledge by reading for 10 minutes.",
    xp_reward=50
)

# Create a player and assign the quest
player = Player(user_id="123", name="Hero")
quest_manager.assign_quest_to_user(user_id="123", quest_id=quest_id)

# Show player's initial stats and assigned quests
print("\n--- Player Initial Stats ---")
player.display_stats()
print("\n--- Player Quests ---")
player.show_all_quests()

# Complete the quest
print("\n--- Completing the Quest ---")
player.complete_quest(quest_id)

# Show updated player stats and quests
print("\n--- Updated Player Stats ---")
player.display_stats()

# Save the player's progress to DynamoDB
player.save()

# Load the player from DynamoDB
loaded_player = Player.load(user_id="123")
if loaded_player:
    print("\n--- Loaded Player from Database ---")
    loaded_player.display_stats()
else:
    print("Player not found in the database.")

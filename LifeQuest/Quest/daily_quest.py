from models.quest import Quest
from models.user_quest import UserQuest


class DailyQuest:
    """
    Represents a daily quest in LifeQuest.
    """
    def __init__(self, quest_id, name, description, xp_reward, user_id=None):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.xp_reward = xp_reward
        self.user_id = user_id  # Optional, for user-specific operations

    def complete_quest(self):
        """
        Completes the quest for the user and returns the XP gained.
        """
        if self.user_id:
            # Update the quest's status in UserQuest
            UserQuest.update_status(self.user_id, self.quest_id, status="Completed")
            return self.xp_reward
        raise ValueError("User ID is required to complete a quest.")

    @classmethod
    def load(cls, quest_id, user_id=None):
        """
        Loads quest details from the Quest model and optionally tracks user-specific progress.
        """
        quest_data = Quest.get(quest_id)
        if quest_data:
            return cls(
                quest_id=quest_data['QuestID'],
                name=quest_data['Name'],
                description=quest_data['Description'],
                xp_reward=quest_data['XP_Reward'],
                user_id=user_id
            )
        return None

from models.quest import Quest
from models.user_quest import UserQuest
from Quest.daily_quest import DailyQuest


class QuestManager:
    """
    Manages quests for LifeQuest.
    """

    def add_custom_quest(self, quest_id, name, description, xp_reward):
        """
        Adds a new quest to the Quest model.
        """
        quest = Quest(quest_id=quest_id, name=name, description=description, xp_reward=xp_reward)
        quest.save()

    def assign_quest_to_user(self, user_id, quest_id):
        """
        Assigns a quest to a user by adding an entry in UserQuest.
        """
        quest_data = Quest.get(quest_id)
        if quest_data:
            user_quest = UserQuest(user_id=user_id, quest_id=quest_id, status="In Progress")
            user_quest.save()
        else:
            print(f"Quest with ID {quest_id} not found.")

    def get_user_quests(self, user_id):
        """
        Retrieves all quests assigned to a user with progress information.
        """
        user_quests = UserQuest.get_all_for_user(user_id)
        quests = []
        for user_quest in user_quests:
            quest = Quest.get(user_quest['QuestID'])
            if quest:
                quests.append(DailyQuest(
                    quest_id=quest['QuestID'],
                    name=quest['Name'],
                    description=quest['Description'],
                    xp_reward=quest['XP_Reward'],
                    user_id=user_id
                ))
        return quests

    def get_all_quests(self):
        """
        Retrieves all available quests from the Quest model.
        """
        quests = Quest.get_all()  # Add this method in Quest model
        return [DailyQuest(
            quest_id=quest['QuestID'],
            name=quest['Name'],
            description=quest['Description'],
            xp_reward=quest['XP_Reward']
        ) for quest in quests]

    def complete_user_quest(self, user_id, quest_id):
        """
        Marks a quest as completed for a user and returns the XP gained.
        """
        user_quest = UserQuest.get(user_id, quest_id)
        if user_quest and user_quest['Status'] != "Completed":
            # Update the quest's status in UserQuest
            UserQuest.update_status(user_id, quest_id, status="Completed")
            
            # Fetch the quest's XP reward
            quest = Quest.get(quest_id)
            if quest:
                return quest['XP_Reward']
        return 0

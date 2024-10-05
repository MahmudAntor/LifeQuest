from Quest.daily_quest import DailyQuest

class QuestManager:
    """
    QuestManager class handles creation, management, and retrieval of daily and custom quests.
    Attributes:
        base_daily_quests (list): A predefined list of daily quests for the player.
        custom_quests (list): A list to store custom quests created by the player.
    Methods:
        add_custom_quest(name, description, xp_reward): Adds a new custom quest to the list.
        get_base_daily_quests(): Returns a list of base daily quests.
        get_custom_quests(): Returns a list of all custom quests.
        get_all_quests(): Returns a combined list of base daily quests and custom quests.
        remove_quest(name): Removes a custom quest by name.
    """
    def __init__(self):
        # Initialize the base daily quests when the QuestManager is created.
        self.base_daily_quests = [
            DailyQuest("Read a book for 10 minutes", "Improve knowledge and reduce stress.", 50),
            DailyQuest("Do 5 push-ups", "Boost physical health and energy.", 30),
            DailyQuest("Meditate for 5 minutes", "Enhance mental clarity and reduce stress.", 40),
            DailyQuest("Take a 10-minute walk", "Improve mood and health.", 30),
            DailyQuest("Write in a journal for 5 minutes", "Reflect and improve self-awareness.", 40)
        ]
        self.custom_quests = []

    def get_base_daily_quests(self):
        """Returns a list of base daily quests."""
        return self.base_daily_quests

    def add_custom_quest(self, name, description, xp_reward):
        """Adds a new custom quest to the custom quest list."""
        new_quest = DailyQuest(name, description, xp_reward)
        self.custom_quests.append(new_quest)
        print(f"Custom quest '{name}' added with {xp_reward} XP reward.")

    def get_custom_quests(self):
        """Returns a list of all custom quests."""
        return self.custom_quests

    def get_all_quests(self):
        """Returns a combined list of all base daily quests and custom quests."""
        return self.base_daily_quests + self.custom_quests

    def remove_quest(self, name):
        """Removes a custom quest by name if it exists."""
        for quest in self.custom_quests:
            if quest.name.lower() == name.lower():
                self.custom_quests.remove(quest)
                print(f"Custom quest '{name}' removed.")
                return
        print(f"Custom quest '{name}' not found.")
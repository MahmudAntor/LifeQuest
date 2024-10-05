from Quest.quest_manager import QuestManager

class Player:
    """
    Represents a player in LifeQuest with XP tracking and quest management.
    Attributes:
        name (str): The name of the player.
        level (int): The level of the player.
        xp (int): The experience points of the player.
        quest_manager (QuestManager): Manages both base and custom quests.
    Methods:
        display_stats(): Displays the player's stats.
        gain_xp(amount): Adds XP to the player and handles level-up logic.
        show_all_quests(): Displays the list of all quests.
        complete_quest(quest_name): Completes a quest by name and returns XP gained.
        add_custom_quest(): Adds a custom quest using the QuestManager.
    """
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.quest_manager = QuestManager()  # Initialize QuestManager

    def display_stats(self):
        """Displays the player's current stats."""
        stats = f"""
        Player Stats:
        ------------
        Name: {self.name}
        Level: {self.level}
        XP: {self.xp}
        Total Quests Completed: {self.total_quests_completed()}
        """
        print(stats)

    def gain_xp(self, amount):
        """Adds XP to the player and handles leveling up if necessary."""
        self.xp += amount
        self._check_level_up()

    def _check_level_up(self):
        """Private method to check if the player has enough XP to level up."""
        xp_threshold = self.level * 100  # Example: level up every 100 * level XP
        if self.xp >= xp_threshold:
            self.level += 1
            self.xp -= xp_threshold  # Subtract the XP threshold from the current XP
            print(f"{self.name} has leveled up! Now at level {self.level}.")

    def total_quests_completed(self):
        """Calculates total completed quests."""
        return len([quest for quest in self.quest_manager.get_all_quests() if quest.completed])

    def show_all_quests(self):
        """Displays the list of all quests (base daily and custom) and their status."""
        print("\nAll Quests:")
        print("-----------")
        for quest in self.quest_manager.get_all_quests():
            print(quest)

    def complete_quest(self, quest_name):
        """Completes a quest by name and returns the XP gained."""
        for quest in self.quest_manager.get_all_quests():
            if quest.name.lower() == quest_name.lower() and not quest.completed:
                xp_gained = quest.complete_quest()
                print(f"Quest '{quest.name}' completed! Gained {xp_gained} XP.")
                self.gain_xp(xp_gained)
                return xp_gained
        print(f"Quest '{quest_name}' not found or already completed.")
        return 0

    def add_custom_quest(self, name, description, xp_reward):
        """Adds a new custom quest through QuestManager."""
        self.quest_manager.add_custom_quest(name, description, xp_reward)
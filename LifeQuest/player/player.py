from Quest.quest_manager import QuestManager
from models.user import User
from models.user_quest import UserQuest


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
        complete_quest(quest_id): Completes a quest by ID and returns XP gained.
        add_custom_quest(): Adds a custom quest using the QuestManager.
        save(): Saves the player data using the User model.
        load(user_id): Loads a player from the database using the User model.
    """

    def __init__(self, user_id, name, level=1, xp=0):
        self.user_id = user_id
        self.name = name
        self.level = level
        self.xp = xp
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
        user_quests = UserQuest.get_all_for_user(self.user_id)
        return len([quest for quest in user_quests if quest['Status'] == "Completed"])

    def show_all_quests(self):
        """Displays the list of all quests (base daily and custom) and their status."""
        print("\nAll Quests:")
        print("-----------")
        user_quests = self.quest_manager.get_user_quests(self.user_id)
        for quest in user_quests:
            print(f"{quest.name}: {quest.description} (XP: {quest.xp_reward})")

    def complete_quest(self, quest_id):
        """Completes a quest by ID and returns the XP gained."""
        user_quest = UserQuest.get(self.user_id, quest_id)
        if user_quest and user_quest['Status'] != "Completed":
            xp_gained = self.quest_manager.complete_user_quest(self.user_id, quest_id)
            self.gain_xp(xp_gained)
            self.save()  # Save the updated player state
            print(f"Quest '{quest_id}' completed! Gained {xp_gained} XP.")
            return xp_gained
        print(f"Quest '{quest_id}' not found or already completed.")
        return 0

    def add_custom_quest(self, quest_id, name, description, xp_reward):
        """Adds a new custom quest through QuestManager."""
        self.quest_manager.add_custom_quest(quest_id, name, description, xp_reward)

    def save(self):
        """Saves the player data to the database using the User model."""
        user = User(user_id=self.user_id, name=self.name, level=self.level, xp=self.xp)
        user.save()

    @classmethod
    def load(cls, user_id):
        """Loads a player from the database using the User model."""
        user_data = User.get(user_id)
        if user_data:
            return cls(
                user_id=user_data['UserID'],
                name=user_data['Name'],
                level=user_data['Level'],
                xp=user_data['XP']
            )
        print(f"Player with ID '{user_id}' not found in the database.")
        return None

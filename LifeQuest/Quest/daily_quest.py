class DailyQuest:
    """
    Represents a single daily quest for the player to complete.
    Attributes:
        name (str): The name of the quest (e.g., 'Read a book for 10 minutes').
        description (str): A brief description of the quest.
        xp_reward (int): The amount of XP awarded for completing the quest.
        completed (bool): Whether the quest has been completed.
    """
    def __init__(self, name, description, xp_reward):
        self.name = name
        self.description = description
        self.xp_reward = xp_reward
        self.completed = False

    def complete_quest(self):
        """Mark the quest as completed."""
        self.completed = True
        return self.xp_reward

    def __repr__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Quest: {self.name}, XP: {self.xp_reward}, Status: {status}"

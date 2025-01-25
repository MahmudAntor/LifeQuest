import requests
from config import Config

class TaskRecommendationService:
    """
    A service to interact with the LLM API for task recommendations.
    """

    def __init__(self):
        self.api_url = Config.LLM_API_URL
        self.api_key = Config.LLM_API_KEY
        self.model = Config.LLM_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def recommend_tasks(self, player_data):
        """
        Fetch task recommendations from the LLM API.

        :param player_data: Dictionary containing player stats and completed quests.
        :return: List of recommended tasks or an error message.
        """
        messages = self._create_messages(player_data)
        payload = {
            "model": self.model,
            "messages": messages,
        }

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=payload
            )
            response.raise_for_status()
            completion = response.json()
            return completion.get("choices", [])[0].get("message", {}).get("content", "").strip().split("\n")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the LLM API: {e}")
            return []

    def _create_messages(self, player_data):
        """
        Generate messages for the LLM based on player data.

        :param player_data: Dictionary containing player stats and completed quests.
        :return: A list of message dictionaries for the model.
        """
        player_stats = f"Player level: {player_data['level']}, XP: {player_data['xp']}."
        completed_tasks = f"Completed tasks: {', '.join(player_data['completed_tasks'])}."
        user_content = f"{player_stats} {completed_tasks} Suggest three new tasks for the player:"
        return [{"role": "user", "content": user_content}]

from utils.dynamodb_client import DynamoDBClient

class Quest:
    def __init__(self, quest_id, name, description, xp_reward):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.xp_reward = xp_reward
        self.table = DynamoDBClient().get_client().Table('LifeQuest_Quests')

    def save(self):
        """
        Save a quest to the DynamoDB table.
        """
        self.table.put_item(Item={
            'QuestID': self.quest_id,
            'Name': self.name,
            'Description': self.description,
            'XP_Reward': self.xp_reward
        })

    @classmethod
    def get(cls, quest_id):
        """
        Retrieve a quest by QuestID.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_Quests')
        response = table.get_item(Key={'QuestID': quest_id})
        return response.get('Item')

    @classmethod
    def get_all(cls):
        """
        Retrieve all quests from the DynamoDB table.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_Quests')
        response = table.scan()
        return response.get('Items', [])

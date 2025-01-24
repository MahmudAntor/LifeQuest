from utils.dynamodb_client import DynamoDBClient

class User:
    def __init__(self, user_id, name, level=0, xp=0):
        self.user_id = user_id
        self.name = name
        self.level = level
        self.xp = xp
        self.table = DynamoDBClient().get_client().Table('LifeQuest_Users')

    def save(self):
        """
        Save a user to the DynamoDB table.
        """
        self.table.put_item(Item={
            'UserID': self.user_id,
            'Name': self.name,
            'Level': self.level,
            'XP': self.xp
        })

    @classmethod
    def get(cls, user_id):
        """
        Retrieve a user by UserID.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_Users')
        response = table.get_item(Key={'UserID': user_id})
        return response.get('Item')

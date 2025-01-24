import boto3
from utils.dynamodb_client import DynamoDBClient
from datetime import datetime

class UserQuest:
    def __init__(self, user_id, quest_id, status="In Progress", date_completed=None):
        """
        Represents a user's quest tracking information.
        """
        self.user_id = user_id
        self.quest_id = quest_id
        self.status = status
        self.date_completed = date_completed
        self.table = DynamoDBClient().get_client().Table('LifeQuest_UserQuests')

    def save(self):
        """
        Save a user-quest relationship to the DynamoDB table.
        """
        item = {
            'UserID': self.user_id,
            'QuestID': self.quest_id,
            'Status': self.status
        }
        if self.date_completed:
            item['DateCompleted'] = self.date_completed
        self.table.put_item(Item=item)

    @classmethod
    def get(cls, user_id, quest_id):
        """
        Retrieve a user-quest relationship by UserID and QuestID.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_UserQuests')
        response = table.get_item(Key={'UserID': user_id, 'QuestID': quest_id})
        return response.get('Item')

    @classmethod
    def get_all_for_user(cls, user_id):
        """
        Retrieve all quests assigned to a specific user.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_UserQuests')
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('UserID').eq(user_id)
        )
        return response.get('Items', [])

    @classmethod
    def update_status(cls, user_id, quest_id, status):
        """
        Update the status of a specific user-quest relationship.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_UserQuests')
        update_expression = "SET #s = :status"
        expression_values = {":status": status}
        expression_names = {"#s": "Status"}

        if status == "Completed":
            update_expression += ", DateCompleted = :date_completed"
            expression_values[":date_completed"] = datetime.now().isoformat()

        table.update_item(
            Key={'UserID': user_id, 'QuestID': quest_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )

    @classmethod
    def delete(cls, user_id, quest_id):
        """
        Delete a specific user-quest relationship.
        """
        table = DynamoDBClient().get_client().Table('LifeQuest_UserQuests')
        table.delete_item(Key={'UserID': user_id, 'QuestID': quest_id})

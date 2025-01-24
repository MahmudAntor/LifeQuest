import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError
import configparser
import os
from threading import Lock

class DynamoDBClient:
    """
    Singleton class to manage a single instance of the DynamoDB client.
    """
    _instance = None
    _lock = Lock()  # Ensures thread-safe singleton instantiation

    def __new__(cls, config_path="aws_config.ini"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(config_path)
        return cls._instance

    def _initialize(self, config_path):
        """
        Initializes the DynamoDB client using credentials from a configuration file.
        """
        try:
            # Check if the config file exists
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found at {config_path}")
            
            # Read the configuration file
            config = configparser.ConfigParser()
            config.read(config_path)
            
            # Extract AWS credentials and region
            aws_access_key_id = config.get("aws", "aws_access_key_id")
            aws_secret_access_key = config.get("aws", "aws_secret_access_key")
            region_name = config.get("aws", "region_name")
            
            # Initialize the session with credentials
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
            
            # Initialize DynamoDB resource
            self.dynamodb = session.resource('dynamodb', region_name=region_name)

        except FileNotFoundError as e:
            print(f"Configuration file error: {e}")
        except (NoCredentialsError, PartialCredentialsError):
            print("AWS credentials not found or incomplete. Check your configuration.")
        except EndpointConnectionError as e:
            print(f"Could not connect to the DynamoDB endpoint: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.dynamodb = None

    def get_client(self):
        """
        Returns the DynamoDB client resource.
        """
        return self.dynamodb

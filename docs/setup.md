## ⚙️ Setup Instructions

### Prerequisites
1. Install **Python 3.8 or higher**.
2. Set up AWS credentials with access to DynamoDB:
   - use the `aws_config.ini` file as described below.

### Configuration
1. Create a configuration file named `aws_config.ini` in the configs folder:
   ```ini
   [aws]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   region_name = YOUR_REGION
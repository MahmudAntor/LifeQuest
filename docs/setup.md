# ⚙️ Setup Instructions

## Prerequisites

1. Install **Python 3.13 or higher**.
2. Set up AWS credentials with access to DynamoDB:
   - Use the `aws_config.ini` file as described below.

## Configuration

1. Create a configuration file named `aws_config.ini` in the `configs` folder:
   ```ini
   [aws]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   region_name = YOUR_REGION
   ```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/MahmudAntor/LifeQuest.git
   ```
2. Navigate to the project directory:
   ```sh
   cd LifeQuest
   ```
3. Create a virtual environment:

   ```sh
   python -m venv env
   ```
4. Activate environment

   ```sh
   source env/bin/activate
   ```
5. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server::
   ```sh
   uvicorn LifeQuest.api.api:app --reload
   ```
2. Access the API documentation at: 
Swagger UI: Localhost/docs
ReDoc: localhost/redoc


## Troubleshooting

- Ensure your AWS credentials are correctly set up in the `aws_config.ini` file.



from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debugging print statement
print("Loaded Environment Variables:")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"ENV_FOLDER: {os.getenv('ENV_FOLDER')}")

from study import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
import os
from dotenv import load_dotenv

# --- NEW: Explicitly load the .env file at the very start ---
# Construct the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# Load it
load_dotenv(dotenv_path=dotenv_path)

# Now import the app creator
from app import create_app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # For development, it's highly recommended to run in debug mode.
    # It gives better error pages and auto-reloads when you save a file.
    app.run(debug=True)
import os

# No need for load_dotenv here anymore
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration variables from environment variables."""

    # General Config - These are loaded from the .env file by run.py
    SECRET_KEY = os.environ.get('SECRET_KEY')
    COQUI_TOS_AGREED = os.environ.get('COQUI_TOS_AGREED') # Make sure it's read
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    FLASK_APP = 'run.py'
    FLASK_ENV = 'development'
    
    # Database Config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Config
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    GENERATED_FOLDER = os.path.join(basedir, 'generated_audio')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
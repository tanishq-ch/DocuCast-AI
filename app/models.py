# app/models.py

from flask_login import UserMixin
from app.extensions import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a user from the database."""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model for the database."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    podcasts = db.relationship('Podcast', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
# --- NEW: Podcast Model ---
class Podcast(db.Model):
    __tablename__ = 'podcasts'

    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100), nullable=False)
    # Status can be: 'processing', 'completed', 'failed'
    status = db.Column(db.String(20), nullable=False, default='processing')
    generated_audio_path = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Foreign Key to link to a User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Podcast {self.id} - {self.original_filename}>'
"""Database models for the application."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db

class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'flasksession-users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.string(200), primary_key=False, nullable=False, unique=False)
    website = db.Column(db.String(60), index=False, nullable=True, unique=False)
    created_on = db.Column(db.DateTime, index=False, nullable=True, unique=False)
    last_login = db.Column(db.DateTime, index=False, nullable=True, unique=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>, format(self.name)'
    
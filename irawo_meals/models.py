"""
Database models for the irawo_meals app with SQLAlchemy
"""

from irawo_meals import db
from sqlalchemy import Column, ForeignKey, Integer, String

# Create object representing users table in database
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(60))
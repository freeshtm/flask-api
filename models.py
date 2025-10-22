import datetime
from app_setup import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.String(80), nullable=True)
    university = db.Column(db.String(80), nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self): 
        return f"User(username = {self.username}, email = {self.email})"
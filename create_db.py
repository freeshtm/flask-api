from app_setup import app, db 
from models import UserModel, RideModel, RideParticipantModel, RatingModel

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
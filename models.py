import datetime
import enum
from app_setup import db
from werkzeug.security import generate_password_hash, check_password_hash

class RideStatus(enum.Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

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

class RideModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    from_address = db.Column(db.Text, nullable=False)
    from_lat = db.Column(db.Float, nullable=False)
    from_lng = db.Column(db.Float, nullable=False)
    to_address = db.Column(db.Text, nullable=False)
    to_lat = db.Column(db.Float, nullable=False)
    to_lng = db.Column(db.Float, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    price_per_seat = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(RideStatus, by_name=False), default=RideStatus.PLANNED) #dodałem to by_name
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Ride(id = {self.id}, driver_id = {self.driver_id}, from = {self.from_address}, to = {self.to_address}, status = {self.status})"

class RideParticipantModel(db.Model):
    __table_args__ = (db.UniqueConstraint('ride_id', 'passenger_id', name='unique_ride_passenger'),)
    
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride_model.id', ondelete='CASCADE'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"RideParticipant(id = {self.id}, ride_id = {self.ride_id}, passenger_id = {self.passenger_id})"

class RatingModel(db.Model):
    __table_args__ = (
        db.UniqueConstraint('user_id', 'rater_id', 'ride_id', name='unique_rating_per_ride'),
        db.CheckConstraint('stars >= 1 AND stars <= 5', name='check_stars_range')
    )
    
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride_model.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    rater_id = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Rating(id = {self.id}, ride_id = {self.ride_id}, user_id = {self.user_id}, rater_id = {self.rater_id}, stars = {self.stars})"


from flask_restful import Resource, reqparse, fields, marshal_with, abort
from werkzeug.security import generate_password_hash, check_password_hash

from app_setup import db
from models import UserModel
from models import *
from datetime import datetime

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")
user_args.add_argument('student_id', type=str, required=False)
user_args.add_argument('university', type=str, required=False)

userFields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'student_id': fields.String,
    'university': fields.String,
    'average_rating': fields.Float,
    'created_at': fields.DateTime(dt_format='iso8601')
}

login_user_args = reqparse.RequestParser()
login_user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
login_user_args.add_argument('password', type=str, required=True, help="Password cannot be blank") 


rideFields = {
    'id': fields.Integer,
    'driver_id': fields.Integer,
    'from_address': fields.String,
    'from_lat': fields.Float,
    'from_lng': fields.Float,
    'to_address': fields.String,
    'to_lat': fields.Float,
    'to_lng': fields.Float,
    'departure_time': fields.DateTime(dt_format='iso8601'),
    'price_per_seat': fields.Float,
    'seats_available': fields.Integer,
    'status': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601')
}

ride_args = reqparse.RequestParser()
ride_args.add_argument('driver_id', type=int, required=True, help="Driver ID cannot be blank")
ride_args.add_argument('from_address', type=str, required=True, help="From address cannot be blank")
ride_args.add_argument('from_lat', type=float, required=True, help="From latitude cannot be blank")
ride_args.add_argument('from_lng', type=float, required=True, help="From longitude cannot be blank")
ride_args.add_argument('to_address', type=str, required=True, help="To address cannot be blank")
ride_args.add_argument('to_lat', type=float, required=True, help="To latitude cannot be blank")
ride_args.add_argument('to_lng', type=float, required=True, help="To longitude cannot be blank")
ride_args.add_argument('departure_time', type=str, required=True, help="Departure time cannot be blank (use ISO format)")
ride_args.add_argument('price_per_seat', type=float, required=True, help="Price per seat cannot be blank")
ride_args.add_argument('seats_available', type=int, required=True, help="Seats available cannot be blank")
ride_args.add_argument('status', type=str, required=False, choices=('planned', 'in_progress', 'completed', 'cancelled'))
#ride_args.add_argument('status', type=str, required=False, choices=('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'))


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        password_hash = generate_password_hash(args['password'])
        
        user = UserModel(
            username=args['username'],
            email=args['email'],
            password_hash=password_hash,
            student_id=args.get('student_id'),
            university=args.get('university')
        )
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        
        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password_hash = generate_password_hash(args['password'])
        if args.get('student_id') is not None:
            user.student_id = args['student_id']
        if args.get('university') is not None:
            user.university = args['university']
        
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

class Register(Resource):
    def post(self):
        args = user_args.parse_args()

        if UserModel.query.filter_by(username=args['username']).first():
            abort(400, message="Username already exist")
        if UserModel.query.filter_by(email=args['email']).first():
            abort(400, message="Email already exists")
        
        password_hash = generate_password_hash(args['password'])

        user = UserModel(
            username = args['username'],
            email = args['email'],
            password_hash = password_hash,
            student_id = args.get('student_id'),
            university = args.get('university')
            )
        db.session.add(user)
        db.session.commit()
        return {'message': "User created successfully"}, 201
    
class Login(Resource):
    def post(self):
        args = login_user_args.parse_args()

        user = UserModel.query.filter_by(email=args['email']).first()
        if not user:
            abort(404, message="User not found")
        if not check_password_hash(user.password_hash, args['password']):
            abort(401, message="Wrong email or password")
        return{
            "id" : user.id,
            "email" : user.email,
            "message" : "Login succesful"
        }, 200
        

class Rides(Resource):
    @marshal_with(rideFields)
    def get(self):
        rides = RideModel.query.all() 
        return rides 
    
    @marshal_with(rideFields)
    def post(self):
        args = ride_args.parse_args()

        try:
            departure_time = datetime.fromisoformat(args['departure_time'])
        except ValueError:
            return {'message': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}, 400

        
        ride = RideModel(
            driver_id=args['driver_id'],
            from_address=args['from_address'],
            from_lat=args['from_lat'],
            from_lng=args['from_lng'],
            to_address=args['to_address'],
            to_lat=args['to_lat'],
            to_lng=args['to_lng'],
            departure_time=departure_time,
            price_per_seat=args['price_per_seat'],
            seats_available=args['seats_available'],
            status=(args.get('status') or 'planned').upper()
        )
        db.session.add(ride)
        db.session.commit()
        rides = UserModel.query.all()
        return rides, 201
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Ride ID is required")
        args = parser.parse_args()

        ride = RideModel.query.get(args['id'])
        if not ride:
            return {'message': 'Ride not found'}, 404

        db.session.delete(ride)
        db.session.commit()
        return {'message': f'Ride with id {args["id"]} deleted successfully'}, 200

class RideJoin(Resource):
    def post(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument('passenger_id', type=int, required=True, help="Passenger ID is required")
        args = parser.parse_args()

        ride = RideModel.query.get(ride_id)
        if not ride:
            return {'message': 'Ride not found'}, 404

        if ride.seats_available <= 0:
            return {'message': 'No seats available'}, 400
        if ride.driver_id == args['passenger_id']:
            return {'message': 'Driver cannot join'}, 400

        existing = RideParticipantModel.query.filter_by(
            ride_id=ride_id,
            passenger_id=args['passenger_id']
        ).first()
        if existing:
            return {'message': 'Passenger already joined this ride'}, 400

        participant = RideParticipantModel(
            ride_id=ride_id,
            passenger_id=args['passenger_id'],
            status=ParticipantStatus.REQUESTED
        )

        ride.seats_available -= 1
        db.session.add(participant)
        db.session.commit()

        return {'message': f'Passenger {args["passenger_id"]} joined ride {ride_id}'}, 201
    
participantFields = {
    'id': fields.Integer,
    'ride_id': fields.Integer,
    'passenger_id': fields.Integer,
    'status': fields.String,
    'joined_at': fields.DateTime(dt_format='iso8601')
}

class AllParticipants(Resource):
    @marshal_with(participantFields)
    def get(self):
        participants = RideParticipantModel.query.all()
        return participants


class RideLeave(Resource):
    def post(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument('passenger_id', type=int, required=True, help="Passenger ID is required")
        args = parser.parse_args()

        participant = RideParticipantModel.query.filter_by(
            ride_id=ride_id,
            passenger_id=args['passenger_id']
        ).first()

        if not participant:
            return {'message': 'Passenger not in this ride'}, 404

        if participant.status != ParticipantStatus.REQUESTED:
            return {'message': 'Cannot leave ride in current status'}, 400

        ride = RideModel.query.get(ride_id)
        ride.seats_available += 1

        db.session.delete(participant)
        db.session.commit()

        return {'message': f'Passenger {args["passenger_id"]} left ride {ride_id}'}, 200
    
class RideStart(Resource):
    def patch(self, ride_id):
        ride = RideModel.query.get(ride_id)
        if not ride:
            return {'message': 'Ride not found'}, 404

        if ride.status != RideStatus.PLANNED:
            return {'message': 'Ride cannot be started'}, 400

        ride.status = RideStatus.IN_PROGRESS
        db.session.commit()

        return {'message': f'Ride {ride_id} started'}, 200
    
class RideComplete(Resource):
    def patch(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument('driver_id', type=int, required=True, help="Driver ID is required")
        args = parser.parse_args()

        ride = RideModel.query.get(ride_id)
        if not ride:
            return {'message': 'Ride not found'}, 404

        if ride.driver_id != args['driver_id']:
            return {'message': 'Only the driver can complete the ride'}, 403

        if ride.status != RideStatus.IN_PROGRESS:
            return {'message': 'Ride is not in progress and cannot be completed'}, 400

        ride.status = RideStatus.COMPLETED

        participants = RideParticipantModel.query.filter_by(ride_id=ride_id).all()
        for p in participants:
            p.status = ParticipantStatus.COMPLETED

        db.session.commit()

        return {'message': f'Ride {ride_id} completed and participants updated'}, 200

from flask import Flask
from app_setup import app, api
#from api import Users, User, Register, Login, Rides, RideJoin,AllParticipants,RideLeave,RideStart
from api import *

@app.route('/')
def home():
    return {
        'message': 'Flask API',
        'endpoints': {
            'users': '/api/users/',
            'user': '/api/users/<id>',
            'register': '/api/register',
            'login': '/api/login/'
        }
    }

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login/')
api.add_resource(Rides, '/api/rides/')
api.add_resource(RideJoin, '/api/rides/<int:ride_id>/join/')
api.add_resource(AllParticipants, '/api/participants/')
api.add_resource(RideLeave, '/api/rides/<int:ride_id>/leave')
api.add_resource(RideStart, '/api/rides/<int:ride_id>/start')
api.add_resource(RideComplete, '/api/rides/<int:ride_id>/complete')
api.add_resource(RideParticipants, '/api/rides/<int:ride_id>/participants')
api.add_resource(Ratings, '/api/ratings/')
api.add_resource(UserRides, '/api/users/<int:id>/rides')

if __name__ == '__main__':
    app.run(debug=True)

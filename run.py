from flask import Flask
from app_setup import app, api
from api import Users, User, Register, Login

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

if __name__ == '__main__':
    app.run(debug=True)

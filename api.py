from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.String(80), unique=True, nullable=True)
    university = db.Column(db.String(80), nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self): 
        return f"User(username = {self.username}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")  # Surowe hasło, zahaszuj w kodzie
user_args.add_argument('student_id', type=str, required=False)  # Optional
user_args.add_argument('university', type=str, required=False)  # Optional
# Do not add average_rating and created_at - deafults are enough

userFields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'student_id': fields.String,
    'university': fields.String,
    'average_rating': fields.Float,
    'created_at': fields.DateTime(dt_format='iso8601')
}

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
            student_id=args.get('student_id'),  # .get() for optional fields, to avoid KeyError if not provided
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
        
        # Update if provided
        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']
        if args['password']:  # Hash if provided
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
            abort(400,message="Email already exists")
        ##if UserModel.query.filter_by(student_id=args['student_id']).first():
          ##  abort(400,message="Student_id already exists")
        
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
    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Register, '/api/register/')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 
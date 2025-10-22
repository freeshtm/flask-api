from flask_restful import Resource, reqparse, fields, marshal_with, abort
from werkzeug.security import generate_password_hash, check_password_hash

from app_setup import db
from models import UserModel

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
        
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from werkzeug .exceptions import HTTPException
from flask import make_response
from .database import db
from .models import User
import json


create_user_parser = reqparse.RequestParser() 
create_user_parser.add_argument('user_id')
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('password')
create_user_parser.add_argument('email')
create_user_parser.add_argument('first_name')
create_user_parser.add_argument('last_name')
create_user_parser.add_argument('profile_pic')
create_user_parser.add_argument('followers')
create_user_parser.add_argument('following')

update_user_parser = reqparse.RequestParser() 
update_user_parser.add_argument('profile_pic')



login_fields_1 = {
    "user_id" : fields.Integer,
    "user_name" : fields.String,
    "password" : fields.String,
    "email" : fields.String,
    "first_name" : fields.String,
    "last_name" : fields.String,
    "profile_pic" : fields.String
}
login_fields_2 = {
    "user_id" : fields.Integer,
    "user_name" : fields.String,
    "profile_pic" : fields.String
}

class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response('',status_code)
class BuisnessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message = {'error_code':error_code,'error_message':error_message}
        self.response = make_response(json.dumps(message),status_code)

class UserAPI(Resource):
    @marshal_with(login_fields_1)
    def get(self, user_name):
        
        sql = db.session.query(User).filter(User.user_name == user_name).first()
        if sql:
            return sql
        else:
            raise NotFoundError(status_code = 404)
    @marshal_with(login_fields_2)
    def post(self):
        
        args = create_user_parser.parse_args()
        user_id = args.get("user_id",None)
        user_name = args.get("user_name",None)
        password = args.get("password",None)
        email = args.get("email",None)
        first_name = args.get("first_name",None)
        last_name = args.get("last_name",None)
        profile_pic = args.get("profile_pic",None)
        following = args.get("following",None)
        followers = args.get("followers",None)
        # return password
        if user_id is None:
            raise BuisnessValidationError(status_code=400, error_code ='USER001',error_message = 'User Id is required')
        if user_name is None:
            raise BuisnessValidationError(status_code=400, error_code ='USER002',error_message = 'User Name is required')
        if password is None:
            raise BuisnessValidationError(status_code=400, error_code ='USER003',error_message = 'Password is required')
        if email is None:
            raise BuisnessValidationError(status_code=400, error_code ='USER004',error_message = 'email is required')
        if first_name is None:
            raise BuisnessValidationError(status_code=400, error_code ='USER005',error_message = 'First Name Name is required')

        sql = User(user_id = user_id, user_name = user_name, password = password, email = email, first_name = first_name, last_name = last_name
        , profile_pic = profile_pic, followers = followers, following = following)
        db.session.add(sql)
        db.session.commit()
        return sql
    
    @marshal_with(login_fields_2)
    def put(self, user_name):
        args = update_user_parser.parse_args()
        sql = User.query.filter_by(user_name = user_name).first()
        if sql:
            profile_pic = args.get("profile_pic", None)
            sql.profile_pic = profile_pic
            db.session.commit()
            return sql
        else:
            raise BuisnessValidationError(status_code=400, error_code ='USER002',error_message = 'User Name is required or does not exist')
    
    def delete(self, user_name):
        sql = User.query.filter_by(user_name = user_name).first()
        if sql:
            db.session.delete(sql)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            raise BuisnessValidationError(status_code=400, error_code ='USER002',error_message = 'User Name is required or does not exist')

from flask_restful import Resource, Api, fields, marshal_with, reqparse
from werkzeug .exceptions import HTTPException
from flask import make_response
from .database import db
from .models import User, UserPosts, Posts
import json

post_fields_1 = {
   "post_id" : fields.Integer
}
create_post_parser = reqparse.RequestParser() 
create_post_parser.add_argument('post_name')
create_post_parser.add_argument('caption')
create_post_parser.add_argument('image')

update_post_parser = reqparse.RequestParser() 
update_post_parser.add_argument('post_name')
update_post_parser.add_argument('post_caption')
update_post_parser.add_argument('post_image')



post_fields_2 = {
    "post_id" : fields.Integer,
    "post_name" : fields.String,
    "post_caption" : fields.String,
    "post_image" : fields.String
}

post_fields_3 = post_fields_2 = {
    "post_id" : fields.Integer,
    "post_name" : fields.String,
}

class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response('',status_code)
class BuisnessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message = {'error_code':error_code,'error_message':error_message}
        self.response = make_response(json.dumps(message),status_code)

class PostAPI(Resource):
    @marshal_with(post_fields_1)
    def get(self, user_name):
        sql = User.query.filter_by(user_name = user_name).first()
        if sql:
            sql1 = UserPosts.query.filter_by(user_id = sql.user_id).all()
            return sql1
        else:
            raise BuisnessValidationError(status_code=400, error_code ='USER002',error_message = 'User Name is required')
    @marshal_with(post_fields_2)
    def post(self, user_name):
        args = create_post_parser.parse_args()
        post_name = args.get("post_name", None)
        caption = args.get("caption", None)
        image = args.get("image", None)
        if not post_name:
            raise BuisnessValidationError(status_code=400, error_code ='POST001',error_message = 'Post Name is required')
        if not caption:
            raise BuisnessValidationError(status_code=400, error_code ='POST002',error_message = 'Post description is required')
        sql = Posts(post_name = post_name, post_caption = caption, post_image = image)
        db.session.add(sql)
        sql1 = User.query.filter_by(user_name = user_name).first()
        sql2 = UserPosts(user_id = sql1.user_id, post_id = sql.post_id)
        db.session.add(sql2)
        db.session.commit()
        return sql

    @marshal_with(post_fields_3)  
    def put(self, user_name, post_id):
        sql1 = User.query.filter_by(user_name = user_name).first()
        sql2 = db.session.query(UserPosts).filter((UserPosts.user_id == sql1.user_id )& (UserPosts.post_id == post_id)).first()
        if sql2:
            sql = Posts.query.filter_by(post_id = post_id).first()
            args = update_post_parser.parse_args()
            post_name = args.get("post_name", None)
            caption = args.get("post_caption", None)
            image = args.get("post_image", None)
            if not post_name:
                raise BuisnessValidationError(status_code=400, error_code ='POST001',error_message = 'Post Name is required')
            if not caption:
                raise BuisnessValidationError(status_code=400, error_code ='POST002',error_message = 'Post description is required')

            sql.post_name = post_name
            sql.post_caption = caption
            if image is not None:
                sql.post_image = image
            else:
                sql.post_image = sql.post_image
            db.session.commit()
            return sql
        return NotFoundError(status_code = 404)


    def delete(self, user_name, post_id):
        sql = Posts.query.filter_by(post_id = post_id).first()
        sql2 = User.query.filter_by(user_name = user_name).first()
        if sql:
            sql1 = db.session.query(UserPosts).filter((UserPosts.user_id == sql2.user_id )& (UserPosts.post_id == post_id)).first()
            db.session.delete(sql)
            db.session.delete(sql1)
            db.session.commit()
            return "Successfully Deleted", 200
        return NotFoundError(status_code = 404)
        

from .database import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    profile_pic = db.Column(db.Text)
    following = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    posting = db.relationship("Posts", secondary = "UserPosts")
    
    
    


class Posts(db.Model):
    __tablename__ = "Posts"
    post_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post_name = db.Column(db.String, nullable = False)
    post_caption = db.Column(db.String, nullable = False)
    post_image = db.Column(db.Text)
    
    date = db.Column(db.String)
    time = db.Column(db.String)
    post_like = db.Column(db.Integer)
    commenting = db.relationship("Comment", secondary = "PostComment")
    
class Comment(db.Model):
    __tablename__ = "Comments"
    comment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    comment = db.Column(db.Text, nullable = False)
    comment_like = db.Column(db.Integer)

class PostComment(db.Model):
    __tablename__ = "PostComment"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("Posts.post_id", ondelete='CASCADE'), nullable = False)
    comment_id = db.Column(db.Integer, db.ForeignKey("Comments.comment_id", ondelete='CASCADE'), nullable = False, unique = True)
    post_user_comment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
   


class UserPosts(db.Model):
    __tablename__ = "UserPosts"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("Posts.post_id"), nullable = False)
    user_post_id = db.Column(db.Integer, primary_key = True, autoincrement = True)

class Follow(db.Model):
    __tablename__ = "Follow"
    user_1 = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable = False)
    user_2 = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete='CASCADE'), nullable = False)
    follow_id = db.Column(db.Integer, primary_key = True, autoincrement = True)


   

db.create_all()
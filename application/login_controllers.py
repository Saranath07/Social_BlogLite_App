from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import User, Posts, PostComment, Follow, UserPosts
from .database import db
import secrets 
import random
from operator import itemgetter
app.secret_key = secrets.token_hex()

@app.route("/home_page/<user_name>", methods = ["GET", "POST", "DELETE", "PUT"])
def home(user_name):
    #select * from User where user_name = user_name limit 1
    sql = User.query.filter_by(user_name = user_name).first()
    all_other_users = User.query.all()
    # return render_template("dummy.html", sql = sql.user_name)
    if sql:
        if('user' in session and session['user'] == sql.user_name):
        
            users = request.args.get('username')
            if users:
                user = User.query.filter(User.user_name.contains(users)).all()
                if user:
                    return render_template("search.html", user = user, user_name = user_name, 
                                                image = sql.profile_pic) 
                return "User does not exist"

            sql_fole = Follow.query.filter_by(user_1 = user_name).all()
            
            followees = []
            for i in sql_fole:
                
                sql_user = User.query.filter_by(user_name = i.user_2).first()
                
                sql_user_posts = UserPosts.query.filter_by(user_id = sql_user.user_id).all()
                
                followee_posts = []
                for j in sql_user_posts:
                    sql_post = Posts.query.filter_by(post_id = j.post_id).first()
                    followee_posts.append((sql_post.post_name, sql_post.post_caption, sql_post.post_image, sql_user.user_name, sql_user.profile_pic, sql_post.post_id,
                            sql_post.post_like, sql_post.date, sql_post.time))
                followees.append(followee_posts)
            

            # sql_folr = Follow.query.filter_by(user_2 = user_name).all()
            # followers = []
            # for i in sql_folr:
                
            #     sql_user = User.query.filter_by(user_name = i.user_1).first()
                
            #     sql_user_posts = UserPosts.query.filter_by(user_id = sql_user.user_id).all()
                
            #     followee_posts = []
            #     for j in sql_user_posts:
            #         sql_post = Posts.query.filter_by(post_id = j.post_id).first()
            #         followee_posts.append((sql_post.post_name, sql_post.post_caption, 
            #         sql_post.post_image, sql_user.user_name, 
            #         sql_user.profile_pic, sql_post.post_id,
            #                 sql_post.post_like, sql_post.date, sql_post.time, sql_post.post_id))
            #         followee_posts.sort(key = itemgetter(9), reverse=True)
            #     followers.append(followee_posts)
            
            

            
            
            




            
            
            return render_template("home.html", user_name = sql.user_name, f_name = sql.first_name, l_name = sql.last_name
            , image = sql.profile_pic, followees = followees)
    return "Error"




@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        c_pass = request.form["c_password"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        if password != c_pass:
            return render_template("pass_error.html")
        sql = User(user_name = username, password = password, email = email, first_name = first_name, last_name = last_name
        , profile_pic = "default.jpg", followers = 0, following = 0)
        try:
            db.session.add(sql)
            db.session.commit()
            return redirect('/login')
        except:
            return render_template("signuperror.html")
    return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = db.session.query(User).filter((User.user_name == username) & (User.password == password)).first()
        
        if sql:
            session['user'] = username
            return redirect(url_for('home', user_name = sql.user_name))
        return render_template("error.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    try:
        session.pop('user')
    except:
        return render_template("error.html")
    return redirect(url_for('login'))
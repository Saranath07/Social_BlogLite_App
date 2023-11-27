from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import User, Posts, UserPosts, Follow, Comment, PostComment
from .database import db

@app.route("/<user_1>/follow/<user_2>", methods = ["GET", "POST"])
def follow(user_1, user_2):
    sql = Follow(user_1 = user_1, user_2 = user_2)
    db.session.add(sql)
    db.session.commit()
    sql1 = User.query.filter_by(user_name = user_1).first()
    
    sql1.following += 1
    sql2 = User.query.filter_by(user_name = user_2).first()
    sql2.followers += 1
    db.session.commit()
    
    return redirect("/" + user_1 + "/profile/" + user_2)

@app.route("/<user_1>/unfollow/<user_2>", methods = ["GET", "POST"])
def unfollow(user_1, user_2):
    sql = db.session.query(Follow).filter((Follow.user_1 == user_1) & (Follow.user_2 == user_2)).first()
    db.session.delete(sql)
    sql1 = User.query.filter_by(user_name = user_1).first()
    sql1.following -= 1
    sql2 = User.query.filter_by(user_name = user_2).first()
    sql2.followers -= 1
    db.session.commit()
    db.session.commit()
    
    return redirect("/" + user_1 + "/profile/" + user_2)

@app.route("/<user_1>/followers/<user_2>")
def display_followers(user_1, user_2):

    sql = Follow.query.filter_by(user_2 = user_2).all()
    sql2 = User.query.filter_by(user_name = user_1).first()
    
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user[0].user_name, user_name = user_1, 
                                        image = sql2.profile_pic)
    followers = []
    for i in sql:
        sql1 = User.query.filter_by(user_name = i.user_1).first()
        followers.append((i.user_1, sql1.profile_pic))

    return render_template("followers.html", followers = followers, user_name = user_1, image = sql2.profile_pic)

@app.route("/<user_1>/followee/<user_2>")
def display_followee(user_1, user_2):
    sql = Follow.query.filter_by(user_1 = user_2).all()
    sql2 = User.query.filter_by(user_name = user_1).first()
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user, user_name = user_1, 
                                        image = sql2.profile_pic)
    followers = []
    
    followees = []
    for i in sql:
        sql1 = User.query.filter_by(user_name = i.user_2).first()
        followees.append((i.user_2, sql1.profile_pic))
    return render_template("followee.html", followees = followees, user_name = user_1, image = sql2.profile_pic)
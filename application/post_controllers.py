from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import User, Posts, UserPosts, PostComment, Comment
from .database import db
from datetime import datetime


app.config['UPLOAD_FOLDER'] = "static\images"


@app.route("/add_post/<user_name>", methods = ["GET", "POST"])
def add_post(user_name):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt = dt_string.split(" ")
    date, time = dt[0], dt[1]
    sql2 = User.query.filter_by(user_name = user_name).first()
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user, user_name = user_name, 
                                                image = sql2.profile_pic) 
        return "User does not exist"
    if sql2:
        if request.method == "GET":
            return render_template('add_post.html', user_name = user_name, image = sql2.profile_pic)
            
        elif request.method == "POST":
            
            name = request.form['name']
            caption = request.form['caption']
            image = request.files['imageFile']
            
            user = User.query.filter_by(user_name = user_name).first()
            user_id = user.user_id
            if image.filename != "":
                file_path = "static/" + image.filename
                image.save(file_path)
                
                
                sql = Posts(post_name = name, post_caption = caption, post_image = image.filename, post_like = 0
                    ,date = date, time = time)
                
                db.session.add(sql)
                db.session.commit()
                
                post_id = sql.post_id
                sql1 = UserPosts(user_id = user_id, post_id = post_id)
                db.session.add(sql1)
                db.session.commit()
                return redirect("/my_profile/" + user_name)
            else:
                sql = Posts(post_name = name, post_caption = caption)
                
                db.session.add(sql)
                db.session.commit()
                
                post_id = sql.post_id
                sql1 = UserPosts(user_id = user_id, post_id = post_id)
                db.session.add(sql1)
                db.session.commit()
                return redirect("/my_profile/" + user_name)
    return "Error"

@app.route("/<user_name>/edit_post/<post_id>", methods = ["GET", "POST"])
def edit_post(user_name, post_id):
    sql2 = Posts.query.filter_by(post_id = post_id).first()
    
    # return sql2.post_image
    sql3 = User.query.filter_by(user_name = user_name).first()
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user, user_name = user_name, 
                                                image = sql3.profile_pic) 
        return "User does not exist"
    sql = User.query.filter_by(user_name = user_name).first()
    if sql:
        if request.method == "GET":
            return render_template('edit_post.html', user_name = user_name, image = sql.profile_pic\
                        ,post_id = post_id, Name = sql2.post_name, Caption = sql2.post_caption, Image = sql2.post_image)
            
        elif request.method == "POST":
            
            name = request.form['name']
            
            caption = request.form['caption']
            image = request.files['imageFile']
           

            if name != "":
                 sql2.post_name = name
            
            if caption != "":
                sql2.post_caption = caption
            
            if image.filename != "":
                file_path = "static/" + image.filename
                image.save(file_path)
                
               
                
                sql2.post_image = image.filename
            sql2.post_like = 0
            
            db.session.commit()
               
            return redirect("/my_profile/" + user_name)
           
                
                
                
                
    return "Error"


@app.route("/<user_name>/delete_post/<post_id>", methods = ["GET", "POST", "DELETE"])
def delete_post(user_name, post_id):
    sql3 = User.query.filter_by(user_name = user_name).first()
    if request.method == "GET":
        return render_template("post_delete_confo.html", image = sql3.profile_pic, user_name = sql3.user_name, post_id = post_id)
    sql = Posts.query.filter_by(post_id = post_id).first()
    
    
    sql2 = UserPosts.query.filter_by(post_id = post_id).all()
    for i in sql2:
        x = PostComment.query.filter_by(post_id = i.post_id).all()
        for j in x:
            
            k = Comment.query.filter_by(comment_id = j.comment_id).first()
            db.session.delete(k)
            db.session.delete(j)
        db.session.delete(i)
    db.session.delete(sql)
    db.session.commit()
    return redirect("/my_profile/" + user_name)


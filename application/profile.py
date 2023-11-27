from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from application.models import User, Posts, UserPosts, Follow, Comment, PostComment
from .database import db



@app.route("/my_profile/<user_name>")
def my_profile(user_name):
    sql = User.query.filter_by(user_name = user_name).first()
    
    if sql:
        user_id = sql.user_id
        total_posts = UserPosts.query.filter_by(user_id = user_id).all()
        total_following = Follow.query.filter_by(user_2 = user_name).all()
        total_followers = Follow.query.filter_by(user_1 = user_name).all()
        users = request.args.get('username')
        if users:
            user = User.query.filter(User.user_name.contains(users)).all()
            if user:
                return render_template("search.html", user = user, user_name = user_name, 
                                            image = sql.profile_pic) 
            return "User does not exist"
        # return render_template("dummy.html", sql = total_posts)
        uposts = UserPosts.query.filter_by(user_id = user_id).all()
        #return render_template("dummy.html", sql = uposts[0].post_id)
        posts = []
        
        for post in uposts:
            x = Posts.query.filter_by(post_id = post.post_id).all()
            for i in x:
                comments = []
                y = PostComment.query.filter_by(post_id = i.post_id).all()
                
                for comment in y:
                    # return str(comment.user_id) + " " + str(comment.comment_id)
                    z = Comment.query.filter_by(comment_id = comment.comment_id).first()
                    w = User.query.filter_by(user_id = comment.user_id).first()
                    comments.append((z.comment, w.user_name, w.profile_pic, z.comment_like, z.comment_id))
                posts.append([i.post_name, i.post_caption, i.post_image, i.post_id, comments, i.post_like, i.date, i.time])
                
        
        return render_template("my_profile_1.html", posts = posts, total_posts = len(total_posts), foll1 = len(total_followers), foll2 = len(total_following)
                    ,user_name = sql.user_name, f_name = sql.first_name, l_name = sql.last_name, image = sql.profile_pic)
    return f"No user Found"
@app.route("/settings/<user_name>", methods = ["GET", "POST"])
def settings(user_name):
    
    sql2 = User.query.filter_by(user_name = user_name).first()
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user, user_name = user_name, 
                                                image = sql2.profile_pic) 
    if sql2:
        if request.method == "POST":
            profile_pic = request.files['profile_pic']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            
            
            if profile_pic.filename != "":
                file_path = "static/" + profile_pic.filename
                profile_pic.save(file_path)
                
                
                sql2.profile_pic = profile_pic.filename
                
            
            
            if email != "":
                sql2.email = email
            if first_name != "":
                sql2.first_name = first_name
            if last_name != "":
                sql2.last_name = last_name
            db.session.commit()

        

        return render_template("settings.html", user_name = user_name, image = sql2.profile_pic)

    return "Error"

@app.route("/comment/<user_name>/<post_id>", methods = ["GET", "POST"])
def post_comment(user_name, post_id):
    sql = Posts.query.filter_by(post_id = post_id).first()
    sql1 = User.query.filter_by(user_name = user_name).first()
    sql2 = UserPosts.query.filter_by(post_id = post_id).first()
    sql3 = User.query.filter_by(user_id = sql2.user_id).first()
    if request.method == "POST":
        comment = request.form['comment']
        add_comment = Comment(comment = comment, comment_like = 0)
        db.session.add(add_comment)
        db.session.commit()
        sql1 = PostComment(user_id = sql1.user_id, post_id = post_id, comment_id = add_comment.comment_id)
        db.session.add(sql1)
        db.session.commit()
        if user_name == sql3.user_name:
            return redirect("/my_profile/" + user_name)
        return redirect("/" + user_name + "/profile/" + sql3.user_name)
    return render_template("add_comment.html", post_id = post_id, user_name = user_name)

@app.route("/<user_name>/like/<post_id>")
def like(user_name, post_id):
    sql = Posts.query.filter_by(post_id = post_id).first()
    sql1 = User.query.filter_by(user_name = user_name).first()
    sql2 = UserPosts.query.filter_by(post_id = post_id).first()
    sql3 = User.query.filter_by(user_id = sql2.user_id).first()
    sql.post_like += 1
    db.session.commit()

    if user_name == sql3.user_name:
        return redirect("/my_profile/" + user_name)
    
    return redirect("/" + user_name+ "/profile/" + sql3.user_name)

@app.route("/<user_name>/comment_like/<comment_id>/<user_2>")
def comment_like(user_name, comment_id, user_2):
    sql = Comment.query.filter_by(comment_id = comment_id).first()
    sql1 = User.query.filter_by(user_name = user_name).first()
    sql.comment_like += 1
    db.session.commit()

    if user_name == user_2:
        return redirect("/my_profile/" + user_name)
    return redirect("/" + user_name + "/profile/" + user_2)
    
  

@app.route("/<user_name_1>/profile/<user_name>", methods = ["GET", "POST"])
def user_profile(user_name_1, user_name):
    sql = User.query.filter_by(user_name = user_name).first()
    sql1 = User.query.filter_by(user_name = user_name_1).first()
    
    users = request.args.get('username')
    if users:
        user = User.query.filter(User.user_name.contains(users)).all()
        if user:
            return render_template("search.html", user = user, user_name = user_name, 
                                                image = sql1.profile_pic) 
    if sql:
        user_id = sql.user_id
        total_posts = UserPosts.query.filter_by(user_id = user_id).all()
        total_following = Follow.query.filter_by(user_2 = user_name).all()
        total_followers = Follow.query.filter_by(user_1 = user_name).all()
        following = db.session.query(Follow).filter((Follow.user_1 == user_name_1) & (Follow.user_2 == user_name)).first()
        result = False
        if following:
            result = True
        # return render_template("dummy.html", sql = total_posts)
        uposts = UserPosts.query.filter_by(user_id = user_id).all()
        #return render_template("dummy.html", sql = uposts[0].post_id)
        posts = []
        
        for post in uposts:
            x = Posts.query.filter_by(post_id = post.post_id).all()
            for i in x:
                comments = []
                y = PostComment.query.filter_by(post_id = i.post_id).all()
                
                for comment in y:
                    # return str(comment.user_id) + " " + str(comment.comment_id)
                    z = Comment.query.filter_by(comment_id = comment.comment_id).first()
                    w = User.query.filter_by(user_id = comment.user_id).first()
                    comments.append((z.comment, w.user_name, w.profile_pic, z.comment_like, z.comment_id))
                posts.append([i.post_name, i.post_caption, i.post_image, i.post_id, comments, i.post_like, i.date, i.time])
                
        
        return render_template("profile.html", posts = posts, total_posts = len(total_posts), foll1 = len(total_followers), foll2 = len(total_following)
                    , f_name = sql.first_name, l_name = sql.last_name, image = sql1.profile_pic, image1 = sql.profile_pic, user_name = user_name_1, other_user = user_name, result = result)
    return f"No user Found"

@app.route("/<user_name>/delete_account", methods = ["GET", "POST"])
def delete_account(user_name):
    if request.method == "GET":
        return render_template("user_delete_confo.html", user_name = user_name)
    if request.method == "POST":
        user = User.query.filter_by(user_name = user_name).first()
        
        sql2 = UserPosts.query.filter_by(user_id = user.user_id).all()
        
        comments = PostComment.query.filter_by(user_id = user.user_id).all()
        
        followers = Follow.query.filter_by(user_1 = user_name).all()
        for i in followers:
            db.session.delete(i)
            db.session.commit()
        followee = Follow.query.filter_by(user_2 = user_name).all()
        for i in followee:
            db.session.delete(i)
            db.session.commit()
        for i in sql2:
            post = Posts.query.filter_by(post_id = i.post_id).first()
            x = PostComment.query.filter_by(post_id = post.post_id).all()
            
            
            for j in x:
                
                db.session.delete(j)
        for i in comments:
            x = Comment.query.filter_by(comment_id = i.comment_id).first()
            db.session.delete(x)
            db.session.delete(i)
            db.session.commit()
    
        
        
        db.session.delete(post)
        db.session.delete(i)
    db.session.delete(user)
    db.session.commit()
    return redirect("/login")
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from .models import Post, Comment, Notification, Like, User
from . import db
from datetime import datetime
from .structures.heap import MaxHeap
import os
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_post_score(post, user_id):
    score = 0
    time_diff = (datetime.utcnow() - post.created_at).total_seconds()
    score -= time_diff / 3600
    score += post.likes * 10
    if post.user_id == user_id:
        score += 50
    return score


def add_notice(user_id, msg, link=""):
    notice = Notification(user_id=user_id, msg=msg, link=link)
    db.session.add(notice)
    db.session.commit()


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(20).all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/posts")
@login_required
def posts():
    all_posts = Post.query.all()
    heap = MaxHeap()
    
    for post in all_posts:
        score = get_post_score(post, current_user.id)
        heap.push((score, post.id, post))
    
    sorted_posts = []
    while not heap.is_empty():
        item = heap.pop()
        sorted_posts.append(item[2])
    
    return render_template("posts.html", user=current_user, posts=sorted_posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        image = None
        
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                image = filename
        
        if text or image:
            post = Post(text=text, image=image, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
        else:
            flash("Post cannot be empty.", category="error")
        
        return redirect(url_for("views.posts"))
    
    return render_template("posts.html", user=current_user, posts=[])


@views.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        flash("Post not found.", category="error")
    elif post.user_id != current_user.id:
        flash("You cannot delete this post.", category="error")
    else:
        Comment.query.filter_by(post_id=post_id).delete()
        Like.query.filter_by(post_id=post_id).delete()
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    
    return redirect(url_for("views.posts"))


@views.route("/like-post/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        post.likes -= 1
        liked = False
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        post.likes += 1
        liked = True
        if post.user_id != current_user.id:
            add_notice(post.user_id, f"{current_user.username} liked your post", f"/posts")
    
    db.session.commit()
    return jsonify({"likes": post.likes, "liked": liked})


@views.route("/add-comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    text = request.form.get("text")
    post = Post.query.get(post_id)
    
    if not post:
        flash("Post not found.", category="error")
    elif not text:
        flash("Comment cannot be empty.", category="error")
    else:
        comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        
        if post.user_id != current_user.id:
            add_notice(post.user_id, f"{current_user.username} commented on your post", f"/posts")
        
        flash("Comment added!", category="success")
    
    return redirect(url_for("views.posts"))


@views.route("/delete-comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    
    if not comment:
        flash("Comment not found.", category="error")
    elif comment.user_id != current_user.id:
        flash("You cannot delete this comment.", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted.", category="success")
    
    return redirect(url_for("views.posts"))


@views.route("/notifications")
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(
        Notification.created_at.desc()
    ).all()
    return render_template("notifications.html", user=current_user, notifications=user_notifications)


@views.route("/mark-notification-read/<int:notification_id>", methods=["POST"])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)
    
    if notification and notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    
    return jsonify({"success": True})


@views.route("/search")
@login_required
def search():
    query = request.args.get("q", "")
    
    if not query:
        return render_template("search_results.html", user=current_user, results=[], query="")
    
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    posts = Post.query.filter(Post.text.ilike(f"%{query}%")).all()
    
    return render_template(
        "search_results.html",
        user=current_user,
        users=users,
        posts=posts,
        query=query
    )

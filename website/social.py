from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Follow, Message, Notification
from . import db
from .structures.graph_follow import FollowGraph
from datetime import datetime

social = Blueprint("social", __name__)

follow_graph = FollowGraph()


def add_notice(user_id, msg, link=""):
    notice = Notification(user_id=user_id, msg=msg, link=link)
    db.session.add(notice)
    db.session.commit()


@social.route("/people")
@login_required
def people():
    users = User.query.filter(User.id != current_user.id).all()
    
    following_ids = set()
    follows = Follow.query.filter_by(follower_id=current_user.id).all()
    for f in follows:
        following_ids.add(f.followed_id)
    
    return render_template(
        "social_people.html",
        user=current_user,
        users=users,
        following_ids=following_ids
    )


@social.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    profile_user = User.query.get_or_404(user_id)
    
    followers_count = Follow.query.filter_by(followed_id=user_id).count()
    following_count = Follow.query.filter_by(follower_id=user_id).count()
    
    is_following = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=user_id
    ).first() is not None
    
    return render_template(
        "social_profile.html",
        user=current_user,
        profile_user=profile_user,
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following
    )


@social.route("/follow/<int:user_id>", methods=["POST"])
@login_required
def follow(user_id):
    if user_id == current_user.id:
        flash("You cannot follow yourself.", category="error")
        return redirect(url_for("social.people"))
    
    target_user = User.query.get(user_id)
    if not target_user:
        flash("User not found.", category="error")
        return redirect(url_for("social.people"))
    
    existing = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=user_id
    ).first()
    
    if existing:
        flash("Already following this user.", category="error")
    else:
        new_follow = Follow(follower_id=current_user.id, followed_id=user_id)
        db.session.add(new_follow)
        db.session.commit()
        
        follow_graph.follow(current_user.id, user_id)
        add_notice(user_id, f"{current_user.username} started following you", f"/profile/{current_user.id}")
        
        flash(f"Now following {target_user.username}!", category="success")
    
    return redirect(url_for("social.people"))


@social.route("/unfollow/<int:user_id>", methods=["POST"])
@login_required
def unfollow(user_id):
    existing = Follow.query.filter_by(
        follower_id=current_user.id,
        followed_id=user_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        follow_graph.unfollow(current_user.id, user_id)
        flash("Unfollowed.", category="success")
    else:
        flash("Not following this user.", category="error")
    
    return redirect(url_for("social.people"))


@social.route("/chats")
@login_required
def chats_list():
    sent = db.session.query(Message.receiver_id).filter_by(sender_id=current_user.id).distinct()
    received = db.session.query(Message.sender_id).filter_by(receiver_id=current_user.id).distinct()
    
    chat_user_ids = set()
    for row in sent:
        chat_user_ids.add(row[0])
    for row in received:
        chat_user_ids.add(row[0])
    
    chat_users = User.query.filter(User.id.in_(chat_user_ids)).all()
    
    return render_template("chats_list.html", user=current_user, chat_users=chat_users)


@social.route("/chat/<int:user_id>")
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    Message.query.filter_by(sender_id=user_id, receiver_id=current_user.id, is_read=False).update(
        {"is_read": True}
    )
    db.session.commit()
    
    return render_template("chat.html", user=current_user, other_user=other_user, messages=messages)


@social.route("/send-message/<int:user_id>", methods=["POST"])
@login_required
def send_message(user_id):
    text = request.form.get("text")
    
    if not text:
        flash("Message cannot be empty.", category="error")
        return redirect(url_for("social.chat", user_id=user_id))
    
    other_user = User.query.get(user_id)
    if not other_user:
        flash("User not found.", category="error")
        return redirect(url_for("social.chats_list"))
    
    msg = Message(text=text, sender_id=current_user.id, receiver_id=user_id)
    db.session.add(msg)
    db.session.commit()
    
    add_notice(user_id, f"New message from {current_user.username}", f"/chat/{current_user.id}")
    
    return redirect(url_for("social.chat", user_id=user_id))


@social.route("/api/messages/<int:user_id>")
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    result = []
    for m in messages:
        result.append({
            "id": m.id,
            "text": m.text,
            "sender_id": m.sender_id,
            "created_at": m.created_at.isoformat(),
            "is_mine": m.sender_id == current_user.id
        })
    
    return jsonify(result)

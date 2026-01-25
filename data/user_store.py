# data/user_store.py

from data.db import users
from datetime import datetime


def get_all_usernames():
    """Get list of all registered usernames"""
    return sorted([user["_id"] for user in users.find({}, {"_id": 1})])


def create_user(username, password):
    """Create a new user with password"""
    users.insert_one({
        "_id": username,
        "password": password,  # In production, hash this!
        "total_score": 0,
        "cards_studied": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "current_streak": 0,
        "best_streak": 0,
        "created_at": datetime.utcnow()
    })


def get_user(username):
    """Get user data"""
    return users.find_one({"_id": username})


def update_user_score(username, points_delta, correct=True):
    """Update user's score and stats"""
    increment = {
        "total_score": points_delta,
        "cards_studied": 1
    }
    
    if correct:
        increment["correct_answers"] = 1
        increment["current_streak"] = 1
    else:
        increment["incorrect_answers"] = 1
        
    users.update_one(
        {"_id": username},
        {
            "$inc": increment
        }
    )
    
    # Update best streak if current is higher
    user = get_user(username)
    if correct and user["current_streak"] > user.get("best_streak", 0):
        users.update_one(
            {"_id": username},
            {"$set": {"best_streak": user["current_streak"]}}
        )
    
    # Reset streak if incorrect
    if not correct:
        users.update_one(
            {"_id": username},
            {"$set": {"current_streak": 0}}
        )


def get_leaderboard(limit=10):
    """Get top users by score"""
    return list(users.find().sort("total_score", -1).limit(limit))
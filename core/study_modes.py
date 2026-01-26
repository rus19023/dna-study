# core/study_modes.py

import streamlit as st

STUDY_MODES = {
    "flashcard": {
        "name": "📇 Flashcard Mode",
        "description": "Traditional flip cards (honor system)",
        "requires_typing": False,
        "requires_commit": False,
        "min_delay": 0,
        "verification_rate": 0.1  # 10% verification
    },
    "quiz": {
        "name": "✍️ Quiz Mode",
        "description": "Type your answer for verification",
        "requires_typing": True,
        "requires_commit": False,
        "min_delay": 0,
        "verification_rate": 0
    },
    "commit": {
        "name": "🎯 Commit Mode",
        "description": "Commit before revealing answer",
        "requires_typing": False,
        "requires_commit": True,
        "min_delay": 3,  # 3 second delay
        "verification_rate": 0.2  # 20% verification
    },
    "hardcore": {
        "name": "🔥 Hardcore Mode",
        "description": "All anti-cheat features enabled",
        "requires_typing": True,
        "requires_commit": True,
        "min_delay": 5,
        "verification_rate": 0.3  # 30% verification
    }
}


def get_mode_config(mode_key):
    """Get configuration for a study mode"""
    return STUDY_MODES.get(mode_key, STUDY_MODES["flashcard"])
import sqlite3
import os

DATABASE_FOLDER = "database"
DATABASE_NAME = os.path.join(DATABASE_FOLDER, "chatbot.db")


def get_connection():
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_conversation(user_message, bot_response):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations (user_message, bot_response)
        VALUES (?, ?)
    """, (user_message, bot_response))

    connection.commit()
    connection.close()


def get_conversations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, user_message, bot_response, created_at
        FROM conversations
        ORDER BY created_at DESC
    """)

    conversations = cursor.fetchall()
    connection.close()

    return conversations
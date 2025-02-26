import mysql.connector 
import datetime 
import os

db_config = {
    "host":"localhost",
    "user":"root",
    "password":os.getenv("MYSQL_PASS"),
    "database":"chat_history"
}

def connect_db():
    return mysql.connector.connect(**db_config)

def store_chat(role,content):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO chat (timestamp, role, content) VALUES (%s,%s,%s)"
    cursor.execute(query,(datetime.datetime.now(),role,content))
    conn.commit()
    cursor.close()
    conn.close()
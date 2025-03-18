from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources = {r"/api/news": {
    "origins": ["https://bakueduaz.github.io"],
    "methods": ["GET"]
}})

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT"),
            sslmode = "require"
        )

        return conn

    except Exception as e:
        print(f"Database connection error: {e}")
        return None
    

@app.route("/api/news", methods=['GET'])
def get_news():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()

        cursor.execute('SELECT id, title, description, image FROM news24')

        news = cursor.fetchall()

        cursor.close()
        conn.close()

        news_list = []

        for item in news:
            news_list.append({
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "image": item[3]
            })

        return jsonify({
            "news": news_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
else:
    application = app
import mysql.connector
import datetime
import json

class CustomManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CustomManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.conn_params = {
            'database': 'finalquiztasy',
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'port': '3306'
        }
        self.init_database()

    def init_database(self):
        """Initialize database and create custom_questions table if it doesn't exist"""
        try:
            # First create the database if it doesn't exist
            conn = mysql.connector.connect(
                host=self.conn_params['host'],
                user=self.conn_params['user'],
                password=self.conn_params['password']
            )
            cursor = conn.cursor()

            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.conn_params['database']}")
            conn.commit()
            cursor.close()
            conn.close()

            # Connect to the database
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Create custom_questions table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS custom_questions
            (id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR (255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                questions JSON NOT NULL,
                user_id INT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id))''')

            conn.commit()
            cursor.close()
            conn.close()
            print("Custom questions table initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")

    def save_question_set(self, name, questions, user_id=None):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Convert questions list to JSON string
            questions_json = json.dumps(questions)

            # Insert the question set
            if user_id:
                cursor.execute(
                    "INSERT INTO custom_questions (name, questions, user_id) VALUES (%s, %s, %s)",
                    (name, questions_json, user_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO custom_questions (name, questions) VALUES (%s, %s)",
                    (name, questions_json)
                )

            conn.commit()
            cursor.close()
            conn.close()
            print(f"Saved question set '{name}' with {len(questions)} questions")
            return True
        except Exception as e:
            print(f"Error saving question set: {e}")
            return False

    def get_question_sets(self, user_id=None):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            if user_id:
                # Get question sets for specific user or public sets (user_id IS NULL)
                cursor.execute(
                    "SELECT name FROM custom_questions WHERE user_id = %s OR user_id IS NULL ORDER BY created_at DESC",
                    (user_id,)
                )
            else:
                # Get only public question sets if no user is logged in
                cursor.execute(
                    "SELECT name FROM custom_questions WHERE user_id IS NULL ORDER BY created_at DESC"
                )

            result = cursor.fetchall()
            cursor.close()
            conn.close()

            # Extract names from result
            question_sets = [row[0] for row in result]
            return question_sets
        except Exception as e:
            print(f"Error retrieving question sets: {e}")
            return []

    def get_question_set_by_name(self, name):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT questions FROM custom_questions WHERE name = %s",
                (name,)
            )

            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            print(f"Error retrieving question set: {e}")
            return None

    def delete_question_set(self, name, user_id=None):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            if user_id:
                # Only allow deletion if the set belongs to the user
                cursor.execute(
                    "DELETE FROM custom_questions WHERE name = %s AND user_id = %s",
                    (name, user_id)
                )
            else:
                # Only allow deletion of public sets if no user ID provided
                cursor.execute(
                    "DELETE FROM custom_questions WHERE name = %s AND user_id IS NULL",
                    (name,)
                )

            deleted = cursor.rowcount > 0
            conn.commit()
            cursor.close()
            conn.close()

            return deleted
        except Exception as e:
            print(f"Error deleting question set: {e}")
            return False
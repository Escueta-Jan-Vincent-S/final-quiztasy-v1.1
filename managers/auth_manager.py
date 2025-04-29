import mysql.connector
import re
import hashlib
import os

class AuthManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.conn_params = {
            'database': 'finalquiztasy',
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'port': '3306'
        }
        self.current_user = None
        self.is_logged_in = False
        self.init_database()
        self._initialized = True

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
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

            cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR (255) UNIQUE NOT NULL,
                password_hash VARCHAR (255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

            # Create simplified player_stats table with only level
            cursor.execute('''CREATE TABLE IF NOT EXISTS player_stats
            (user_id INT PRIMARY KEY,
                level INT DEFAULT 1,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id))''')
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")

    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        """Validate email format using regex"""
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_pattern, email) is not None

    def validate_password(self, password):
        """Validate password meets minimum requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        return True, "Password is valid"

    def check_email_exists(self, email):
        """Check if an email already exists in the database"""
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone() is not None
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Database error checking email: {e}")
            return False

    def register(self, email, password):
        # Validate email format
        if not self.validate_email(email):
            return False, "Invalid email format"

        # Validate password requirements
        valid_password, password_message = self.validate_password(password)
        if not valid_password:
            return False, password_message

        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "Email already registered"

            # Insert new user
            hashed_password = self._hash_password(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, hashed_password)
            )
            conn.commit()

            # Get the last inserted ID
            user_id = cursor.lastrowid

            # Initialize player stats
            cursor.execute(
                "INSERT INTO player_stats (user_id) VALUES (%s)",
                (user_id,)
            )

            conn.commit()
            cursor.close()
            conn.close()
            return True, "Registration successful"
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"

    def login(self, email, password):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            hashed_password = self._hash_password(password)
            cursor.execute(
                "SELECT id, email FROM users WHERE email = %s AND password_hash = %s",
                (email, hashed_password)
            )
            user = cursor.fetchone()

            if user:
                self.current_user = {"id": user[0], "email": user[1]}
                self.is_logged_in = True
                print(f"User logged in: {self.current_user}")  # Debug log

                # Update last login time
                cursor.execute(
                    "UPDATE player_stats SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s",
                    (user[0],)
                )
                conn.commit()
                cursor.close()
                conn.close()
                return True, "Login successful"
            else:
                cursor.close()
                conn.close()
                return False, "Invalid email or password"
        except Exception as e:
            print(f"Login error: {e}")
            return False, f"Login failed: {str(e)}"

    def logout(self):
        """Log out the current user"""
        try:
            self.current_user = None
            self.is_logged_in = False  # Reset logged-in flag
            return True
        except Exception as e:
            print(f"Error during logout: {e}")
            return False

    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user

    def get_user_stats(self):
        """Get stats for the current user (only level now)"""
        if not self.current_user:
            return None
        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT level FROM player_stats WHERE user_id = %s",
                (self.current_user["id"],)
            )
            stats = cursor.fetchone()

            cursor.close()
            conn.close()

            if stats:
                return {
                    "level": stats[0]
                }
            return None
        except Exception as e:
            print(f"Error fetching user stats: {e}")
            return None
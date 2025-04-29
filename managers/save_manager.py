import mysql.connector
from managers.auth_manager import AuthManager


class SaveManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SaveManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.auth_manager = AuthManager()
        self.conn_params = self.auth_manager.conn_params
        self.init_database()
        self._initialized = True

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # Connect to the database
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Create game_progress table
            cursor.execute('''CREATE TABLE IF NOT EXISTS game_progress
            (
                user_id
                INT
                PRIMARY
                KEY,
                current_level
                INT
                DEFAULT
                1,
                hero_type
                VARCHAR
                              (
                50
                              ) DEFAULT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY
                              (
                                  user_id
                              ) REFERENCES users
                              (
                                  id
                              ))''')

            conn.commit()
            cursor.close()
            conn.close()
            print("Save Manager: Game progress table initialized successfully")
        except Exception as e:
            print(f"Save Manager: Database initialization error: {e}")

    def save_progress(self, level, hero_type):
        """Save the player's progress"""
        current_user = self.auth_manager.get_current_user()
        if not current_user:
            print("Save Manager: No user logged in, cannot save progress")
            return False

        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Check if user already has progress data
            cursor.execute(
                "SELECT * FROM game_progress WHERE user_id = %s",
                (current_user["id"],)
            )
            exists = cursor.fetchone()

            if exists:
                # Update existing progress
                cursor.execute(
                    "UPDATE game_progress SET current_level = %s, hero_type = %s WHERE user_id = %s",
                    (level, hero_type, current_user["id"])
                )
            else:
                # Insert new progress
                cursor.execute(
                    "INSERT INTO game_progress (user_id, current_level, hero_type) VALUES (%s, %s, %s)",
                    (current_user["id"], level, hero_type)
                )

            conn.commit()
            cursor.close()
            conn.close()
            print(f"Save Manager: Progress saved - Level: {level}, Hero: {hero_type}")
            return True
        except Exception as e:
            print(f"Save Manager: Error saving progress: {e}")
            return False

    def load_progress(self):
        """Load the player's progress"""
        current_user = self.auth_manager.get_current_user()
        if not current_user:
            print("Save Manager: No user logged in, cannot load progress")
            return None

        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT current_level, hero_type FROM game_progress WHERE user_id = %s",
                (current_user["id"],)
            )
            progress = cursor.fetchone()

            cursor.close()
            conn.close()

            if progress:
                return {
                    "level": progress[0],
                    "hero_type": progress[1]
                }
            else:
                print("Save Manager: No progress found for current user")
                return None
        except Exception as e:
            print(f"Save Manager: Error loading progress: {e}")
            return None

    def has_saved_progress(self):
        """Check if the current user has any saved progress"""
        progress = self.load_progress()
        return progress is not None

    def update_level(self, level):
        """Update only the level"""
        current_user = self.auth_manager.get_current_user()
        if not current_user:
            print("Save Manager: No user logged in, cannot update level")
            return False

        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Check if user already has progress data
            cursor.execute(
                "SELECT hero_type FROM game_progress WHERE user_id = %s",
                (current_user["id"],)
            )
            result = cursor.fetchone()

            if result:
                hero_type = result[0]
                # Update existing progress
                cursor.execute(
                    "UPDATE game_progress SET current_level = %s WHERE user_id = %s",
                    (level, current_user["id"])
                )
                conn.commit()
                cursor.close()
                conn.close()
                print(f"Save Manager: Level updated to {level}")
                return True
            else:
                cursor.close()
                conn.close()
                print("Save Manager: No existing progress found to update level")
                return False
        except Exception as e:
            print(f"Save Manager: Error updating level: {e}")
            return False

    def reset_progress(self):
        """Reset the player's progress to level 1"""
        current_user = self.auth_manager.get_current_user()
        if not current_user:
            print("Save Manager: No user logged in, cannot reset progress")
            return False

        try:
            conn = mysql.connector.connect(**self.conn_params)
            cursor = conn.cursor()

            # Check if the user has existing progress
            cursor.execute(
                "SELECT hero_type FROM game_progress WHERE user_id = %s",
                (current_user["id"],)
            )
            result = cursor.fetchone()

            if result:
                # Get the current hero_type to maintain it
                hero_type = result[0]

                # Reset the level to 1 but keep the same hero_type
                cursor.execute(
                    "UPDATE game_progress SET current_level = 1 WHERE user_id = %s",
                    (current_user["id"],)
                )
                conn.commit()
                cursor.close()
                conn.close()
                print(f"Save Manager: Progress reset to level 1 for user {current_user['id']}")
                return True
            else:
                # No progress to reset
                cursor.close()
                conn.close()
                print("Save Manager: No existing progress found to reset")
                return False
        except Exception as e:
            print(f"Save Manager: Error resetting progress: {e}")
            return False

    def reset_game_state(self):
        """Reset in-memory game state without affecting the database"""
        print("Save Manager: Game state reset")
        # This method doesn't need to do anything with the database
        # It's a hook for the game to know when to reset its state
        return True
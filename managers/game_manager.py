import pygame
from managers.auth_manager import AuthManager

class GameManager:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.current_screen = None
        self.game_running = True
        self.user_preferences = {}
        self.game_stats = {}

    def set_current_screen(self, screen_name):
        """Set the currently active screen"""
        self.current_screen = screen_name
        print(f"Screen changed to: {screen_name}")

    def get_current_screen(self):
        """Get the currently active screen"""
        return self.current_screen

    def get_current_user(self):
        """Get the currently logged in user from auth manager"""
        return self.auth_manager.get_current_user()

    def is_user_logged_in(self):
        """Check if a user is currently logged in"""
        return self.auth_manager.is_logged_in

    def logout_user(self):
        """Log out the current user"""
        return self.auth_manager.logout()

    def login_user(self, email, password):
        """Log in a user with the provided credentials"""
        return self.auth_manager.login(email, password)

    def register_user(self, email, password):
        """Register a new user with the provided credentials"""
        return self.auth_manager.register(email, password)

    def get_user_stats(self):
        """Get stats for the current user"""
        return self.auth_manager.get_user_stats()

    def save_user_preferences(self, preferences):
        """Save user preferences"""
        self.user_preferences = preferences

    def get_user_preferences(self):
        """Get user preferences"""
        return self.user_preferences

    def update_game_stats(self, stats_update):
        """Update game statistics"""
        self.game_stats.update(stats_update)
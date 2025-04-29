import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from managers.audio_manager import AudioManager
from managers.auth_manager import AuthManager
from managers.game_manager import GameManager
from ui.menu_background import MenuBackground
from ui.main_menu import MainMenu
from ui.game_modes import GameModes
from ui.hero_selection import HeroSelection
from ui.pvp_hero_selection import PVPHeroSelection
from maps.map import Map
from gameplay.battle import Battle
from gameplay.pvp import PVP
from gameplay.custom import CustomMode

class FinalQuiztasy:
    def __init__(self):
        pygame.init()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Final Quiztasy')

        # Set window icon
        icon_path = os.path.join(self.script_dir, "images", "logo", "logo.png")
        if os.path.exists(icon_path):
            window_icon = pygame.image.load(icon_path)
            pygame.display.set_icon(window_icon)

        # Game state
        self.running = True
        self.auth_manager = AuthManager()
        self.game_manager = GameManager()
        self.game_manager.auth_manager = self.auth_manager

        # Initialize game components
        self.setup_background()
        self.setup_audio()
        self.main_menu = MainMenu(self.screen, self.audio_manager, self.script_dir, exit_callback=self.exit_game, game_instance=self)
        self.hero_selection = HeroSelection(self, self.background_menu)
        self.pvp_hero_selection = PVPHeroSelection(self, self.background_menu)

        # Pass game_manager instead of auth_manager to ensure consistent use of the singleton
        self.game_modes = GameModes(self.screen, self.audio_manager, self.script_dir, scale=1.0, game_instance=self, auth_manager=self.game_manager.auth_manager)
        self.custom_mode = CustomMode(self.screen, self.audio_manager, self.script_dir, game_instance=self)
        self.lspu_map = None
        self.battle = None
        self.pvp = PVP(self)

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

    def setup_background(self):
        # Initialize background video
        self.background_menu = MenuBackground(
            os.path.join(self.script_dir, "assets", "videos", "background", "backgroundMenu.mp4"), speed=0.3)

    def setup_audio(self):
        # Initialize audio manager
        self.audio_manager = AudioManager(os.path.join(self.script_dir, "assets", "audio", "ost", "menuOst.mp3"),
                                          os.path.join(self.script_dir, "assets", "audio", "sfx","click_sound_button.mp3"))
        self.audio_manager.play_music()  # Play The OST Music

    def exit_game(self):
        """Callback function to exit the game."""
        self.running = False

    def map(self, hero_ost_path):
        """Stops menu music, plays hero-specific map music, and loads the map."""
        if not hasattr(self, "selected_hero") or not self.selected_hero:
            self.selected_hero = "boy"  # Default to boy if no hero was selected

        # Stop the main menu music
        if self.audio_manager:
            self.audio_manager.stop_music()

        # Update the AudioManager with the new OST instead of creating a new instance
        self.audio_manager.music_path = hero_ost_path
        if self.audio_manager.audio_enabled:
            self.audio_manager.play_music()

        # Create the LSPU map
        self.lspu_map = Map(self.screen, self.script_dir, self.return_to_main_menu, self.audio_manager, self.selected_hero, game_instance=self)
        self.hero_selection.hide()
        self.lspu_map.run()

        # Stop hero-specific map music when exiting
        self.audio_manager.stop_music()

        # Resume main menu music when returning
        self.audio_manager.music_path = os.path.join(self.script_dir, "assets", "audio", "ost", "menuOst.mp3")
        if self.audio_manager.audio_enabled:
            self.audio_manager.play_music()

    def start_battle(self, level, player_type):
        """Starts the battle when entering a level"""
        self.battle = Battle(self.screen, self.script_dir, level, player_type, self.audio_manager, game_instance=self)
        self.battle.run()

    def return_to_main_menu(self):
        """Callback function to return to the main menu."""
        print("Switching to main menu")
        self.running_map = False  # Stop map loop if it's running
        self.main_menu.show()  # Ensure the main menu appears
        # Also make sure to reset any necessary states
        if hasattr(self, 'lspu_map'):
            self.lspu_map = None
        if hasattr(self, 'battle'):
            self.battle = None

    # Add methods to access auth_manager functionality through game_manager
    def is_user_logged_in(self):
        """Check if a user is currently logged in"""
        return self.game_manager.is_user_logged_in()

    def get_current_user(self):
        """Get the currently logged in user"""
        return self.game_manager.get_current_user()

    def login_user(self, email, password):
        """Log in a user with the provided credentials"""
        return self.game_manager.login_user(email, password)

    def register_user(self, email, password):
        """Register a new user with the provided credentials"""
        return self.game_manager.register_user(email, password)

    def logout_user(self):
        """Log out the current user"""
        return self.game_manager.logout_user()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Pass events to the appropriate screen based on visibility
            if hasattr(self, 'hero_selection') and self.hero_selection.visible:
                self.hero_selection.update(event)
            elif hasattr(self, 'pvp_hero_selection') and self.pvp_hero_selection.visible:
                self.pvp_hero_selection.update(event)
            elif hasattr(self, 'custom_mode') and self.custom_mode.visible:  # Add this check
                self.custom_mode.update(event)
            elif hasattr(self, 'game_modes') and self.game_modes.visible:
                self.game_modes.update(event)
            else:
                self.main_menu.handle_events(event)

    def draw(self):
        # Draw background
        frame_surface = self.background_menu.get_frame()
        frame_surface = pygame.transform.scale(frame_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(frame_surface, (0, 0))

        # Draw the appropriate UI screen based on visibility
        if hasattr(self, 'hero_selection') and self.hero_selection.visible:
            self.hero_selection.draw()
        elif hasattr(self, 'pvp_hero_selection') and self.pvp_hero_selection.visible:
            self.pvp_hero_selection.draw()
        elif hasattr(self, 'custom_mode') and self.custom_mode.visible:  # Add this check
            self.custom_mode.draw()
        elif hasattr(self, 'game_modes') and self.game_modes.visible:
            self.game_modes.draw()
        else:
            self.main_menu.draw()

    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        # Clean up resources
        self.background_menu.close()
        pygame.quit()


if __name__ == "__main__":
    game = FinalQuiztasy()
    game.run()
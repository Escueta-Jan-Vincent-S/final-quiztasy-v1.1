import pygame
import os
from ui.button import Button
from .back_button import BackButton
from managers.save_manager import SaveManager


class GameModes:
    def __init__(self, screen, audio_manager, script_dir, scale=0.5, game_instance=None, auth_manager=None):
        self.game_instance = game_instance  # Store the game instance
        self.screen = screen
        self.audio_manager = audio_manager
        self.visible = False  # Controls visibility
        self.scale = scale  # Scaling factor for buttons
        self.show_new_continue = False  # Controls New/Continue selection
        self.auth_manager = auth_manager
        self.save_manager = SaveManager()
        current_user = self.auth_manager.get_current_user() if self.auth_manager else None

        # Specific scales for border and new/continue buttons
        self.border_scale = 0.5  # Customize this value for the border
        self.new_continue_scale = 0.6  # Customize this value for new/continue buttons

        # Define button positions
        self.positions = {
            "sp": (960, 280),  # Middle top
            "pvp": (480, 800),  # Bottom left
            "custom": (1440, 800)  # Bottom right
        }

        # Load buttons with scaling
        self.buttons = {
            "sp": self.create_button(script_dir, "sp", self.positions["sp"]),
            "pvp": self.create_button(script_dir, "pvp", self.positions["pvp"]),
            "custom": self.create_button(script_dir, "custom", self.positions["custom"])
        }

        # New/Continue selection screen assets with custom scaling for border
        border_image = pygame.image.load(
            os.path.join(script_dir, "assets", "images", "buttons", "game modes", "new or continue", "border.png"))
        # Scale the border image
        original_border_size = border_image.get_rect().size
        scaled_border_width = int(original_border_size[0] * self.border_scale)
        scaled_border_height = int(original_border_size[1] * self.border_scale)
        self.new_continue_border = pygame.transform.scale(border_image, (scaled_border_width, scaled_border_height))
        self.new_continue_border_rect = self.new_continue_border.get_rect(center=(960, 540))

        # Create new/continue buttons with custom scaling
        self.new_button = self.create_button(script_dir, "new", (905, 480), action=self.start_new_game,
                                             button_scale=self.new_continue_scale)

        # Load continue button images (normal, hover, locked)
        continue_img_path = os.path.join(script_dir, "assets", "images", "buttons", "game modes", "new or continue",
                                         "continue_btn_img.png")
        continue_hover_path = os.path.join(script_dir, "assets", "images", "buttons", "game modes", "new or continue",
                                           "continue_btn_hover.png")
        continue_locked_path = os.path.join(script_dir, "assets", "images", "buttons", "game modes", "new or continue",
                                            "continue_btn_locked.png")

        # Create continue button (will be updated based on saved progress)
        self.continue_button = Button(
            905, 600, continue_img_path, continue_hover_path,
            action=self.continue_game, scale=self.new_continue_scale,
            audio_manager=self.audio_manager
        )

        # Store locked button image
        self.continue_locked_img = pygame.image.load(continue_locked_path)
        original_size = self.continue_locked_img.get_rect().size
        scaled_width = int(original_size[0] * self.new_continue_scale)
        scaled_height = int(original_size[1] * self.new_continue_scale)
        self.continue_locked_img = pygame.transform.scale(self.continue_locked_img, (scaled_width, scaled_height))

        # Add Back button
        self.back_button = BackButton(self.screen, script_dir, self.go_back, audio_manager=self.audio_manager,
                                      position=(100, 100), scale=0.25)

    def play_single_player(self):
        if not self.auth_manager:  # Check if auth_manager is available
            print("DEBUG: AuthManager is not initialized.")
            return

        current_user = self.auth_manager.get_current_user()

        if not current_user:
            print("DEBUG: No user is logged in. Please log in first.")
            return

        print(f"Playing single-player mode as {current_user}")
        self.show_new_continue = True  # Show new/continue prompt

        has_progress = self.save_manager.has_saved_progress()
        self.update_continue_button(has_progress)

        for button in self.buttons.values():
            button.active = False  # Disable background buttons when prompt is active

    def update_continue_button(self, has_progress):
        """Update the continue button based on whether the user has saved progress"""
        if has_progress:
            # Enable continue button
            self.continue_button.active = True
        else:
            # Disable continue button and use locked image
            self.continue_button.active = False
            self.continue_button.original_img = self.continue_locked_img
            self.continue_button.image = self.continue_locked_img

    def play_pvp(self):
        print("Playing player-vs-player mode")
        self.hide()  # Hide game modes
        if self.game_instance:
            if hasattr(self.game_instance, 'pvp_hero_selection'):
                self.game_instance.pvp_hero_selection.show()

    def play_custom_mode(self):
        print("Entering custom mode")
        self.hide()  # Hide the game modes UI

        # Show the custom mode
        if self.game_instance and hasattr(self.game_instance, 'custom_mode'):
            self.game_instance.custom_mode.show()

        # Hide main menu elements
        if self.game_instance:
            main_menu = self.game_instance
            if hasattr(self.game_instance, 'main_menu'):
                main_menu = self.game_instance.main_menu

            if main_menu:
                main_menu.show_game_logo = False
                main_menu.visible = False

    def start_new_game(self):
        print("Starting a new game...")

        # Reset user progress data to level 1
        if self.auth_manager and self.auth_manager.get_current_user():
            current_user = self.auth_manager.get_current_user()
            print(f"Resetting save data for user: {current_user['email']}")

            # Reset save data to initial state (level 1)
            self.save_manager.reset_progress()
            print("Save data reset to level 1")

            # Reset any level states in the game instance if they exist
            if self.game_instance and hasattr(self.game_instance, 'lspu_map') and self.game_instance.lspu_map:
                # Lock all levels except level 1
                for level in self.game_instance.lspu_map.levels.levels:
                    if level["id"] > 1:  # Lock all levels except level 1
                        level["unlocked"] = False
                    else:
                        level["unlocked"] = True
                print("Game map levels reset")

        self.show_new_continue = False
        for button in self.buttons.values():
            button.active = True  # Re-enable buttons when leaving prompt

        if self.game_instance:
            if hasattr(self.game_instance, 'hero_selection'):
                self.game_instance.hero_selection.show()
            elif hasattr(self.game_instance, 'game_instance') and hasattr(self.game_instance.game_instance,
                                                                          'hero_selection'):
                self.game_instance.game_instance.hero_selection.show()

    def continue_game(self):
        """Continue previous game if progress exists"""
        if not self.continue_button.active:
            print("Continue button is locked - no saved progress")
            return

        print("Continuing previous game...")
        self.show_new_continue = False

        # Load saved progress
        progress = self.save_manager.load_progress()
        if progress and self.game_instance:
            print(f"Loading saved progress: Level {progress['level']}, Hero: {progress['hero_type']}")

            # Set the selected hero in game instance
            self.game_instance.selected_hero = progress['hero_type']

            # Unlock levels up to the saved level
            if hasattr(self.game_instance, 'lspu_map'):
                if self.game_instance.lspu_map is None:
                    # Map hasn't been created yet, will handle it when loading the map
                    pass

            # Re-enable buttons when leaving prompt
            for button in self.buttons.values():
                button.active = True

            # Get hero's OST path
            hero_ost_path = os.path.join(self.game_instance.script_dir, "assets", "audio", "ost",
                                         progress['hero_type'], f"{progress['hero_type']}_map_ost.mp3")

            # Load the map directly with the saved hero
            self.game_instance.map(hero_ost_path)

            # After the map loads, unlock levels up to the saved level
            if hasattr(self.game_instance, 'lspu_map') and self.game_instance.lspu_map:
                for level_id in range(1, progress['level'] + 1):
                    self.game_instance.lspu_map.levels.unlock_level(level_id)
        else:
            print("No saved progress found")

    def create_button(self, script_dir, name, position, action=None, button_scale=None):
        """Helper method to create buttons with scaling."""
        # Use the provided scale or default to the class scale
        button_scale = button_scale if button_scale is not None else self.scale

        folder = "new or continue" if name in ["new", "continue"] else "modes"
        img_path = os.path.join(script_dir, "assets", "images", "buttons", "game modes", folder, f"{name}_btn_img.png")
        hover_path = os.path.join(script_dir, "assets", "images", "buttons", "game modes", folder,
                                  f"{name}_btn_hover.png")
        click_path = None if folder == "modes" else os.path.join(script_dir, "assets", "images", "buttons",
                                                                 "game modes", folder, f"{name}_btn_click.png")

        return Button(
            position[0], position[1], img_path, hover_path, click_path,
            action if action else lambda: self.on_click(name), scale=button_scale, audio_manager=self.audio_manager
        )

    def on_click(self, name):
        """Handles button clicks for game mode selection."""
        print(f"Button {name} clicked!")
        if name == "sp":
            self.play_single_player()
        elif name == "pvp":
            self.play_pvp()
        elif name == "custom":
            self.play_custom_mode()

    def go_back(self):
        """Handles Back button click."""
        print("Back button clicked!")
        if self.show_new_continue:
            self.show_new_continue = False  # Hide only the New/Continue selection
            for button in self.buttons.values():
                button.active = True  # Re-enable buttons when closing prompt
        else:
            self.hide()  # Hide game modes
            if self.game_instance:
                if hasattr(self.game_instance, 'main_menu'):
                    self.game_instance.main_menu.visible = True  # Explicitly set visible to True
                    self.game_instance.main_menu.show_game_logo = True  # Show logo
                    self.game_instance.main_menu.main_menu()  # Show main menu elements

    def update(self, event):
        if self.visible:
            # Only update back button and active prompt buttons when new/continue is shown
            if self.show_new_continue:
                self.new_button.update(event)
                # Only update continue button if it's active (if there's saved progress)
                if self.continue_button.active:
                    self.continue_button.update(event)
                self.back_button.update(event)
            else:
                # Update all buttons when not showing new/continue
                for button in self.buttons.values():
                    button.update(event)
                self.back_button.update(event)

    def draw(self):
        if self.visible:
            # Always draw the game mode buttons in the background
            for button in self.buttons.values():
                button.draw(self.screen)

            # Draw the new/continue prompt on top if active
            if self.show_new_continue:
                self.screen.blit(self.new_continue_border, self.new_continue_border_rect.topleft)
                self.new_button.draw(self.screen)

                # Always draw continue button, but it will look different if disabled
                self.continue_button.draw(self.screen)

            # Always draw the back button on top
            self.back_button.draw()

    def show(self):
        """Show the game mode selection."""
        self.visible = True
        self.show_new_continue = False  # Reset this when showing the menu
        for button in self.buttons.values():
            button.active = True

    def hide(self):
        """Hide the game mode selection."""
        self.visible = False
        self.show_new_continue = False  # Reset this when hiding the menu q
        for button in self.buttons.values():
            button.active = False
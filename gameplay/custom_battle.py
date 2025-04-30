import pygame
import time
import os
import random
from characters.player import Player
from managers.custom_manager import CustomManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_PATH
from .pause import Pause
from characters.enemy import MiniBoss, Boss


class CustomBattle:
    def __init__(self, screen, script_dir, question_set_name, audio_manager=None, game_instance=None):
        self.screen = screen
        self.script_dir = script_dir
        self.question_set_name = question_set_name
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.small_font = pygame.font.Font(FONT_PATH, 30)
        self.input_font = pygame.font.Font(FONT_PATH, 35)
        self.audio_manager = audio_manager
        self.game_instance = game_instance

        # Load custom questions
        self.custom_manager = CustomManager()
        self.questions = self.custom_manager.get_question_set_by_name(question_set_name)

        # Ensure we have at least 10 questions for a fair game
        if self.questions is None or len(self.questions) < 10:
            self.error_message = "Error: Need at least 10 questions to start a battle"
            print(self.error_message)
            self.questions = []
            self.running = False
            return

        # Randomize player type (boy or girl)
        self.player_type = random.choice(["boy", "girl"])
        print(f"Selected player type: {self.player_type}")

        # Initialize player and enemy
        self.player = Player(script_dir, self.player_type)

        # Enemy HP is based on number of questions
        enemy_hp = len(self.questions)
        if random.random() < 1:  # 80% chance of mini boss
            self.enemy = MiniBoss(script_dir, level=1, hp=enemy_hp, damage=1)

        # Battle state
        self.current_question_index = 0
        self.current_question = None
        self.user_answer = ""
        self.timer_start = 0
        self.time_left = 60  # 60 seconds per question
        self.battle_message = ""
        self.message_timer = 0
        self.input_active = True

        # Save the current music path for restoration later
        self.original_music = None
        if pygame.mixer.music.get_busy():
            # Store the path to menuOst.mp3 instead of determining by player type
            self.original_music = os.path.join(self.script_dir, "assets", "audio", "ost", "menuOst.mp3")
            print(f"Saved original music: {self.original_music}")

        # Initialize pause menu with specific callbacks
        self.pause_menu = Pause(
            screen,
            script_dir,
            audio_manager,
            menu_callback=self.return_to_menu_from_pause
        )

        # Initialize text input field
        self.input_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 300,  # x position
            SCREEN_HEIGHT - 150,  # y position
            600,  # width
            60  # height
        )
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_active  # Start with active color

        # Set up first question
        self.load_next_question()

        # Load and play battle music
        self.battle_music = self.load_battle_music()
        if self.battle_music:
            pygame.mixer.music.load(self.battle_music)
            pygame.mixer.music.play(-1)  # Loop the battle music

    def open_map_from_pause(self):
        """Handle opening map when selected from pause menu"""
        # Implement logic to open map
        print("Opening map from pause menu")
        self.running = False  # End current battle

    def return_to_menu_from_pause(self):
        """Handle returning to main menu when selected from pause menu"""
        print("Returning to main menu from pause menu")
        self.running = False  # End current battle
        if self.game_instance:
            # Call the return_to_main_menu method instead of main_menu
            self.game_instance.return_to_main_menu()
        else:
            print("No game instance")

    def load_battle_music(self):
        """Load the appropriate battle music based on the player type."""
        if self.player_type == "boy":
            return os.path.join(self.script_dir, "assets", "audio", "ost", "battle", "boy_battle_ost.mp3")
        elif self.player_type == "girl":
            return os.path.join(self.script_dir, "assets", "audio", "ost", "battle", "girl_battle_ost.mp3")
        return None

    def stop_battle_music(self):
        """Stop the battle music and restore the original music."""
        pygame.mixer.music.stop()

        # Restore the original music if it exists
        if self.original_music and os.path.exists(self.original_music):
            print(f"Restoring original music: {self.original_music}")
            pygame.mixer.music.load(self.original_music)
            pygame.mixer.music.play(-1)  # Loop the original music
        else:
            print("No original music to restore")

    def load_next_question(self):
        """Loads the next question from the custom question set"""
        if self.current_question_index < len(self.questions):
            self.current_question = self.questions[self.current_question_index]
            self.timer_start = time.time()
            self.time_left = 60  # Reset timer
            self.user_answer = ""  # Clear previous answer
            self.input_active = True  # Enable input for new question
            print(f"Loaded question: {self.current_question['question']}")
        else:
            # No more questions, player wins
            self.battle_message = "Victory! You answered all questions!"
            print("All questions completed")
            self.input_active = False
            # Wait a bit before ending the battle
            pygame.time.delay(2000)
            self.running = False

    def handle_events(self):
        """Handle user input during battle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Only process other events if not paused
            if not self.pause_menu.is_paused():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if input box is clicked
                    if self.input_rect.collidepoint(event.pos) and self.input_active:
                        self.color = self.color_active
                    else:
                        self.color = self.color_passive

                elif event.type == pygame.KEYDOWN and self.input_active:
                    # Handle text input
                    if event.key == pygame.K_RETURN:
                        # Submit answer when Enter is pressed
                        self.check_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove last character if backspace is pressed
                        self.user_answer = self.user_answer[:-1]
                    else:
                        # Add character to answer
                        self.user_answer += event.unicode

            # Always process pause menu events
            self.pause_menu.update(event)

    def check_answer(self):
        """Checks if the user's answer is correct"""
        if not self.current_question:
            return

        # Get correct answer from current question
        correct_answer = str(self.current_question['answer']).strip().lower()
        user_answer = self.user_answer.strip().lower()

        if user_answer == correct_answer:
            # Correct answer - enemy takes damage
            self.enemy.take_damage(1)
            self.battle_message = "Correct! Enemy takes damage!"

            if self.enemy.hp <= 0:
                self.battle_message = "Victory! You defeated the enemy!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Move to next question
                self.current_question_index += 1
                self.load_next_question()
        else:
            # Wrong answer - player takes damage
            self.player.take_damage(1)  # Always 1 damage for simplicity
            self.battle_message = f"Wrong! You take 1 damage!"

            if self.player.hp <= 0:
                self.battle_message = "Defeat! You have been defeated!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Move to next question
                self.current_question_index += 1
                self.load_next_question()

        # Set message timer
        self.message_timer = time.time()

    def update_timer(self):
        """Updates the time left to answer the question"""
        # If paused, don't update anything
        if self.pause_menu.is_paused():
            return

        # Adjust timer for any time spent paused
        paused_time = self.pause_menu.get_total_paused_time()
        if paused_time > 0:
            self.timer_start += paused_time  # Move the start time forward by paused duration

        # Calculate remaining time
        elapsed = time.time() - self.timer_start
        self.time_left = max(0, 60 - elapsed)  # 60 seconds per question

        # If time runs out, treat as wrong answer
        if self.time_left <= 0 and self.running and self.input_active:
            self.battle_message = "Time's up! You take damage!"
            self.player.take_damage(1)
            self.input_active = False  # Disable input when time's up

            if self.player.hp <= 0:
                self.battle_message = "Defeat! You have been defeated!"
                # Wait a bit before ending the battle
                pygame.time.delay(2000)
                self.running = False  # End the battle
            else:
                # Move to next question after delay
                pygame.time.delay(1500)  # Show time's up message
                self.current_question_index += 1
                self.load_next_question()

            # Set message timer
            self.message_timer = time.time()

    def draw_background(self, screen):
        """Draw a simple background for the battle"""
        # Fill screen with a gradient background
        for i in range(SCREEN_HEIGHT):
            color_value = 50 + (i / SCREEN_HEIGHT * 50)
            pygame.draw.line(screen, (0, int(color_value), int(color_value * 2)),
                             (0, i), (SCREEN_WIDTH, i))

    def draw(self):
        """Draws the battle screen"""
        # Draw background
        self.draw_background(self.screen)

        # Draw player and enemy
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # Draw timer
        timer_text = self.font.render(f"Time: {int(self.time_left)}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (timer_rect.x - 10, timer_rect.y - 10,
                          timer_rect.width + 20, timer_rect.height + 20))
        self.screen.blit(timer_text, timer_rect)

        # Draw question box
        question_box = pygame.Rect(50, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), question_box)
        pygame.draw.rect(self.screen, (255, 255, 255), question_box, 3)

        # Draw question text
        if self.current_question:
            question_text = self.font.render(self.current_question["question"], True, (255, 255, 255))
            question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250))
            self.screen.blit(question_text, question_rect)

        # Draw input field if not paused
        if not self.pause_menu.is_paused() and self.input_active:
            pygame.draw.rect(self.screen, self.color, self.input_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)

            # Render input text
            input_surface = self.input_font.render(self.user_answer, True, (255, 255, 255))

            # Ensure input text fits within input box by limiting width
            max_width = self.input_rect.width - 20
            if input_surface.get_width() > max_width:
                visible_text = self.user_answer
                while self.input_font.render(visible_text, True, (255, 255, 255)).get_width() > max_width:
                    visible_text = visible_text[1:]  # Remove first character
                input_surface = self.input_font.render(visible_text, True, (255, 255, 255))

            # Position text in input box
            text_pos = (self.input_rect.x + 10,
                        self.input_rect.y + (self.input_rect.height - input_surface.get_height()) // 2)
            self.screen.blit(input_surface, text_pos)

        # Draw battle message
        if self.battle_message and time.time() - self.message_timer < 2:
            message_text = self.font.render(self.battle_message, True, (255, 255, 0))
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (message_rect.x - 10, message_rect.y - 10,
                              message_rect.width + 20, message_rect.height + 20))
            self.screen.blit(message_text, message_rect)

        # Draw question counter
        if self.questions:
            counter_text = self.small_font.render(
                f"Question {self.current_question_index + 1}/{len(self.questions)}",
                True, (255, 255, 255)
            )
            counter_rect = counter_text.get_rect(topright=(SCREEN_WIDTH - 100, 20))
            self.screen.blit(counter_text, counter_rect)

        # Draw pause menu (button and overlay if paused)
        self.pause_menu.draw()

    def run(self):
        """Main battle loop"""
        # Check if we have enough questions to start
        if not self.questions or len(self.questions) < 10:
            print(f"Not enough questions to start battle: {len(self.questions) if self.questions else 0}/10")
            return False

        while self.running:
            # Handle events
            self.handle_events()

            # Update timer
            self.update_timer()

            # Draw battle
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Stop battle music and restore original music when the battle ends
        self.stop_battle_music()

        # Return result (True for victory, False for defeat)
        return self.enemy.hp <= 0
import pygame
import os
import sys
import datetime
from managers.custom_manager import CustomManager
from .custom_ui import CustomUI
from .custom_battle import CustomBattle


class CustomMode:
    def __init__(self, screen, audio_manager, script_dir, scale=0.5, game_instance=None):
        self.game_instance = game_instance
        self.screen = screen
        self.audio_manager = audio_manager
        self.visible = False
        self.scale = scale
        self.script_dir = script_dir

        # Initial save slots (can be loaded from storage later)
        self.save_slots = []
        self.selected_slot = None

        # Question creation state
        self.creating_question = False
        self.current_questions = []  # Store questions during creation

        # Create UI
        self.ui = CustomUI(screen, audio_manager, script_dir, scale, self)

        # Get the CustomManager singleton instance
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from managers.custom_manager import CustomManager
        self.custom_manager = CustomManager()

    def create_question(self):
        """Handle create button click."""
        print("Create Question Clicked")
        # Show the question creation interface
        self.creating_question = True
        self.current_questions = []
        self.ui.reset_inputs()
        self.ui.set_status("")

    def next_question(self):
        """Save current question and clear inputs for next question."""
        inputs = self.ui.get_input_values()
        question = inputs["question"]
        answer = inputs["answer"]

        if question and answer:
            self.current_questions.append({"question": question, "answer": answer})
            self.ui.reset_inputs()
            self.ui.set_status(f"Question added successfully. Total: {len(self.current_questions)}",
                               pygame.Color('green'))
        else:
            self.ui.set_status("Please enter both question and answer before proceeding", pygame.Color('red'))

    def done_creating(self):
        """Finish creating questions and save to database."""
        # First check if there are any questions or if current fields are filled
        inputs = self.ui.get_input_values()
        question = inputs["question"]
        answer = inputs["answer"]

        # Add the current question if fields are filled
        if question and answer:
            self.current_questions.append({"question": question, "answer": answer})

        if not self.current_questions:
            self.ui.set_status("Please add at least one question before finishing", pygame.Color('red'))
            return

        # Check if we have at least 10 questions for battle
        if len(self.current_questions) < 10:
            self.ui.set_status("You need at least 10 questions for a battle. Please add more.", pygame.Color('red'))
            return

        # Generate a name based on current date/time
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        question_set_name = f"Questions - {current_date}"

        # Use game instance's save_question_set method for consistent user handling
        if self.game_instance and hasattr(self.game_instance, 'save_question_set'):
            self.game_instance.save_question_set(question_set_name, self.current_questions)
            print(f"Saved question set via game instance")
        else:
            # Fallback to direct database save if game instance method not available
            user_id = None
            if self.game_instance and hasattr(self.game_instance, 'get_current_user'):
                current_user = self.game_instance.get_current_user()
                if current_user:
                    user_id = current_user.get('id')
                    print(f"Saving questions for user ID: {user_id}")
            self.custom_manager.save_question_set(question_set_name, self.current_questions, user_id)

        # Update slot list using game instance method if available
        if self.game_instance and hasattr(self.game_instance, 'get_question_sets'):
            self.save_slots = self.game_instance.get_question_sets()
        else:
            # Fallback to direct database query if game instance method not available
            user_id = None
            if self.game_instance and hasattr(self.game_instance, 'get_current_user'):
                current_user = self.game_instance.get_current_user()
                if current_user:
                    user_id = current_user.get('id')
            self.save_slots = self.custom_manager.get_question_sets(user_id)
        self.ui.update_max_scroll(self.save_slots)

        self.ui.set_status(f"Saved {len(self.current_questions)} questions as '{question_set_name}'",
                           pygame.Color('green'))

        # Set timer to exit question creation mode after showing success message
        pygame.time.set_timer(pygame.USEREVENT + 2, 1500)  # Exit after 1.5 seconds

    def delete_question_set(self, slot_index):
        """Delete the question set at the given index."""
        if 0 <= slot_index < len(self.save_slots):
            slot_name = self.save_slots[slot_index]
            print(f"Deleting question set: {slot_name}")

            # Get user ID and delete the question set
            if self.game_instance and hasattr(self.game_instance, 'get_current_user'):
                current_user = self.game_instance.get_current_user()
                user_id = current_user.get('id') if current_user else None
            else:
                user_id = None

            # Delete from database
            if self.custom_manager.delete_question_set(slot_name, user_id):
                # Remove from local list
                self.remove_slot(slot_index)

                # Show status message
                self.ui.set_status(f"Question set '{slot_name}' deleted successfully", pygame.Color('red'))
            else:
                # Show error message
                self.ui.set_status("Failed to delete question set", pygame.Color('red'))

    def start_battle(self):
        """Start a battle with the currently selected question set."""
        if self.selected_slot is None or self.selected_slot >= len(self.save_slots):
            self.ui.set_status("Please select a question set first", pygame.Color('red'))
            return

        # Get the selected question set name
        question_set_name = self.save_slots[self.selected_slot]
        print(f"Starting battle with question set: {question_set_name}")

        # Check if the question set has at least 10 questions
        questions = self.custom_manager.get_question_set_by_name(question_set_name)
        if not questions or len(questions) < 10:
            self.ui.set_status(
                f"Need at least 10 questions to battle. This set has {len(questions) if questions else 0}.",
                pygame.Color('red'))
            return

        # Hide custom mode UI
        self.visible = False

        # Create and run the battle
        custom_battle = CustomBattle(
            self.screen,
            self.script_dir,
            question_set_name,
            self.audio_manager,
            self.game_instance
        )

        result = custom_battle.run()

        # Show custom mode UI again after battle ends
        self.visible = True

        # Display battle result
        if result:
            self.ui.set_status("Battle Won! Congratulations!", pygame.Color('green'))
        else:
            self.ui.set_status("Battle Lost! Try again!", pygame.Color('red'))

    def remove_slot(self, slot_index):
        """Remove a save slot."""
        if 0 <= slot_index < len(self.save_slots):
            print(f"Removing slot: {self.save_slots[slot_index]}")
            self.save_slots.pop(slot_index)
            if self.selected_slot == slot_index:
                self.selected_slot = None
            elif self.selected_slot is not None and self.selected_slot > slot_index:
                self.selected_slot -= 1
            self.ui.update_max_scroll(self.save_slots)

    def go_back(self):
        """Handle back button click."""
        if self.creating_question:
            # If in question creation mode, go back to slot selection
            self.creating_question = False
            return

        print("Back button clicked!")
        self.hide()
        # Return to game modes
        if self.game_instance and hasattr(self.game_instance, 'game_modes'):
            self.game_instance.game_modes.show()

            if hasattr(self.game_instance, 'main_menu'):
                self.game_instance.main_menu.show_game_logo = False

    def update(self, event):
        """Update UI elements and handle events."""
        if not self.visible:
            return

        # Check if timer to close question creation mode has elapsed
        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Stop the timer
            self.creating_question = False
            return

        # Update UI and get any actions
        result = self.ui.update(event, self.creating_question, self.save_slots, self.selected_slot)

        # Handle actions returned from UI
        if result:
            if result["action"] == "delete_slot":
                self.delete_question_set(result["index"])
            elif result["action"] == "select_slot":
                self.selected_slot = result["index"]
            elif result["action"] == "start_battle":
                self.start_battle()

    def draw(self):
        """Draw all UI elements."""
        if not self.visible:
            return

        self.ui.draw(self.creating_question, self.save_slots, self.selected_slot, self.current_questions)

    def show(self):
        """Show the custom mode screen."""
        self.visible = True

        # Use game instance's get_question_sets method for consistent user handling
        if self.game_instance and hasattr(self.game_instance, 'get_question_sets'):
            self.save_slots = self.game_instance.get_question_sets()
        else:
            # Fallback to direct database query if game instance method not available
            user_id = None
            if self.game_instance and hasattr(self.game_instance, 'get_current_user'):
                current_user = self.game_instance.get_current_user()
                if current_user:
                    user_id = current_user.get('id')
            self.save_slots = self.custom_manager.get_question_sets(user_id)
        self.ui.update_max_scroll(self.save_slots)
        self.ui.show()

    def hide(self):
        """Hide the custom mode screen."""
        self.visible = False
        self.creating_question = False
        self.ui.hide()
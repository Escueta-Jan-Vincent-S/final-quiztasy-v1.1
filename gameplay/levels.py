import pygame
import os
from characters.enemy import MiniBoss


class Level:
    def __init__(self, script_dir, level_id):
        self.script_dir = script_dir
        self.level_id = level_id

        level_settings = {
            1: {"name": "Level 1", "description": "Basta Level 1", "enemy_hp": 5, "enemy_damage": 1,
                "question_difficulty": 1, "timer_seconds": 10, "background": "level1_bg.png",
                "enemy_range": (1, 5)},  # Mini enemies 1-5 for level 1
            2: {"name": "Level 2", "description": "Basta Level 2", "enemy_hp": 6, "enemy_damage": 1,
                "question_difficulty": 1, "timer_seconds": 10, "background": "level2_bg.png",
                "enemy_range": (1, 5)},  # Mini enemies 6-10 for level 2
            3: {"name": "Level 3", "description": "Basta Level 3", "enemy_hp": 7, "enemy_damage": 1,
                "question_difficulty": 1, "timer_seconds": 10, "background": "level3_bg.png",
                "enemy_range": (1, 5)},  # Mini enemies 11-15 for level 3
            4: {"name": "Level 4", "description": "Basta Level 4", "enemy_hp": 8, "enemy_damage": 1,
                "question_difficulty": 1, "timer_seconds": 10, "background": "level4_bg.png",
                "enemy_range": (1, 5)},  # Mini enemies 16-19 for level 4
            5: {"name": "Level 5", "description": "Basta Level 5", "enemy_hp": 9, "enemy_damage": 1,
                "question_difficulty": 1, "timer_seconds": 10, "background": "level5_bg.png",
                "enemy_range": (1, 5)},
        }

        # Get settings for this level or default to level 1 if not found
        settings = level_settings.get(level_id, level_settings[1])

        self.name = settings["name"]
        self.description = settings["description"]
        self.enemy_hp = settings["enemy_hp"]
        self.enemy_damage = settings["enemy_damage"]
        self.question_difficulty = settings["question_difficulty"]
        self.timer_seconds = settings["timer_seconds"]
        self.enemy_range = settings["enemy_range"]

        # Load background for this level
        bg_filename = settings["background"]
        bg_path = f"{script_dir}/assets/images/battle/backgrounds/{bg_filename}"

        # Check if the background file exists, if not use default
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path)
        else:
            self.background = pygame.image.load(f"{script_dir}/assets/images/battle/backgrounds/level1_bg.png")

        self.background = pygame.transform.scale(self.background, (1920, 1080))

    def create_enemy(self):
        """Creates the enemy for this level with appropriate range"""
        return MiniBoss(
            self.script_dir,
            level=self.level_id,
            hp=self.enemy_hp,
            damage=self.enemy_damage,
            enemy_range=self.enemy_range
        )

    def get_timer_seconds(self):
        """Returns the number of seconds for the timer"""
        return self.timer_seconds

    def get_difficulty(self):
        """Returns the difficulty level for questions"""
        return self.question_difficulty

    def draw_background(self, screen):
        """Draws the level background"""
        screen.blit(self.background, (0, 0))
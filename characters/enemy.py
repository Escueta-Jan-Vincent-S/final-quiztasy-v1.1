import pygame
import os
import random
from settings import FONT_PATH


class Enemy:
    def __init__(self, script_dir, enemy_type="mini", level=1, hp=None, damage=None, enemy_range=None):
        self.script_dir = script_dir
        self.enemy_type = enemy_type
        self.level = level

        # Default enemy range if not specified
        self.enemy_range = enemy_range if enemy_range is not None else (1, 19)

        # HP and damage will be set by the level, but we provide defaults here
        self.hp = hp if hp is not None else 5  # Default HP
        self.max_hp = self.hp
        self.damage = damage if damage is not None else 1  # Default damage

        # Load the appropriate enemy image
        self.load_image()

        # Position the enemy on the right side of the screen
        self.rect = self.image.get_rect()
        self.rect.x = 1200  # Right side position
        self.rect.bottom = 700  # Adjust this value as needed

    def load_image(self):
        """Loads the appropriate enemy image based on type and level"""
        if self.enemy_type == "mini":
            # Select an enemy image from the range specified for this level
            min_id, max_id = self.enemy_range
            mini_id = random.randint(min_id, max_id)

            image_path = os.path.join(self.script_dir, "assets", "images", "battle", "enemy", "mini",
                                      f"mini_{mini_id}.png")

            # Check if the file exists, if not use a default enemy
            if not os.path.exists(image_path):
                image_path = os.path.join(self.script_dir, "assets", "images", "battle", "enemy", "mini", "mini_1.png")

        else:  # Boss type
            image_path = os.path.join(self.script_dir, "assets", "images", "battle", "enemy", "boss", "boss.png")

            # Check if the boss image exists, if not use a default mini enemy
            if not os.path.exists(image_path):
                image_path = os.path.join(self.script_dir, "assets", "images", "battle", "enemy", "mini", "mini_1.png")

        self.image = pygame.image.load(image_path)

        # Scale image if needed
        scale_factor = 2.5  # Adjust based on your image size
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor),
                                                         int(self.image.get_height() * scale_factor)))
        self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, amount):
        """Applies damage to the enemy"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp <= 0  # Returns True if enemy is defeated

    def get_damage_amount(self):
        """Returns the amount of damage this enemy deals"""
        return self.damage

    def draw(self, screen):
        """Draws the enemy on the screen"""
        screen.blit(self.image, self.rect)

        # Draw HP bar
        bar_width = 200
        bar_height = 20
        bar_x = screen.get_width() - bar_width - 100
        bar_y = screen.get_height() - bar_height - 320

        # Background (empty) bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Filled portion of the bar
        health_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

        # HP text
        font = pygame.font.Font(FONT_PATH, 20)
        hp_text = font.render(f"{self.hp}/{self.max_hp} HP", True, (255, 255, 255))
        screen.blit(hp_text, (bar_x + 10, bar_y + 2))


class MiniBoss(Enemy):
    def __init__(self, script_dir, level=1, hp=None, damage=None, enemy_range=None):
        super().__init__(script_dir, "mini", level, hp, damage, enemy_range)


class Boss(Enemy):
    def __init__(self, script_dir, level=1, hp=None, damage=None, enemy_range=None):
        super().__init__(script_dir, "boss", level, hp, damage, enemy_range)
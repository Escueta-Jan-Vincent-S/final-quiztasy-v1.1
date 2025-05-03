import pygame
import sys
import os


class MapCharacterMovement:
    def __init__(self, hero_type, script_dir, initial_x, initial_y):
        """Initialize character movement and animations."""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.hero_type = hero_type

        # Character position
        self.character_x = initial_x
        self.character_y = initial_y
        self.character_speed = 9  # 9 normal

        # Animation properties
        self.direction = "front"  # Default direction is front
        self.is_walking = False
        self.animation_frame = 0
        self.animation_cooldown = 100  # Milliseconds between animation frames
        self.last_animation_update = pygame.time.get_ticks()

        # Load character animations
        self.load_character_animations()

    def load_character_animations(self):
        """Load all character animation frames based on hero_type."""
        base_path = os.path.join(self.script_dir, "..", "assets", "images", "map", "animation", self.hero_type)

        # Initialize animation dictionaries
        self.animations = {
            "back": {"stand": None, "walk_left": None, "walk_right": None},
            "front": {"stand": None, "walk_left": None, "walk_right": None},
            "left": {"stand": None, "walk_left": None, "walk_right": None},
            "right": {"stand": None, "walk_left": None, "walk_right": None}
        }

        # Load back animations
        self.animations["back"]["stand"] = pygame.image.load(
            os.path.join(base_path, "back and walk", f"{self.hero_type}_back_stand.png")
        ).convert_alpha()
        self.animations["back"]["walk_left"] = pygame.image.load(
            os.path.join(base_path, "back and walk", f"{self.hero_type}_back_walkl.png")
        ).convert_alpha()
        self.animations["back"]["walk_right"] = pygame.image.load(
            os.path.join(base_path, "back and walk", f"{self.hero_type}_back_walkr.png")
        ).convert_alpha()

        # Load front animations
        self.animations["front"]["stand"] = pygame.image.load(
            os.path.join(base_path, "front and walk", f"{self.hero_type}_front_stand.png")
        ).convert_alpha()
        self.animations["front"]["walk_left"] = pygame.image.load(
            os.path.join(base_path, "front and walk", f"{self.hero_type}_front_walkl.png")
        ).convert_alpha()
        self.animations["front"]["walk_right"] = pygame.image.load(
            os.path.join(base_path, "front and walk", f"{self.hero_type}_front_walkr.png")
        ).convert_alpha()

        # Load sideway animations - with enhanced boy animations
        if self.hero_type == "boy":
            # Enhanced animations for boy character
            self.animations["left"]["stand"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_left_stand.png")
            ).convert_alpha()
            self.animations["left"]["walk_left"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_leftl_walk.png")
            ).convert_alpha()
            self.animations["left"]["walk_right"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_leftr_walk.png")
            ).convert_alpha()

            self.animations["right"]["stand"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_right_stand.png")
            ).convert_alpha()
            self.animations["right"]["walk_left"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_rightl_walk.png")
            ).convert_alpha()
            self.animations["right"]["walk_right"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_rightr_walk.png")
            ).convert_alpha()
        else:
            # Default animations for other characters
            self.animations["left"]["stand"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_left_stand.png")
            ).convert_alpha()
            self.animations["left"]["walk_left"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_left_walk.png")
            ).convert_alpha()
            self.animations["left"]["walk_right"] = self.animations["left"]["stand"]  # For girl, stand is walk_right

            self.animations["right"]["stand"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_right_stand.png")
            ).convert_alpha()
            self.animations["right"]["walk_left"] = pygame.image.load(
                os.path.join(base_path, "sideway and walk", f"{self.hero_type}_right_walk.png")
            ).convert_alpha()
            self.animations["right"]["walk_right"] = self.animations["right"]["stand"]  # For girl, stand is walk_right

        # Scale all animations to an appropriate size
        scale_factor = 2.5  # Adjust as needed 3 Last Time
        for direction in self.animations:
            for animation_type in self.animations[direction]:
                img = self.animations[direction][animation_type]
                scaled_width = int(img.get_width() * scale_factor)
                scaled_height = int(img.get_height() * scale_factor)
                self.animations[direction][animation_type] = pygame.transform.scale(
                    img, (scaled_width, scaled_height)
                )

    def update_animation(self):
        """Update character animation frame based on movement and direction."""
        current_time = pygame.time.get_ticks()
        animation_speed = self.animation_cooldown

        # All animations now use the same speed for both boy and girl
        if current_time - self.last_animation_update >= animation_speed:
            self.last_animation_update = current_time
            if self.is_walking:
                self.animation_frame = (self.animation_frame + 1) % 4  # Same 4-step cycle for both characters
            else:
                # When not walking, always reset to standing frame
                self.animation_frame = 0

    def get_current_frame(self):
        """Get the current animation frame based on character type and direction."""
        # If not walking, always return standing position for both boy and girl
        if not self.is_walking:
            return self.animations[self.direction]["stand"]

        if self.hero_type == "boy":
            # Boy animation cycle: walk_left, stand, walk_right, stand
            frame_cycle = ["walk_left", "stand", "walk_right", "stand"]
            key = frame_cycle[self.animation_frame % 4]
            return self.animations[self.direction].get(key, self.animations[self.direction]["stand"])
        else:
            # Girl animation cycle with very short stand time for sideways movement
            if self.direction in ["left", "right"]:
                # For sideways, we want walk frames to be most frequent
                # Using custom cycle that minimizes stand time
                frame_cycle = ["walk_left", "walk_left", "stand", "walk_right"]
                key = frame_cycle[self.animation_frame % 4]

                if key == "walk_left":
                    return self.animations[self.direction]["walk_left"]
                elif key == "walk_right":
                    return self.animations[self.direction]["stand"]  # For girl, stand is used as walk_right
                else:
                    return self.animations[self.direction]["stand"]
            else:
                # For front/back directions, use normal cycle
                frame_cycle = ["walk_left", "stand", "walk_right", "stand"]
                key = frame_cycle[self.animation_frame % 4]
                return self.animations[self.direction].get(key, self.animations[self.direction]["stand"])

    def handle_movement(self, map_bounds, map_pos, screen_size):
        # Unpack parameters
        map_x, map_y = map_pos
        screen_width, screen_height = screen_size

        # Get keyboard state
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        was_walking = self.is_walking
        self.is_walking = False

        # Check arrow keys
        if keys[pygame.K_LEFT]:
            dx = -self.character_speed
            self.direction = "left"
            self.is_walking = True
        elif keys[pygame.K_RIGHT]:
            dx = self.character_speed
            self.direction = "right"
            self.is_walking = True

        if keys[pygame.K_UP]:
            dy = -self.character_speed
            self.direction = "back"
            self.is_walking = True
        elif keys[pygame.K_DOWN]:
            dy = self.character_speed
            self.direction = "front"
            self.is_walking = True

        # Only process if movement keys are pressed
        if dx != 0 or dy != 0:
            # Character's position on the map (absolute coordinates)
            char_map_x = self.character_x - map_x
            char_map_y = self.character_y - map_y

            # Calculate new character position on the map
            new_char_map_x = char_map_x + dx
            new_char_map_y = char_map_y + dy

            # Define map margins - how close character can get to map edge
            margin = 20

            # Check if new position is within map boundaries
            valid_x = margin <= new_char_map_x <= map_bounds['width'] - margin
            valid_y = margin <= new_char_map_y <= map_bounds['height'] - margin

            # Get character dimensions
            current_frame = self.get_current_frame()
            char_width = current_frame.get_width()
            char_height = current_frame.get_height()

            if valid_x and valid_y:  # Both movements are valid
                # Determine if we need to move the character or the map

                # For X-axis movement
                if self.character_x == screen_width // 2:
                    # Character is centered horizontally - try to move map first
                    new_map_x = map_x - dx

                    if map_bounds['min_x'] <= new_map_x <= map_bounds['max_x']:
                        # Map can move within boundaries
                        map_x = new_map_x
                    else:
                        # Map would go out of bounds, move character instead
                        self.character_x += dx
                else:
                    # Character is not centered - try to recenter it
                    new_character_x = self.character_x + dx

                    # If character is moving toward center
                    moving_toward_center = (self.character_x < screen_width // 2 and dx > 0) or \
                                           (self.character_x > screen_width // 2 and dx < 0)

                    if moving_toward_center:
                        # Move character toward center
                        self.character_x = new_character_x

                        # If character crossed center, reset to center and adjust map
                        if (dx > 0 and self.character_x > screen_width // 2) or \
                                (dx < 0 and self.character_x < screen_width // 2):
                            # Calculate how much we overshot
                            overshoot = abs(self.character_x - screen_width // 2)

                            # Reset character to center
                            self.character_x = screen_width // 2

                            # Adjust map by overshoot (in correct direction)
                            map_x -= (dx > 0) and -overshoot or overshoot

                            # Ensure map stays within boundaries
                            map_x = max(min(map_x, map_bounds['max_x']), map_bounds['min_x'])
                    else:
                        # Moving away from center but still at edge, just move character
                        self.character_x = new_character_x

                # For Y-axis movement (similar logic)
                if self.character_y == screen_height // 2:
                    # Character is centered vertically - try to move map first
                    new_map_y = map_y - dy

                    if map_bounds['min_y'] <= new_map_y <= map_bounds['max_y']:
                        # Map can move within boundaries
                        map_y = new_map_y
                    else:
                        # Map would go out of bounds, move character instead
                        self.character_y += dy
                else:
                    # Character is not centered - try to recenter it
                    new_character_y = self.character_y + dy

                    # If character is moving toward center
                    moving_toward_center = (self.character_y < screen_height // 2 and dy > 0) or \
                                           (self.character_y > screen_height // 2 and dy < 0)

                    if moving_toward_center:
                        # Move character toward center
                        self.character_y = new_character_y

                        # If character crossed center, reset to center and adjust map
                        if (dy > 0 and self.character_y > screen_height // 2) or \
                                (dy < 0 and self.character_y < screen_height // 2):
                            # Calculate how much we overshot
                            overshoot = abs(self.character_y - screen_height // 2)

                            # Reset character to center
                            self.character_y = screen_height // 2

                            # Adjust map by overshoot (in correct direction)
                            map_y -= (dy > 0) and -overshoot or overshoot

                            # Ensure map stays within boundaries
                            map_y = max(min(map_y, map_bounds['max_y']), map_bounds['min_y'])
                    else:
                        # Moving away from center but still at edge, just move character
                        self.character_y = new_character_y

            elif valid_x:  # Only X movement is valid
                # Apply only X movement
                if self.character_x == screen_width // 2:
                    new_map_x = map_x - dx
                    if map_bounds['min_x'] <= new_map_x <= map_bounds['max_x']:
                        map_x = new_map_x
                    else:
                        self.character_x += dx
                else:
                    new_character_x = self.character_x + dx
                    moving_toward_center = (self.character_x < screen_width // 2 and dx > 0) or \
                                           (self.character_x > screen_width // 2 and dx < 0)

                    if moving_toward_center:
                        self.character_x = new_character_x
                        if (dx > 0 and self.character_x > screen_width // 2) or \
                                (dx < 0 and self.character_x < screen_width // 2):
                            overshoot = abs(self.character_x - screen_width // 2)
                            self.character_x = screen_width // 2
                            map_x -= (dx > 0) and -overshoot or overshoot
                            map_x = max(min(map_x, map_bounds['max_x']), map_bounds['min_x'])
                    else:
                        self.character_x = new_character_x

            elif valid_y:  # Only Y movement is valid
                # Apply only Y movement
                if self.character_y == screen_height // 2:
                    new_map_y = map_y - dy
                    if map_bounds['min_y'] <= new_map_y <= map_bounds['max_y']:
                        map_y = new_map_y
                    else:
                        self.character_y += dy
                else:
                    new_character_y = self.character_y + dy
                    moving_toward_center = (self.character_y < screen_height // 2 and dy > 0) or \
                                           (self.character_y > screen_height // 2 and dy < 0)

                    if moving_toward_center:
                        self.character_y = new_character_y
                        if (dy > 0 and self.character_y > screen_height // 2) or \
                                (dy < 0 and self.character_y < screen_height // 2):
                            overshoot = abs(self.character_y - screen_height // 2)
                            self.character_y = screen_height // 2
                            map_y -= (dy > 0) and -overshoot or overshoot
                            map_y = max(min(map_y, map_bounds['max_y']), map_bounds['min_y'])
                    else:
                        self.character_y = new_character_y

            # Ensure character stays within screen boundaries
            self.character_x = max(char_width // 2, min(self.character_x, screen_width - char_width // 2))
            self.character_y = max(char_height // 2, min(self.character_y, screen_height - char_height // 2))

        # Update animation state if movement state changed
        if was_walking != self.is_walking:
            self.animation_frame = 0
            self.last_animation_update = pygame.time.get_ticks()
        else:
            # Update animation frames
            self.update_animation()

        return (map_x, map_y), (self.character_x, self.character_y)

    def draw(self, screen):
        # Get current character frame
        character_image = self.get_current_frame()

        # Calculate character position (centered at character_x, character_y)
        char_x = self.character_x - character_image.get_width() // 2
        char_y = self.character_y - character_image.get_height() // 2

        # Draw character
        screen.blit(character_image, (char_x, char_y))
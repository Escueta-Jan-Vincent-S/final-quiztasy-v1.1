import pygame
import math

class CollisionLine:
    def __init__(self, start_pos, end_pos, line_width=3):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.line_width = line_width

        # Calculate line properties for collision detection
        self.dx = end_pos[0] - start_pos[0]
        self.dy = end_pos[1] - start_pos[1]
        self.length = math.sqrt(self.dx ** 2 + self.dy ** 2)

        # Normalize direction vector
        if self.length > 0:
            self.nx = self.dx / self.length
            self.ny = self.dy / self.length
        else:
            self.nx, self.ny = 0, 0

    def point_to_line_distance(self, point):
        px = point[0] - self.start_pos[0]
        py = point[1] - self.start_pos[1]

        # Calculate dot product
        dot = px * self.nx + py * self.ny

        # Clamp dot product to line segment
        dot = max(0, min(self.length, dot))

        # Find closest point on line
        closest_x = self.start_pos[0] + self.nx * dot
        closest_y = self.start_pos[1] + self.ny * dot

        # Calculate distance
        dx = point[0] - closest_x
        dy = point[1] - closest_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def check_collision(self, character_pos, character_radius):
        distance = self.point_to_line_distance(character_pos)
        return distance < (character_radius + self.line_width / 2)

    def draw(self, screen, map_x, map_y, debug_mode=True, color=(255, 0, 0)):
        if debug_mode:
            adjusted_start = (self.start_pos[0] + map_x, self.start_pos[1] + map_y)
            adjusted_end = (self.end_pos[0] + map_x, self.end_pos[1] + map_y)
            pygame.draw.line(screen, color, adjusted_start, adjusted_end, self.line_width)


class MapCollisionHandler:
    def __init__(self):
        self.collision_lines = []
        self.debug_mode = False  # Set to False to hide collision lines
        self.character_collision_radius = 20

    def add_line(self, start_pos, end_pos, line_width=3):
        self.collision_lines.append(CollisionLine(start_pos, end_pos, line_width))

    def add_rectangle(self, top_left, width, height, line_width=3):
        x, y = top_left
        # Create four lines representing rectangle sides
        self.add_line((x, y), (x + width, y), line_width)  # Top
        self.add_line((x + width, y), (x + width, y + height), line_width)  # Right
        self.add_line((x, y + height), (x + width, y + height), line_width)  # Bottom
        self.add_line((x, y), (x, y + height), line_width)  # Left

    def add_polygon(self, points, line_width=3):
        if len(points) < 3:
            return

        for i in range(len(points)):
            start = points[i]
            end = points[(i + 1) % len(points)]
            self.add_line(start, end, line_width)

    def check_collision(self, character_pos):
        for line in self.collision_lines:
            if line.check_collision(character_pos, self.character_collision_radius):
                return True
        return False

    def draw_lines(self, screen, map_x, map_y):
        if self.debug_mode:
            for line in self.collision_lines:
                line.draw(screen, map_x, map_y, self.debug_mode)

    def set_debug_mode(self, enabled):
        self.debug_mode = enabled

    def set_character_collision_radius(self, radius):
        self.character_collision_radius = radius
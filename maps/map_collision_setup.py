class MapCollisionSetup:
    @staticmethod
    def setup_collision_barriers(collision_handler):
        collision_handler.set_character_collision_radius(50)

        # Paths/roads boundaries
        # Highway
        collision_handler.add_line((1760, 300), (1760, 7500))  # V-Left Highway
        collision_handler.add_line((2210, 300), (2210, 1020))  # V-Cutted Upper Right Highway
        collision_handler.add_line((2210, 1940), (2210, 7500))  # V-Cutted Lower Right Highway
        collision_handler.add_line((1760, 300), (2210, 300))  # H-Close Upper Highway
        collision_handler.add_line((1760, 7500), (2210, 7500))  # H-Close Lower Highway

        # Entrance
        collision_handler.add_rectangle((2345, 1586.3), 750, 10)  # Garden Part Rectangle
        collision_handler.add_line((2210, 1020), (2430, 1020))  # Car to Garden to Gate
        collision_handler.add_line((2430, 1020), (2430, 1200))  # Car to Garden to Gate
        collision_handler.add_line((2430, 1200), (2345, 1200))  # Car to Garden to Gate
        collision_handler.add_line((2345, 1200), (2345, 1360))  # Car to Garden to Gate
        collision_handler.add_line((2345, 1360), (3250, 1360))  # Car to Garden to Gate
        collision_handler.add_line((2210, 1940), (3250, 1940))  # Lowerpart of Gate
        collision_handler.add_line((3120, 1545), (3120, 1735))  # Middle gate
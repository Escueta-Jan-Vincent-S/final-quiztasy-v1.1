class MapCollisionSetup:
    @staticmethod
    def setup_collision_barriers(collision_handler):
        collision_handler.set_character_collision_radius(50)
        # Highway Area
        collision_handler.add_line((1760, 300), (1760, 7500))  # V-Left Highway
        collision_handler.add_line((2210, 300), (2210, 1020))  # V-Cutted Upper Right Highway
        collision_handler.add_line((2210, 2020), (2210, 7500))  # V-Cutted Lower Right Highway
        collision_handler.add_line((1760, 300), (2210, 300))  # H-Close Upper Highway
        collision_handler.add_line((1760, 7500), (2210, 7500))  # H-Close Lower Highway

        # Entrance Area
        collision_handler.add_rectangle((2345, 1586.3), 750, 10)  # Garden Part Rectangle
        collision_handler.add_line((2210, 1020), (2430, 1020)) # Car to Garden to Gate
        collision_handler.add_line((2430, 1020), (2430, 1200)) # Car to Garden to Gate
        collision_handler.add_line((2430, 1200), (2345, 1200)) # Car to Garden to Gate
        collision_handler.add_line((2345, 1200), (2345, 1360)) # Car to Garden to Gate
        collision_handler.add_line((2345, 1360), (3250, 1360)) # Car to Garden to Gate

        collision_handler.add_line((3120, 1545), (3120, 1735)) # Left Side Middle gate
        collision_handler.add_line((3250, 1545), (3250, 1735)) # Right Side Middle gate
        collision_handler.add_line((3120, 1545), (3250, 1545)) # Upper Close Middle Gate
        collision_handler.add_line((3120, 1735), (3250, 1735)) # Lower Close Middle Gate

        collision_handler.add_line((2210, 2020), (2360, 2020)) # Connection of Lower Right Highway to lower part of gate
        collision_handler.add_line((2360, 1940), (3250, 1940)) # Lowerpart of Gate
        collision_handler.add_line((3250, 1990), (4430, 1990)) # Lowerpart of Gate Small Tree
        collision_handler.add_line((3550, 1940), (3600, 1940)) # Lowerpart of Gate Big Tree 1
        collision_handler.add_line((3925, 1940), (3975, 1940))  # Lowerpart of Gate Big Tree 2

        # Garden Area Right side of Entrance
        collision_handler.add_line((3250, 1630), (4325, 1630)) # Garden Upper Side
        collision_handler.add_line((3250, 1650), (4325, 1650)) # Garden Lower Side

        # Research Building Area
        collision_handler.add_line((4430, 1990), (4430, 3060))  # Research Building Area Left Side
        collision_handler.add_line((4430, 3060), (4650, 3060)) # Bike Area Top Side
        collision_handler.add_line((4650, 3060), (4650, 3660))  # Bike Area Right Side
        collision_handler.add_line((4650, 3660), (5110, 3660))  # Research Building Area Lower Side
        collision_handler.add_line((5110, 3660), (5110, 2010))  # Research Building Area Right Side
        collision_handler.add_line((5110, 2010), (5900, 2010))  # Research Building Area Upper Side

        # Church Area
        collision_handler.add_line((3250, 1360), (3250, 400)) # Church Left Side
        collision_handler.add_line((3250, 400), (3600, 400))  # Church Upper Side
        collision_handler.add_line((3600, 400), (3600, 1280))  # Church Right Side / Left Side of Administration Building

        # Administration Building Area
        collision_handler.add_line((3600, 1280), (4700, 1280)) # Administration Building Lower Side
        collision_handler.add_line((4700, 1280), (4700, 1160))  # Administration Building Lower Side 2
        collision_handler.add_line((4700, 1160), (4810, 1160))  # Administration Building Lower Side 3
        collision_handler.add_line((4810, 1160), (4810, 900))  # Administration Building Right Side

        collision_handler.add_line((4810, 900), (5120, 900)) # Barrier Between Administration Building and Canteen
        collision_handler.add_line((5120, 900), (5120, 970)) # Canteen Left Side
        collision_handler.add_line((5120, 970), (5215, 970))  # Canteen Left Side 2
        collision_handler.add_line((5215, 970), (5215, 1080))  # Canteen Left Side 3
        collision_handler.add_line((5215, 1080), (5350, 1080))  # Canteen Lower Side
        collision_handler.add_line((5350, 1080), (5350, 1120))  # Canteen Lower Side 2
        collision_handler.add_line((5350, 1120), (5530, 1120))  # Canteen Lower Side 3
        collision_handler.add_line((5530, 1080), (5530, 1120))  # Canteen Lower Side 4
        collision_handler.add_line((5530, 1080), (5665, 1080))  # Canteen Lower Side 5
        collision_handler.add_line((5665, 1080), (5665, 970))  # Canteen Right Side
        collision_handler.add_line((5665, 970), (5975, 970))  # Canteen Right Side 2

        collision_handler.add_line((5975, 970), (5975, 1330))  # Yellow Thing Area Connected to Canteen
        collision_handler.add_line((5975, 1330), (5700, 1330))  # Upper Part of Garden Area Right Side of Fountain
        collision_handler.add_line((5700, 1330), (5700, 1455))  # Fountain Area Right Side
        collision_handler.add_line((5700, 1455), (6160, 1455))  # Lower Part of Garden Area Right Side of Fountain



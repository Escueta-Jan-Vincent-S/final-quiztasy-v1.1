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

        # LOWER PART
        # Garden Area Right side of Entrance
        collision_handler.add_line((3250, 1630), (4325, 1630)) # Garden Upper Side
        collision_handler.add_line((3250, 1650), (4325, 1650)) # Garden Lower Side

        # Research Building Area
        collision_handler.add_line((4430, 1990), (4430, 3060))  # Research Building Area Left Side
        collision_handler.add_line((4430, 3060), (4650, 3060)) # Bike Area Top Side
        collision_handler.add_line((4650, 3060), (4650, 3660))  # Bike Area Right Side
        collision_handler.add_line((4650, 3660), (5110, 3660))  # Research Building Area Lower Side
        collision_handler.add_line((5110, 3660), (5110, 2010))  # Research Building Area Right Side
        collision_handler.add_line((5110, 2010), (6300, 2010))  # Research Building Area Upper Side
        collision_handler.add_line((6200, 1850), (6300, 1850)) # Light
        collision_handler.add_line((6200, 1850), (6200, 2010))  # Light Left
        collision_handler.add_line((6300, 1850), (6300, 2010))  # Light Right
        collision_handler.add_line((6025, 1950), (6300, 1950)) # Tree

        # Waiting Shed Area
        collision_handler.add_line((6300, 2010), (6300, 2200)) # Waiting Shed Left Side with Lights
        collision_handler.add_line((6250, 2200), (6250, 3480)) # Waiting Shed Left Side
        collision_handler.add_line((6550, 1990), (6550, 3800)) # Waiting Shed Mid Left Side
        collision_handler.add_line((6730, 1990), (6730, 3770))  # Waiting Shed Mid Right Side
        collision_handler.add_line((6550, 1990), (6730, 1990)) # Waiting Shed Upper Side with Lights
        collision_handler.add_line((6200, 3480), (6250, 3480))

        # Baba ng Waiting Shed Mid Right Side
        collision_handler.add_line((6730, 3770), (7300, 3770)) # Below Lvl 14
        collision_handler.add_line((7300, 3770), (7300, 4130)) # Right Y
        collision_handler.add_line((7300, 4130), (7410, 4130)) # Right X
        collision_handler.add_line((7410, 4130), (7410, 4840))  # Right Y - Right Side of Level 13
        collision_handler.add_line((7410, 4840), (7790, 4840)) # Right X - Below Side of Level 13
        collision_handler.add_line((7790, 4840), (7790, 3790))  # Right Y - Right Side of Level 13
        collision_handler.add_line((7790, 3790), (7600, 3790))  # Right X - Baba ng Shed
        collision_handler.add_line((7600, 3790), (7600, 3400))  # Right Y - Left Side ng Shed
        collision_handler.add_line((7600, 3400), (7030, 3400))  # Right X
        collision_handler.add_line((7030, 3400), (7030, 1850))  # Waiting Shed Right Side
        collision_handler.add_line((7000, 1850), (7050, 1850)) # Light Barrier
        collision_handler.add_line((7000, 1930), (7050, 1930))  # Light Barrier 2
        collision_handler.add_line((7050, 2010), (7810, 2010)) # X Below Level 15
        collision_handler.add_line((7810, 2030), (8200, 2030))  # X Below Level 16
        collision_handler.add_line((8200, 2100), (9500, 2100)) # X Below Level 18
        collision_handler.add_line((8710, 2040), (8790, 2040))  # Tree Barrier

        # GYM RIGHT SIDE
        collision_handler.add_line((9500, 2100), (9500, 4840)) # Gym Right Side
        collision_handler.add_line((9500, 4840), (10000, 4840))  # Below Level 11
        collision_handler.add_line((10000, 4840), (10000, 2000))  # Right Side of Level 11

        # CHMT ata to
        collision_handler.add_line((6150, 3480), (6150, 7280)) # CHMT Hanggang Dulo sa Baba sa Left
        collision_handler.add_line((6550, 3800), (6500, 3800))  # Waiting Shed Mid Left Side sa CHMT
        collision_handler.add_line((6500, 3800), (6500, 3900))  # Waiting Shed Mid Left Side sa CHMT 2
        collision_handler.add_line((6500, 3900), (6470, 3900))  # Waiting Shed Mid Left Side sa CHMT 3
        collision_handler.add_line((6470, 3900), (6470, 4150))  # Waiting Shed Mid Left Side sa CHMT 4
        collision_handler.add_line((6470, 4150), (6550, 4150))  # Waiting Shed Mid Left Side sa CHMT 5
        collision_handler.add_line((6570, 4150), (6570, 5300))  # Harap ng CHMT, Left side ng CAS
        collision_handler.add_line((6570, 5300), (8100, 5300))  # Baba ng CAS

        # POOL AREA
        collision_handler.add_line((8100, 5300), (8100, 5700)) # Left side ng shed
        collision_handler.add_line((8100, 5700), (9310, 5700)) # Baba ng shed
        collision_handler.add_line((9310, 5700), (9310, 5400))  # Right Side ng shed
        collision_handler.add_line((9310, 5400), (9620, 5400))  # Right Side ng shed 2
        collision_handler.add_line((9620, 5400), (9620, 6650))  # Right Side ng pool
        collision_handler.add_line((8190, 6650), (9620, 6650))  # Lower Side ng pool
        collision_handler.add_line((8190, 6650), (8190, 7280))  # Left side ng extension
        collision_handler.add_line((6150, 7280), (8190, 7280))  # Lower Barrier Mula Extension gang don

        # POOL
        collision_handler.add_line((8230, 5965), (8230, 6330)) # Left Side ng pool
        collision_handler.add_line((9200, 5965), (9200, 6330))  # Right Side ng pool
        collision_handler.add_line((8230, 5965), (9200, 5965))  # Upper Side ng pool
        collision_handler.add_line((8230, 6330), (9200, 6330))  # Lower Side ng pool

        # YUNG ANO THEATHER BAYUN
        collision_handler.add_line((6570, 5810), (6570, 6920)) # Left Side ng Theater
        collision_handler.add_line((7415, 5810), (7415, 5910)) # Right Side ng Theater
        collision_handler.add_line((7415, 5910), (7780, 5910))  # Right Side ng Theater 2
        collision_handler.add_line((7780, 5910), (7780, 6370))  # Right Side ng Theater 3
        collision_handler.add_line((7670, 6370), (7770, 6370))  # Right Side ng Theater 4
        collision_handler.add_line((7670, 6370), (7680, 6760))  # Right Side ng Theater 5 Right Side ng kotse
        collision_handler.add_line((7415, 6760), (7680, 6760))  # Right Side ng Theater 5
        collision_handler.add_line((7415, 6760), (7415, 6920))  # Right Side ng Theater 6
        collision_handler.add_line((6570, 5810), (7415, 5810))  # Upper Side ng Theater
        collision_handler.add_line((6570, 6920), (7415, 6920))  # Lower Side ng Theater

        # UPPER PART
        # Church Area
        collision_handler.add_line((3250, 1360), (3250, 400))  # Church Left Side
        collision_handler.add_line((3250, 400), (3600, 400))  # Church Upper Side
        collision_handler.add_line((3600, 400), (3600, 1280))  # Church Right Side / Left Side of Administration Building

        # Administration Building Area
        collision_handler.add_line((3600, 1280), (4700, 1280))  # Administration Buildiwdng Lower Side
        collision_handler.add_line((4700, 1280), (4700, 1160))  # Administration Building Lower Side 2
        collision_handler.add_line((4700, 1160), (4810, 1160))  # Administration Building Lower Side 3
        collision_handler.add_line((4810, 1160), (4810, 900))  # Administration Building Right Side
        collision_handler.add_line((4810, 900), (5120, 900)) # Barrier Between Administration Building and Canteen

        # Canteen Area
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
        collision_handler.add_line((5350, 1500), (5540, 1500))  # Lower Fontaine Barrier
        collision_handler.add_line((5340, 1400), (5550, 1400))  # Upper Fontaine Barrier
        collision_handler.add_line((5390, 1340), (5500, 1340))  # Upper Fontaine Barrier

        # CCS ata to
        collision_handler.add_line((6160, 1455), (6160, 1150)) # Left Side of Lvl 6
        collision_handler.add_line((6160, 1150), (6680, 1150))  # Upper Side of Lvl 6
        collision_handler.add_line((6680, 1150), (6680, 1455))  # Right Side of Lvl 6
        collision_handler.add_line((6680, 1455), (7030, 1455))  # Plawer

        # Below Tennis Area
        collision_handler.add_line((7030, 1455), (7030, 970))  # Left Side
        collision_handler.add_line((7030, 970), (7500, 970))  # Upper Side
        collision_handler.add_line((7500, 970), (7500, 1455))  # Right Side
        collision_handler.add_line((7500, 1455), (7900, 1455)) # Bulaklakin

        # Saan To?
        collision_handler.add_line((7900, 1455), (7900, 1540)) # Green Dahon
        collision_handler.add_line((7900, 1540), (7990, 1540))  # Green Dahon Ulet Sa baba
        collision_handler.add_line((7990, 1540), (7990, 1380))  # Green Dahon Ulet Sa Kanan
        collision_handler.add_line((7990, 1380), (8360, 1380))  # Building
        collision_handler.add_line((8360, 1380), (8360, 800))  # Left Side ng Level 17
        collision_handler.add_line((8365, 800), (8665, 800))  # Upper Side ng Level 17
        collision_handler.add_line((8665, 800), (8665, 1380))  # Right Side ng Level 17
        collision_handler.add_line((8665, 1380), (9500, 1380))  # Dalawang Building

        # Engineering Tapat
        collision_handler.add_line((9500, 1380), (9500, 450)) # Left Side ng Engineering
        collision_handler.add_line((9500, 450), (10020, 450))  # Upper Side ng Engineering
        collision_handler.add_line((10020, 450), (10020, 830)) # Right Side ng Engineering
        collision_handler.add_line((9930, 830), (10020, 830))  # CHMT Ata
        collision_handler.add_line((9930, 830), (9930, 1150))  # CHMT Ata Ulet
        collision_handler.add_line((10000, 1150), (10000, 2000)) # Right Side ng Level 19

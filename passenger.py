# =========================================================
# P A S S E N G E R   S Y S T E M
# =========================================================
from imports import *
from assets import passenger_imgs
from settings import all_destinations, passenger_types

# tinitignan niya kung rush hour men
is_rush_hour = False

# ======================================================
# P A S S E N G E R   C L A S S
# ======================================================
class Passenger:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.image = random.choice(passenger_imgs)
        self.is_riding = False
        self.approaching = False
        self.is_leaving = False
        self.has_requested = False 
        self.alpha = 255
        self.speed = 1.0
        self.message = ""
        
        # Bawat pasahero may sariling babaan pagka-spawn pa lang
        self.destination = random.choice(all_destinations) 
        
        # Pag-set kung anong klaseng pasahero at magkano pamasahe nila
        self.p_type = random.choice(passenger_types)
        self.fare = 11 if self.p_type in ["Student", "Senior", "PWD"] else 13
        
    def update(self, jeep_pos, jeep_is_moving, current_passengers):
        global is_rush_hour
        
        self.message = "" 
        
        # 1. KUNG BUMABABA NA AT UMALIS
        if self.is_leaving:
            self.pos.y -= 0.8
            self.alpha -= 5
            if self.alpha <= 0: 
                self.respawn()
            return
            
        # 2. KUNG NAKASAKAY NA SA JEEP
        # 2. KUNG NAKASAKAY NA SA JEEP
        if self.is_riding:
            # Laging chine-check kung nasa loob na ng 60 pixels radius (drop-off zone)
            dist_to_dest = self.destination.distance_to(jeep_pos)
            
            if dist_to_dest < 60: 
                self.has_requested = True  # Kakatok at lalabas yung "PARA!"
            else:
                self.has_requested = False # Mawawala yung "PARA!" kapag lumagpas

            return
            
        # 3. KUNG NAG-AABANG PA LANG SA KALSADA
        dist = self.pos.distance_to(jeep_pos)
        
        # Kapag malapit ang jeep (70 pixels)
        if dist < 70 and not self.is_riding and not self.is_leaving:
            if current_passengers >= 18: # Check kung puno
                self.message = "Ay, puno na!"
                self.approaching = False
            else:
                self.message = "Para po!"
                if not jeep_is_moving:
                    self.approaching = True
                    
        # 4. KUNG NAGLALAKAD PAPUNTA SA JEEP (SASAKAY)
        if self.approaching:
            if dist > 5:
                direction = (jeep_pos - self.pos).normalize()
                # Rush hour speed boost logic
                curr_speed = self.speed * 1.5 if is_rush_hour else self.speed
                self.pos += direction * curr_speed
            else:
                self.is_riding = True
                self.approaching = False
                self.message = ""

    def respawn(self):
        self.is_leaving = False
        self.is_riding = False
        self.has_requested = False
        self.alpha = 255
        self.pos = pygame.Vector2(random.randint(100, 750), random.randint(100, 550))
        
        # Bigyan uli ng bagong destination, type, at pamasahe pagka-respawn
        self.destination = random.choice(all_destinations) 
        self.p_type = random.choice(passenger_types)
        self.fare = 11 if self.p_type in ["Student", "Senior", "PWD"] else 13
        
# ======================================================
# I N I T I A L   S P A W N I N G
# ======================================================
passengers_on_map = [Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
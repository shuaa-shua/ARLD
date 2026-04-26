# =========================================================
# P A S S E N G E R   S Y S T E M
# =========================================================
from imports import *
from assets import passenger_imgs

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

    def update(self, jeep_pos, jeep_is_moving, current_passengers):
        global is_rush_hour
        
        self.message = "" # Reset message kada frame
        
        if self.is_leaving:
            self.pos.y -= 0.8
            self.alpha -= 5
            if self.alpha <= 0: 
                self.respawn()
            return
            
        if self.is_riding:
            # dito inaadjust ung bilis ng pag para ng passenger 3500+ mas matagal
            if not self.has_requested and random.randint(1, 3500) == 1:
                self.has_requested = True
            return
            
        dist = self.pos.distance_to(jeep_pos)
        
        # Kapag malapit ang jeep (150 pixels)
        if dist < 150 and not self.is_riding and not self.is_leaving:
            if current_passengers >= 18: # Check kung puno
                self.message = "Ay, puno na!"
                self.approaching = False
            else:
                self.message = "Para po!"
                if not jeep_is_moving:
                    self.approaching = True
                    
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

# ======================================================
# I N I T I A L   S P A W N I N G
# ======================================================
# 3. Gawa ng 15 na tao sa map
passengers_on_map = [Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
# =========================================================
# S E T T I N G S  &  C O N S T A N T S
# =========================================================
from imports import *

# ======================================================
# S C R E E N  S E T U P
# ======================================================
width = 850
height = 650

# ======================================================
# J E E P  S E T U P  (Constants)
# ======================================================
rotation_speed = 3 # Bilis ng pagliko
jeep_speed_original = 0.9 # bilis ng jeep normal na takbo
reverse_speed = 0.3 # bilis ng pag stras hihihi

# ======================================================
# S U P E R  S A I Y A N  B O O S T  S Y S T E M
# ======================================================
max_boost_power = 100        # 
ss_charge_speed = 1.5        # Bilis ng pagpuno ng bar 
ss_boost_duration = 3000     # Gaano katagal ang bilis 
ss_speed_multiplier = 3.0    # Gaano kabilis kapag nka-boost

# GAS CONSUMPTION VALUES
gas_consume_normal = 0.001   # Bawas gas kapag normal lang (mabagal lang natin)
gas_consume_charging = 0.03  # bawas nung gas habang nagcha-charge (bago mag-boost)
gas_consume_boosting = 0.01  # bawas nung gas kapag naka-boost na

# ======================================================
# H E A L T H  S Y S T E M
# ======================================================
max_health = 100
collision_damage = 10        # Bawas sa health kada bangga
damage_cooldown = 1000       # 1 second bago pwedeng mabawasan ulit

# ======================================================
# G A S  S Y S T E M
# ======================================================
max_gas = 100
gas_consumption = 0.01       # Bilis bawas ng gas

# ======================================================
# T I M E   S Y S T E M  
# ======================================================
time_tick_speed = 2.0        

# ======================================================
# R U S H  H O U R  S Y S T E M 
# ======================================================
rush_notif_duration = 6000 

# ======================================================
# C A M E R A  S E T U P
# ======================================================
zoom_factor = 2.0 #ZOOM IN AND OUT 

# ======================================================
# H I T B O X  S E T U P (Invisible Walls)
# ======================================================
SHOW_HITBOXES = False
#(x left, right, y- up down, width, height)
house_hitboxes = [
    pygame.Rect(160, 320, 150, 190),
    pygame.Rect(160, 110, 70, 300),
    pygame.Rect(15, 30, 60, 200),
    pygame.Rect(298, 25, 55, 200),
    pygame.Rect(320, 25, 140, 65),
    pygame.Rect(570, 12, 300, 60),
    pygame.Rect(563, 170, 100, 150),
    pygame.Rect(795, 170, 20, 160),#
    pygame.Rect(420, 175, 40, 130),
    pygame.Rect(400, 400, 60, 60),
    pygame.Rect(380, 580, 80, 60),
    pygame.Rect(630, 420, 150, 150)
]

# ======================================================
# Q U O T A  &  D A S H B O A R D  L O G I C (DAGDAG)
# ======================================================
daily_quota = 300
gas_price_per_unit = 6.0       #Price ng gas, 6 pesos per 1 percent  
passenger_types = ["Regular", "Student", "Senior", "PWD"]

# ======================================================
# U I   C O N S T A N T S  &  T I M E R S
# ======================================================
coming_soon_duration = 3000   
backspace_delay = 400
backspace_speed = 50
fade_speed = 10                
saved_duration = 1000
# =========================================================
# J E E P   S T A T E   &   V A R I A B L E S
# =========================================================
from imports import *
from settings import *

# ======================================================
# J E E P  S E T U P
# ======================================================
jeep_x = width // 2 
jeep_y = height - 150
jeep_angle = 0
jeep_speed = jeep_speed_original

# Para sa animation at shake
aura_alpha = 0
engine_shake_x = 0 # 
engine_shake_y = 0

# ======================================================
# E N G I N E   S T A T E S
# ======================================================
engine_on = False
is_starting = False
engine_start_timer = 0

# ======================================================
# S U P E R  J E E P  B O O S T  S Y S T E M
# ======================================================
ss_charging = False         # Kung nka-hold ang left click
ss_charge_power = 0         # 0 to 100
ss_is_active = False        # Kung nka-boost na
ss_boost_timer = 0          # Timer para sa duration

# ======================================================
# H E A L T H  S Y S T E M
# ======================================================
current_health = max_health
last_damage_time = 0        # Para hindi maubos agad ang buhay sa isang dikit lang

# ======================================================
# G A S  S Y S T E M
# ======================================================
current_gas = max_gas
current_consume_rate = 0

# ======================================================
# H E A D L I G H T   S Y S T E M
# ======================================================
headlight_on = False

# ======================================================
# P A S S E N G E R   T R A C K I N G
# ======================================================
jeep_passengers_count = 0
last_drop_time = 0

# --- SPECIAL MISSION TRACKER ---
active_mission_dest = None        # Hawak yung Vector2 ng destination
active_mission_passenger = None   # Sino yung pasaway na pasahero
mission_notif_timer = 0
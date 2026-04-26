# =========================================================
# C A M E R A   &   S H A K E   S Y S T E M
# =========================================================
from imports import *
from settings import width, height, zoom_factor

# ======================================================
# C A M E R A   V A R I A B L E S
# ======================================================
cam_x = 0
cam_y = 0

# ======================================================
# C A M E R A   F O L L O W   L O G I C
# ======================================================
def update_camera(jeep_x, jeep_y):
    global cam_x, cam_y
    
    # 1. Center camera sa jeep
    cam_x = jeep_x - (width / 2) / zoom_factor
    cam_y = jeep_y - (height / 2) / zoom_factor
    
    # 2. Camera Limits (Boundaries para hindi lumampas sa mapa)
    if cam_x < 0: 
        cam_x = 0
    if cam_x > width - (width / zoom_factor): 
        cam_x = width - (width / zoom_factor)
        
    if cam_y < 0: 
        cam_y = 0
    if cam_y > height - (height / zoom_factor): 
        cam_y = height - (height / zoom_factor)
        
    return cam_x, cam_y

# ======================================================
# S C R E E N   S H A K E   L O G I C
# ======================================================
def get_shake_offset(last_damage_time):
    """
    Nagbabalik ng offset x at y para umuga ang screen 
    kapag kababangga lang ng jeep.
    """
    s_offset_x = 0
    s_offset_y = 0
    
    # Shake effect kapag bagong bangga (loob ng 150 milliseconds)
    if pygame.time.get_ticks() - last_damage_time < 150:
        s_offset_x = random.randint(-6, 6)
        s_offset_y = random.randint(-6, 6)
        
    return s_offset_x, s_offset_y

def get_glitch_shake_offset():
    """
    Para ito sa Lose Screen glitch effect (malakas na kalog).
    """
    shake_offset_x = random.randint(-10, 10)
    shake_offset_y = random.randint(-10, 10)
    
    return shake_offset_x, shake_offset_y
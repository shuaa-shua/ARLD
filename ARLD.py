#========================================================
#I M P O R T
#========================================================
import pygame
import sys
import time
import random
import cv2
import math

# ======================================================
# I N I T
# ======================================================
pygame.init()
pygame.mixer.init()

# ======================================================
# S C R E E N  S E T U P
# ======================================================
width = 850
height = 650

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("All Roads Lead to Dagupan (ARLD)")
clock = pygame.time.Clock()

# =======================================================
# S O U N D  S E T U P
# =======================================================
# Sa SOUND SETUP section
engine_start_sound = pygame.mixer.Sound("music/car starting.mp3") # Tunog ng pag-redondo
engine_idle_sound = pygame.mixer.Sound("music/car sound.mp3")   # Tuloy-tuloy na ugong
engine_start_sound.set_volume(0.6)
engine_idle_sound.set_volume(0.4)

win_music = pygame.mixer.Sound("music/win music.mp3") 
win_music.set_volume(0.6)
win_music_playing = False # Flag para hindi mag-loop ang pag-play


engine_on = False
is_starting = False
idle_playing = False
engine_start_timer = 0

lose_sound = pygame.mixer.Sound("music/lose sound.wav")
lose_sound.set_volume(1.0)

lose_music_playing = False

accident_sound = pygame.mixer.Sound("music/Accident sound.mp3")
accident_sound.set_volume(0.6)

powerup_sound = pygame.mixer.Sound("music/powerup.mp3")
powerup_sound.set_volume(1.0)

speedup_sound = pygame.mixer.Sound("music/speedup.mp3")
speedup_sound.set_volume(0.8)
charge_playing = False
boost_sound_playing = False

knocking_sound = pygame.mixer.Sound("music/knocking.mp3")
knocking_sound.set_volume(1.0)
para_sound_played = False

money_sound = pygame.mixer.Sound("music/Money.mp3")
money_sound.set_volume(0.8)

button_sound = pygame.mixer.Sound("music/button sound.wav")
button_sound.set_volume(0.5)

jeep_horn_sound = pygame.mixer.Sound("music/horn.mp3")
jeep_horn_sound.set_volume(5.0)

click_sound = pygame.mixer.Sound("music/click.wav")
click_sound.set_volume(1.0)

jeep_sound1 = pygame.mixer.Sound("music/bagyo.mp3")
jeep_sound1.set_volume(0.3)

jeep_sound2 = pygame.mixer.Sound("music/Binibirocha.mp3")
jeep_sound2.set_volume(0.3)

jeep_sound3 = pygame.mixer.Sound("music/Hawak Mo Ang Beat Remix.mp3")
jeep_sound3.set_volume(0.3)

jeep_sound4 = pygame.mixer.Sound("music/Kahit Maputi Na Ang Buhok ko.mp3")
jeep_sound4.set_volume(0.3)

jeep_sound5 = pygame.mixer.Sound("music/Malunggay Pandesal.mp3")
jeep_sound5.set_volume(0.3)

jeep_sound6 = pygame.mixer.Sound("music/Manok Na Pula.mp3")
jeep_sound6.set_volume(0.3)

jeep_sound7 = pygame.mixer.Sound("music/Modelong Charing.mp3")
jeep_sound7.set_volume(0.3)

jeep_sound8 = pygame.mixer.Sound("music/Totoy Bibbo.mp3")
jeep_sound8.set_volume(0.3)

jeep_sound9 = pygame.mixer.Sound("music/Touch By Touch.mp3")
jeep_sound9.set_volume(0.3)

jeep_sound10 = pygame.mixer.Sound("music/papadudut.mp3")
jeep_sound10.set_volume(0.4)

# =======================================================
# M U S I C   P L A Y E R   L O G I C
# =======================================================
playlist = [
    {"name": "OFF", "sound": None},
    {"name": "Bagyo", "sound": jeep_sound1},
    {"name": "Binibirocha", "sound": jeep_sound2},
    {"name": "Hawak Mo Beat", "sound": jeep_sound3},
    {"name": "Maputi Buhok", "sound": jeep_sound4},
    {"name": "Pandesal", "sound": jeep_sound5},
    {"name": "Manok Pula", "sound": jeep_sound6},
    {"name": "Charing", "sound": jeep_sound7},
    {"name": "Totoy Bibbo", "sound": jeep_sound8},
    {"name": "Touch Touch", "sound": jeep_sound9},
    {"name": "papadudut", "sound": jeep_sound10}
]
current_music_index = 0

def start_jeep_radio(index):
    # 1. Patayin muna ang Main Menu music
    pygame.mixer.music.stop()
    
    # 2. I-stop muna lahat ng kasalukuyang kanta sa playlist
    for item in playlist:
        # SAFETY CHECK: I-check kung may laman yung sound (hindi None)
        if item["sound"] is not None:
            item["sound"].stop()
            
    # 3. Kunin ang napiling kanta base sa index
    selected_item = playlist[index]
    
    # 4. I-check kung ang napili ay may sound o "OFF"
    if selected_item["sound"] is not None:
        # Kung may sound (ON), patugtugin ito
        selected_item["sound"].play(-1)
    else:
        # Kung None (OFF), mananatiling tahimik ang paligid
        print("Radio turned OFF")

pygame.mixer.music.load("music/main bg music beep.mp3")
pygame.mixer.music.set_volume(0.4)

# ======================================================
# V I D E O  B A C K G R O U N D S
# ======================================================
video = cv2.VideoCapture("backgrounds/moving bg.mp4")
blurdbg_vid = cv2.VideoCapture("backgrounds/blurd vid bg.mp4")



# ======================================================
# B U T T O N  I M A G E S
# ======================================================
button_start = pygame.image.load("buttons/START.png").convert_alpha()
button_start = pygame.transform.scale(button_start, (233, 65))

button_about = pygame.image.load("buttons/ABOUT.png").convert_alpha()
button_about = pygame.transform.scale(button_about, (233, 65))

button_exit = pygame.image.load("buttons/EXIT.png").convert_alpha()
button_exit = pygame.transform.scale(button_exit, (234, 65))

button_confirm = pygame.image.load("buttons/CONFIRM.png").convert_alpha()
button_confirm = pygame.transform.scale(button_confirm, (172, 65))

button_cancel = pygame.image.load("buttons/CANCEL.png").convert_alpha()
button_cancel = pygame.transform.scale(button_cancel, (174, 65))

button_cancel_green = pygame.image.load("buttons/CANCEL GREEN.png").convert_alpha()
button_cancel_green = pygame.transform.scale(button_cancel_green, (174, 65))

button_confirm_exit = pygame.image.load("buttons/EXIT.png").convert_alpha()
button_confirm_exit = pygame.transform.scale(button_confirm_exit, (172, 65))

button_caldag = pygame.image.load("buttons/CAL DAG.png").convert_alpha()
button_caldag = pygame.transform.scale(button_caldag, (387, 62))

button_sandag = pygame.image.load("buttons/SAN DAG.png").convert_alpha()
button_sandag = pygame.transform.scale(button_sandag, (387, 62))

button_lindag = pygame.image.load("buttons/LIN DAG.png").convert_alpha()
button_lindag = pygame.transform.scale(button_lindag, (387, 62))

button_back_menu = pygame.image.load("buttons/BACK MENU.png").convert_alpha()
button_back_menu = pygame.transform.scale(button_back_menu, (387, 62))

# ======================================================
# H O V E R  B U T T O N  I M A G E S
# ======================================================
button_start_hover = pygame.image.load("buttons/HOVER START.png").convert_alpha()
button_start_hover = pygame.transform.scale(button_start_hover, (230, 65))

button_about_hover = pygame.image.load("buttons/HOVER ABOUT.png").convert_alpha()
button_about_hover = pygame.transform.scale(button_about_hover, (233, 65))

button_exit_hover = pygame.image.load("buttons/HOVER EXIT.png").convert_alpha()
button_exit_hover = pygame.transform.scale(button_exit_hover, (233, 65))

button_confirm_hover = pygame.image.load("buttons/HOVER CONFIRM.png").convert_alpha()
button_confirm_hover = pygame.transform.scale(button_confirm_hover, (172, 65))

button_cancel_hover = pygame.image.load("buttons/HOVER CANCEL.png").convert_alpha()
button_cancel_hover = pygame.transform.scale(button_cancel_hover, (165, 64))

button_cancel_green_hover = pygame.image.load("buttons/HOVER CANCEL GREEN.png").convert_alpha()
button_cancel_green_hover = pygame.transform.scale(button_cancel_green_hover, (165, 64))

button_confirm_exit_hover = pygame.image.load("buttons/HOVER EXIT.png").convert_alpha()
button_confirm_exit_hover = pygame.transform.scale(button_confirm_exit_hover, (176, 67))

button_caldag_hover = pygame.image.load("buttons/HOVER CAL DAG.png").convert_alpha()
button_caldag_hover = pygame.transform.scale(button_caldag_hover, (387, 61))

button_sandag_hover = pygame.image.load("buttons/HOVER SAN DAG.png").convert_alpha()
button_sandag_hover = pygame.transform.scale(button_sandag_hover, (387, 62))

button_lindag_hover = pygame.image.load("buttons/HOVER LIN DAG.png").convert_alpha()
button_lindag_hover = pygame.transform.scale(button_lindag_hover, (387, 62))

button_backmenu_hover = pygame.image.load("buttons/HOVER BACK MENU.png").convert_alpha()
button_backmenu_hover = pygame.transform.scale(button_backmenu_hover, (387, 62))

# =======================================================
# S O U N D  S E T U P
# =======================================================
# ... (existing sounds mo)

reverse_sound = pygame.mixer.Sound("music/reverse.mp3") # Siguraduhin na may file ka na ganito
reverse_sound.set_volume(0.3) # Hinaan lang natin para hindi masakit sa tenga
reverse_playing = False # Flag para hindi mag-overlap ang tunog


# ======================================================
# G A M E  B A C K G R O U N D S 
# ======================================================

route_caldag_img = pygame.image.load("route/caldag.png").convert()
route_caldag_img = pygame.transform.scale(route_caldag_img, (width, height))

# ======================================================
# J E E P  S E T U P
# ======================================================
jeep_img_original = pygame.image.load("Jeep/caldag_jeep.png").convert_alpha() 
jeep_img_original = pygame.transform.scale(jeep_img_original, (40, 71)) 
jeep_x = width // 2 
jeep_y = height - 150
jeep_angle = 0
rotation_speed = 3
jeep_speed_original = 0.9
jeep_speed = 0.9
reverse_speed = 0.3
jeep_img_rotated = jeep_img_original
aura_alpha = 0
engine_shake_x = 0 # DAGDAG ITO
engine_shake_y = 0 # DAGDAG ITO
# ======================================================
# S U P E R  S A I Y A N  B O O S T  S Y S T E M
# ======================================================
ss_charging = False         # Kung nka-hold ang left click
ss_charge_power = 0          # 0 to 100
max_boost_power = 100       # <--- DAGDAG MO ITONG LINE NA ITO
ss_charge_speed = 1.5       # Bilis ng pagpuno ng bar (dagdagan para mas mabilis mapuno)

ss_is_active = False        # Kung nka-boost na
ss_boost_duration = 3000    # Gaano katagal ang bilis (in milliseconds, 3000 = 3 seconds)
ss_boost_timer = 0          # Timer para sa duration
ss_speed_multiplier = 3.0   # Gaano kabilis kapag nka-boost (2.5x original speed)

# GAS CONSUMPTION VALUES
gas_consume_normal = 0.001   # Bawas gas kapag umaandar lang (mabagal lang natin)
gas_consume_charging = 0.03  #0.03 # Mabilis na bawas gas habang nagcha-charge (bago pa mag-boost)
gas_consume_boosting = 0.01  # Sobrang bilis na bawas gas habang nka-boost na

# ======================================================
# H E A L T H  S Y S T E M
# ======================================================
max_health = 100
current_health = 100
collision_damage = 10  # Bawas sa buhay kada bangga
last_damage_time = 0   # Para hindi maubos agad ang buhay sa isang dikit lang
damage_cooldown = 1000 # 1 second bago pwedeng mabawasan ulit

# ======================================================
# H O R N  W A V E  S E T U P
# ======================================================
horn_waves = []

# ======================================================
# G A S  S Y S T E M
# ======================================================
max_gas = 100
current_gas = 100
current_consume_rate = 0
gas_consumption = 0.01  # Bilis ng bawas ng gas

# ======================================================
# T I M E   S Y S T E M   (DAGDAG LANG)
# ======================================================
game_hour = 5
game_minute = 30
time_tick_speed = 2.0 # Bagalan natin para hindi masyadong mabilis ang lipas ng oras
time_counter = 0

# ======================================================
# R U S H  H O U R  S Y S T E M  (NEW)
# ======================================================
is_rush_hour = False
rush_hour_message = ""
rush_notif_timer = 0
rush_notif_duration = 6000 
rush_status = "NORMAL" # <--- DAGDAG ITO (NORMAL, WARNING, ACTIVE)

# ======================================================
# S M O K E  S E T U P
# ======================================================
smoke_particles = []


# ======================================================
# H E A D L I G H T   S Y S T E M
# ======================================================
headlight_on = False

# ======================================================
# N I G H T   M O D E   S E T U P
# ======================================================
night_alpha = 0  # 0 = Umaga (Maliwanag), 255 = Sobrang dilim

# --- COMING SOON NOTIFICATION ---
show_coming_soon = False
coming_soon_timer = 0
coming_soon_duration = 3000 # 2 seconds lang bago mawala
cs_alpha = 0
cs_y_offset = 0
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
# C A M E R A  S E T U P
# ======================================================
zoom_factor = 2.0
cam_x = 0
cam_y = 0

# ======================================================
# P A N E L S
# ======================================================
lose_panel = pygame.image.load("panel/YOU LOSE.png").convert_alpha()
lose_panel = pygame.transform.scale(lose_panel, (430, 350))

win_panel = pygame.image.load("panel/YOU WIN.png").convert_alpha()
win_panel = pygame.transform.scale(win_panel, (430, 350))

username_panel = pygame.image.load("panel/username.png").convert_alpha()
username_panel = pygame.transform.scale(username_panel, (430, 230))

about_panel = pygame.image.load("panel/about.png").convert_alpha()
about_panel = pygame.transform.scale(about_panel, (430, 290))

exit_panel = pygame.image.load("panel/exit.png").convert_alpha()
exit_panel = pygame.transform.scale(exit_panel, (430, 230))

saved_panel = pygame.image.load("panel/saved.png").convert_alpha()
saved_panel = pygame.transform.scale(saved_panel, (300, 150))

route_panel = pygame.image.load("panel/route.png").convert_alpha()
route_panel = pygame.transform.scale(route_panel, (430, 350))

pfp_panel = pygame.image.load("panel/PFP.png").convert_alpha()
pfp_panel = pygame.transform.scale(pfp_panel, (200, 60))
pfp_display_x = 15 #left right
pfp_display_y = 15 # up down

passenger_panel = pygame.image.load("panel/passenger_total.png").convert_alpha()
passenger_panel = pygame.transform.scale(passenger_panel, (150, 50))

# PASSENGERS
passenger1 = pygame.image.load("passenger/person1.png").convert_alpha()
# passenger1 = pygame.transform.scale(passenger1, (200, 60))

passenger2 = pygame.image.load("passenger/person2.png").convert_alpha()
# passenger2 = pygame.transform.scale(passenger2, (200, 60))

passenger3 = pygame.image.load("passenger/person3.png").convert_alpha()
# passenger3 = pygame.transform.scale(passenger3, (200, 60))

passenger4 = pygame.image.load("passenger/person4.png").convert_alpha()
# passenger4 = pygame.transform.scale(passenger4, (200, 60))

passenger5 = pygame.image.load("passenger/person5.png").convert_alpha()
# passenger5 = pygame.transform.scale(passenger5, (200, 60))

passenger6 = pygame.image.load("passenger/person6.png").convert_alpha()
# passenger6 = pygame.transform.scale(passenger6, (200, 60))

passenger7 = pygame.image.load("passenger/person7.png").convert_alpha()
# passenger7 = pygame.transform.scale(passenger7, (200, 60))


# ======================================================
# P A S S E N G E R  S Y S T E M
# ======================================================
# 1. Re-scale existing loaded images to be small (25x25 pixels)
passenger_imgs = [passenger1, passenger2, passenger3, passenger4, passenger5, passenger6, passenger7]
passenger_imgs = [pygame.transform.scale(img, (25, 25)) for img in passenger_imgs]


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
        self.message = "" # Reset message kada frame
        if self.is_leaving:
            self.pos.y -= 0.8
            self.alpha -= 5
            if self.alpha <= 0: self.respawn()
            return

        if self.is_riding:
            # Dito mo in-adjust yung bilis ng pag-para (1500)
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

# 3. Gawa ng 15 na tao sa map
passengers_on_map = [Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
jeep_passengers_count = 0

last_drop_time = 0

# --- QUOTA & DASHBOARD LOGIC (DAGDAG) ---
daily_quota = 300
total_earnings = 0
# --- FINAL SUMMARY CALCULATIONS ---
gas_price_per_unit = 6.0      # Halaga ng bawat 1% na gas na nagamit (P6.50)
show_win_panel = False        # Flag para lumabas ang summary panel
show_lose_panel = False
win_anim_counter = 0

passenger_types = ["Regular", "Student", "Senior", "PWD"]
stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
payment_notifs = [] # Para sa floating "+11" or "+13"

# ======================================================
# B U T T O N  R E C T S
# ======================================================
start_rect = button_start.get_rect(topleft=(308, 417))
about_rect = button_about.get_rect(topleft=(309, 487))
exit_rect = button_exit.get_rect(topleft=(309, 557))

confirm_rect = button_confirm.get_rect(topleft=(248, 350))
cancel_rect = button_cancel.get_rect(topleft=(435, 350))

cancel_green_rect = button_cancel_green.get_rect(topleft=(435, 350))
exit_confirm_rect = button_confirm_exit.get_rect(topleft=(248, 350))

caldag_rect = button_caldag.get_rect(topleft=(231, 234))
sandag_rect = button_sandag.get_rect(topleft=(232, 300))
lindag_rect = button_lindag.get_rect(topleft=(232, 364))
backmenu_rect = button_back_menu.get_rect(topleft=(232, 436))

# ======================================================
# P A N E L  P O S I T I O N 
# ======================================================
panel_x = (width - 430) // 2
panel_y = (height - 230) // 2

# ======================================================
# T E X T  I N P U T  U S E R N A M E
# ======================================================
user_text = ""
input_active = False 
cursor_visible = False
last_cursor_blink = pygame.time.get_ticks()

custom_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 20)
small_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 12)
medium_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 16)
dash_info_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 10)
# Dagdag mo ito sa font section
quota_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 10)
#========================================================
# T E X T  B O X
#=========================================================
input_rect = pygame.Rect(panel_x + 49, panel_y + 90, 310, 35)

#========================================================
# H O R N /B A C K S P A C E  S P A C E B A R
#========================================================
backspace_held = False
last_backspace_time = 0
backspace_delay = 400
backspace_speed = 50

# M A I N  M E N U  S P A C E B A R
space_held = False
last_space_time = 0

# =======================================================
# S T A T E S 
# =======================================================
hovered_start = False
hovered_about = False
hovered_exit = False
hovered_confirm = False
hovered_cancel = False
hovered_cancel_green = False
hovered_exit_confirm = False
hovered_caldag = False
hovered_sandag = False
hovered_lindag = False
hovered_backmenu = False
music_started = False
horn_playing = False

show_saved_panel = False
saved_alpha = 0          
fade_speed = 10        
fade_state = "in"        
saved_panel_time = 0
saved_duration = 1000

running = True
loading = True

progress = 0

#==========P A U S E  L O A D I N G===========
pause_points = [20, 40, 60, 80]
pause_index = 0

state = "menu"

# ======================================================
# M A I N  L O O P
# ======================================================
while running:
    dt = clock.get_time()

    for event in pygame.event.get():

        # =========================
        # Q U I T
        # =========================
        if event.type == pygame.QUIT:
            running = False

        # ======================================================
        # G L O B A L   B O O S T   I N P U T (HOLD TO CHARGE)
        # ======================================================
        if not loading and state == "caldag_screen" and current_gas > 0 and engine_on and not (show_win_panel or show_lose_panel):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    if not ss_is_active:
                        ss_charging = True
                        # --- START CHARGE SOUND ---
                        if not charge_playing:
                            powerup_sound.play(-1)
                            charge_playing = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Pag bitaw ng click
                    # --- STOP CHARGE SOUND AGAD ---
                    powerup_sound.stop()
                    charge_playing = False

                    if ss_charge_power >= 100 and not ss_is_active:
                        ss_is_active = True
                        ss_boost_timer = pygame.time.get_ticks()
                        jeep_speed = jeep_speed_original * ss_speed_multiplier
                    else:
                        ss_charge_power = 0
                    
                    ss_charging = False
        # ===============================
        # K E Y B O A R D  I N P U T
        # ===============================
        if not loading:
            if event.type == pygame.KEYDOWN:
                # --- CALDAG SCREEN KEYS (Moved here to avoid Attribute Error) ---
                # --- CALDAG SCREEN KEYS ---
                if state == "caldag_screen":
                    if event.key == pygame.K_ESCAPE: 
                        # --- 1. STOP ALL SOUNDS ---
                        start_jeep_radio(0) 
                        engine_idle_sound.stop()
                        reverse_sound.stop()
                        powerup_sound.stop()
                        speedup_sound.stop()
                        idle_playing = False
                        reverse_playing = False
                        music_started = False # Para bumalik ang main menu music
                        
                        # --- 2. RESET GAMEPLAY VARIABLES ---
                        current_gas = 100
                        current_health = 100
                        total_earnings = 0
                        jeep_passengers_count = 0
                        stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
                        
                        # --- 3. RESET POSITION & PHYSICS ---
                        jeep_x = width // 2 
                        jeep_y = height - 150
                        jeep_angle = 0
                        jeep_speed = jeep_speed_original
                        engine_on = False
                        is_starting = False
                        
                        # --- 4. RESET TIME & SYSTEMS ---
                        game_hour = 5
                        game_minute = 30
                        time_counter = 0
                        rush_status = "NORMAL"
                        is_rush_hour = False
                        night_alpha = 0
                        headlight_on = False
                        
                        # --- 5. CLEAN UP OBJECTS ---
                        smoke_particles = []
                        horn_waves = []
                        payment_notifs = []
                        # I-respawn ang mga tao sa random locations
                        passengers_on_map = [Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
                        
                        # --- 6. SWITCH STATE ---
                        state = "route"
                        print("Game Reset and Back to Route Selection")

                    # 2. Lahat ng ibang keys (E, R, Radio), i-wrap natin dito:
                    # Check kung WALA pang panel na nakasulpot
                    if not (show_win_panel or show_lose_panel):
                        if event.key == pygame.K_e:
                            headlight_on = not headlight_on
                            click_sound.play()
                            
                        if event.key == pygame.K_r:
                            if not engine_on and not is_starting:
                                is_starting = True
                                engine_start_sound.play()
                                engine_start_timer = pygame.time.get_ticks() 
                            elif engine_on:
                                engine_on = False
                                engine_idle_sound.stop()
                                idle_playing = False
                                click_sound.play()
                                ss_charging = False
                                ss_charge_power = 0
                                powerup_sound.stop()
                                charge_playing = False
                                
                        if event.key == pygame.K_RIGHT:
                            button_sound.play()
                            current_music_index = (current_music_index + 1) % len(playlist)
                            start_jeep_radio(current_music_index)
                            
                        if event.key == pygame.K_LEFT:
                            button_sound.play()
                            current_music_index = (current_music_index - 1) % len(playlist)
                            start_jeep_radio(current_music_index)

                # --- USERNAME KEYS ---
                if state == "username" and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                        backspace_held = True
                        last_backspace_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_SPACE:
                        if len(user_text) < 6:
                            user_text += " "
                            space_held = True
                            last_space_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                    else:
                        if len(user_text) < 6:
                            user_text += event.unicode
                            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = False
                if event.key == pygame.K_SPACE:
                    space_held = False

        # =========================
        # C L I C K  E V E N T S
        # =========================
        if not loading and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                if state == "caldag_screen" and (show_win_panel or show_lose_panel):
                    button_sound.play()
                    
                    # 1. STOP LOSE MUSIC
                    lose_sound.stop()
                    win_music.stop()
                    lose_music_playing = False
                    
                    music_started = False
                    # --- ETO ANG "FORCE RESTART" NG MUSIC ---
                    pygame.mixer.music.load("music/main bg music beep.mp3") # I-load ulit ang file
                    pygame.mixer.music.set_volume(0.4) # Siguraduhin na may volume
                    pygame.mixer.music.play(-1) # Patugtugin nang naka-loop
                    # ----------------------------------------
                    
                    
                    # RESET ALL FOR NEXT DAY / RETRY
                    total_earnings = 0
                    current_gas = 100
                    current_health = 100
                    jeep_passengers_count = 0
                    stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
                    
                    # 2. POSITION & PHYSICS RESET
                    jeep_x = width // 2 
                    jeep_y = height - 150
                    jeep_angle = 0
                    jeep_speed = jeep_speed_original
                    engine_on = False
                    is_starting = False
                    
                    # 3. TIME & SYSTEM RESET
                    game_hour = 5
                    game_minute = 30
                    time_counter = 0
                    rush_status = "NORMAL"
                    is_rush_hour = False
                    night_alpha = 0
                    headlight_on = False
                    
                    # 4. OBJECTS & PARTICLES RESET (Linisin ang mapa)
                    smoke_particles = []
                    horn_waves = []
                    payment_notifs = []
                    # I-reset ang mga tao sa mapa (babalik sa 15 na random)
                    passengers_on_map = [Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
                    
                    # 5. STATE & AUDIO RESET
                    show_win_panel = False
                    show_lose_panel = False
                    state = "menu"
                    
                    # --- SUPER SAIYAN RESET (DAGDAG MO ITO) ---
                    ss_charging = False
                    ss_is_active = False
                    ss_charge_power = 0
                    ss_boost_timer = 0
                    charge_playing = False
                    boost_sound_playing = False
                    jeep_speed = jeep_speed_original # Balik sa normal na bilis
                    
                    # Patayin ang mga sounds na baka nag-lo-loop
                    engine_idle_sound.stop()
                    reverse_sound.stop()
                    speedup_sound.stop()
                    powerup_sound.stop()
                    idle_playing = False
                    
                    start_jeep_radio(0) 
                    continue
                
                if state == "menu":
                    if start_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "username"

                    elif about_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "about"

                    elif exit_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "exit"
                        
                elif state == "username":
                    if input_rect.collidepoint(event.pos):
                        input_active = True
                        cursor_visible = True
                        last_cursor_blink = pygame.time.get_ticks()
                    else:
                        input_active = False
                        cursor_visible = False

                    if confirm_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "route"
                        show_saved_panel = True
                        saved_alpha = 0
                        fade_state = "in"
                        print("USERNAME:", user_text)

                    elif cancel_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "menu"
                        user_text = ""
                        input_active = False

                elif state == "exit":
                    if cancel_green_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "menu"
                    
                    elif exit_confirm_rect.collidepoint(event.pos):
                        button_sound.play()
                        running = False
                  
                elif state == "about":
                    state = "menu"
                    
                elif state == "route":
                    # --- BACK MENU CLICK ---
                    if backmenu_rect.collidepoint(event.pos):
                        button_sound.play()
                        state = "menu" 
                        print("Back to Menu")

                    # --- CAL DAG CLICK ---
                    elif caldag_rect.collidepoint(event.pos):
                        button_sound.play()
                        print("Starting Route: CALASIAO - DAGUPAN")
                        state = "caldag_screen"
                        start_jeep_radio(current_music_index) # <--- Simulan agad ang radyo pagpasok
                        
                    # --- SAN DAG CLICK ---
                    elif sandag_rect.collidepoint(event.pos):
                        button_sound.play()
                        show_coming_soon = True
                        coming_soon_timer = pygame.time.get_ticks()
                        print("Starting Route: SAN CARLOS - DAGUPAN")

                    # --- LIN DAG CLICK ---
                    elif lindag_rect.collidepoint(event.pos):
                        button_sound.play()
                        show_coming_soon = True
                        coming_soon_timer = pygame.time.get_ticks() # Simulan ang timer
                        print("Starting Route: LINGAYEN - DAGUPAN")

    # ==========================================
    # B A C K S P A C E  R E P E A T  L O G I C
    # ==========================================
    if backspace_held and input_active:
        now = pygame.time.get_ticks()
        if now - last_backspace_time > backspace_delay:
            user_text = user_text[:-1]
            last_backspace_time = now - (backspace_delay - backspace_speed)

    # ======================================
    # S P A C E  R E P E A T  L O G I C
    # =======================================
    if space_held and input_active:
        now = pygame.time.get_ticks()
        if now - last_space_time > backspace_delay:
            if len(user_text) < 16:
                user_text += " "
                last_space_time = now - (backspace_delay - backspace_speed)
    
    # ==========================================
    # U N I V E R S A L  H O R N  C O N T R O L
    # ==========================================
    # Para hindi maingay ang busina pag nanalo/natalo na
    if not loading and (state == "menu" or (state == "caldag_screen" and not (show_win_panel or show_lose_panel))):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            if not horn_playing:
                jeep_horn_sound.play(-1)
                horn_playing = True
            
            # WIFI EFFECT 
            if state == "caldag_screen" and random.randint(0, 5) == 0:
                radians = math.radians(jeep_angle)
                front_dist = 35 
                wave_x = jeep_x - front_dist * math.sin(radians)
                wave_y = jeep_y - front_dist * math.cos(radians)
                horn_waves.append([[wave_x, wave_y], 5, 255, jeep_angle])
        else:
            if horn_playing:
                jeep_horn_sound.stop()
                horn_playing = False              

    #======================================           
    #J E E P  S C R E E N
    #======================================         
    if state == "caldag_screen":
        keys = pygame.key.get_pressed()
        radians = math.radians(jeep_angle) 

        
        game_active = not (show_win_panel or show_lose_panel)
        
        if game_active:
        # --- STEERING (A at D) ---
            if keys[pygame.K_a]:
                jeep_angle += rotation_speed
            if keys[pygame.K_d]:
                jeep_angle -= rotation_speed

            # --- PASSENGER CORE LOGIC ---
            is_jeep_moving = keys[pygame.K_w] or keys[pygame.K_s]
            jeep_vec = pygame.Vector2(jeep_x, jeep_y)
            
            # ======================================================
            # B O O S T   L O G I C   &   G A S   C O N S U M P T I O N
            # ======================================================
            current_consume_rate = 0 # variable para sa total bawas gas sa frame na ito

            # 1. Habang nagmamaneho (Normal gas consumption)
            # 1. Habang nagmamaneho (Normal gas consumption) - Check engine_on
            if (keys[pygame.K_w] or keys[pygame.K_s]) and engine_on and not (show_win_panel or show_lose_panel):
                current_consume_rate = gas_consume_normal

            # 2. Habang nagcha-charge (MOUSE HOLD)
            if ss_charging and not ss_is_active and current_gas > 0:
                ss_charge_power += ss_charge_speed # Dagdag power
                current_consume_rate = gas_consume_charging # Mas mabilis bawas gas
                
                # Limit sa 100%
                if ss_charge_power > 100: ss_charge_power = 100
            # 3. Habang nka-boost (TURBO ACTIVE)
            if ss_is_active:
                current_consume_rate = gas_consume_boosting # Sobrang bilis bawas gas
                
                # --- START BOOST SOUND ---
                if not boost_sound_playing:
                    speedup_sound.play(-1)
                    boost_sound_playing = True
                
                # Check timer para patayin ang boost
                if pygame.time.get_ticks() - ss_boost_timer > ss_boost_duration:
                    ss_is_active = False
                    jeep_speed = jeep_speed_original # Balik sa normal speed
                    ss_charge_power = 0 # Reset charge
                    
                    # --- STOP BOOST SOUND ---
                    speedup_sound.stop()
                    boost_sound_playing = False
                    print("Boost ended.")
            
            # 4. APPLY GAS CONSUMPTION (Actual na bawas sa gas)
            if current_consume_rate > 0 and engine_on:
                current_gas -= current_consume_rate
                if current_gas <= 0:
                    current_gas = 0
                    
                    # --- ETO YUNG DINAGDAG NATIN ---
                    if not show_win_panel:
                        pygame.mixer.stop()
                        show_win_panel = True # Lalabas na ang panel pag 0 gas na
                        
                    # ------------------------------

                    # --- STOP ALL SOUNDS PARA MALINIS ---
                    powerup_sound.stop()
                    speedup_sound.stop()
                    engine_idle_sound.stop() # Stop din natin idle sound
                    charge_playing = False
                    boost_sound_playing = False
                    idle_playing = False
                    
                    # 3. I-off ang radyo (mahalaga ito para hindi bumalik ang tugtog)
                    start_jeep_radio(0) 
                    
                    # 4. Patugtugin ang Win Music
                    win_music.play(-1)
                    show_win_panel = True
                    
                    # Patayin ang boost kung naubusan ng gas
                    if ss_is_active:
                        ss_is_active = False
                        jeep_speed = jeep_speed_original
                        ss_charging = False
            
            anyone_wants_to_stop = any(p.has_requested for p in passengers_on_map)

            for p in passengers_on_map:
                was_riding = p.is_riding
                p.update(jeep_vec, is_jeep_moving, jeep_passengers_count)
        
                if p.is_riding and not was_riding:
                    if jeep_passengers_count < 18:
                        jeep_passengers_count += 1
                        # --- BAYAD LOGIC ---
                        p_type = random.choice(passenger_types)
                        fare = 11 if p_type in ["Student", "Senior", "PWD"] else 13
                        total_earnings += fare
                        stats[p_type] += 1
                        # Floating notification setup
                        payment_notifs.append([[jeep_screen_x, jeep_screen_y - 30], f"P{fare}", 255])
                        money_sound.play() 
                    else:
                        p.is_riding = False

            # --- SEQUENTIAL DROP-OFF ---
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_f] and not is_jeep_moving:
                
                for p in passengers_on_map:
                    if p.is_riding and p.has_requested:
                        
                        if current_time - last_drop_time > 1600:
                            p.is_riding = False
                            p.is_leaving = True
                            p.has_requested = False
                        
                            p.pos = pygame.Vector2(jeep_x + random.randint(-15, 15), jeep_y + random.randint(-15, 15))
                            jeep_passengers_count -= 1
                            last_drop_time = current_time # Reset timer
                            break 
            
            # --- MOVEMENT (W at S) ---
            # --- MOVEMENT (W at S) ---
            # --- MOVEMENT (W at S) WITH DAMAGE ---
            # --- ENGINE START DELAY CHECK ---
            # Pagkalipas ng 2000 milliseconds (2 seconds), mag-o-on ang makina
            if is_starting:
                if pygame.time.get_ticks() - engine_start_timer > 2000: 
                    engine_on = True
                    is_starting = False

            # --- NEW MOVEMENT CONDITION ---
            can_move = engine_on and current_gas > 0 and current_health > 0 and not show_win_panel

            if (keys[pygame.K_w] or keys[pygame.K_s]) and can_move:
                # --- LOW FUEL BEEP ---
                if current_gas <= 15 and random.randint(0, 80) == 0:
                    reverse_sound.play()
                    
                if keys[pygame.K_w]:
                    new_x = jeep_x - jeep_speed * math.sin(radians)
                    new_y = jeep_y - jeep_speed * math.cos(radians)
                    jeep_rect = pygame.Rect(0, 0, 25, 45)
                    jeep_rect.center = (new_x, new_y)
                    
                    collision = False
                    for wall in house_hitboxes:
                        if jeep_rect.colliderect(wall):
                            collision = True
                            curr_t = pygame.time.get_ticks()
                            if curr_t - last_damage_time > damage_cooldown:
                                current_health -= collision_damage
                                last_damage_time = curr_t
                                accident_sound.play() 
                                
                                # --- SMOKE ON COLLISION ---
                                for _ in range(8): # Bugso ng usok pagkabangga
                                    smoke_particles.append([[jeep_x, jeep_y], random.randint(4, 8), 200])
                            break
                        
                    if not collision: jeep_x, jeep_y = new_x, new_y

                elif keys[pygame.K_s]:
                    # 1. TUNOG NG PAG-ATRAS
                    if not reverse_playing:
                        reverse_sound.play(-1)
                        reverse_playing = True

                    # 2. ACTUAL NA PAG-GALAW (Siguraduhin na hindi ito naka-indent sa loob ng if not reverse_playing)
                    new_x = jeep_x + reverse_speed * math.sin(radians)
                    new_y = jeep_y + reverse_speed * math.cos(radians)
                    
                    jeep_rect = pygame.Rect(0, 0, 25, 45)
                    jeep_rect.center = (new_x, new_y)
                    
                    collision = False
                    for wall in house_hitboxes:
                        if jeep_rect.colliderect(wall):
                            collision = True
                            curr_t = pygame.time.get_ticks()
                            if curr_t - last_damage_time > damage_cooldown:
                                current_health -= collision_damage
                                last_damage_time = curr_t
                                accident_sound.play()
                            break
                    if not collision: jeep_x, jeep_y = new_x, new_y
                    
            # --- STOP REVERSE SOUND ---
            # Pag binitawan ang S o naubusan ng gas, stop ang beep
            if not keys[pygame.K_s] or current_gas <= 0:
                if reverse_playing:
                    reverse_sound.stop()
                    reverse_playing = False
            
            # 4. IMAGE ROTATION UPDATE
            jeep_img_rotated = pygame.transform.rotate(jeep_img_original, jeep_angle)
            
            # Titigil lang ang jeep kung may gas PA at hindi pa sira (health > 0)
            if (keys[pygame.K_w] or keys[pygame.K_s]) and current_gas > 0 and current_health > 0:
                #FOR SMOKE
                radians = math.radians(jeep_angle)
                offset = 40 
                smoke_x = jeep_x + offset * math.sin(radians)
                smoke_y = jeep_y + offset * math.cos(radians)
                smoke_particles.append([[smoke_x, smoke_y], random.randint(3, 8), 200])

            # Update at Fade-out logic
            for particle in smoke_particles[:]:
                particle[2] -= 8  
                particle[1] += 0.5 
                if particle[2] <= 0:
                    smoke_particles.remove(particle) 
                    
            cam_x = jeep_x - (width / 2) / zoom_factor
            cam_y = jeep_y - (height / 2) / zoom_factor
            
            # --- TIME PROGRESSION LOGIC (DAGDAG LANG) ---
            time_counter += time_tick_speed
            if time_counter >= 60:
                game_minute += 1
                time_counter = 0
            if game_minute >= 60:
                game_hour += 1
                game_minute = 0
            if game_hour >= 20 and game_minute >= 30: # Stop sa 8:30 PM
                game_hour = 20
                game_minute = 30
                
                if not show_win_panel:
                    pygame.mixer.stop()
                    win_music.play(-1)
                    show_win_panel = True
                    
            # --- DYNAMIC DARKNESS LOGIC (6 PM - 7 PM) ---
            if game_hour == 18: # 6 PM
                # Ang 60 minutes ay unti-unting mag-aadjust ng alpha mula 0 to 150
                # (60 minutes * 2.5 = 150 alpha)
                night_alpha = game_minute * 2.5 
            elif game_hour >= 19: # 7 PM onwards
                night_alpha = 200 # Max na dilim (para kita pa rin ang laro, huwag nating i-255)
            else:
                night_alpha = 0 # Umaga
            
            # --- RUSH HOUR TRACKER LOGIC ---
            new_status = "NORMAL"
            # 7:30 AM - 7:59 AM (Warning) | 3:30 PM - 3:59 PM (Warning)
            if (game_hour == 7 and game_minute >= 30) or (game_hour == 15 and game_minute >= 30):
                new_status = "WARNING"
            # 8:00 AM - 10:00 AM (Active) | 4:00 PM - 7:00 PM (Active)
            elif (8 <= game_hour < 10) or (16 <= game_hour < 19):
                new_status = "ACTIVE"

            if new_status != rush_status:
                rush_status = new_status
                rush_notif_timer = pygame.time.get_ticks() 
                if rush_status != "NORMAL":
                    button_sound.play()

            # --- IMPROVED RUSH HOUR SPAWNING ---
            if rush_status == "ACTIVE":
                is_rush_hour = True
                # Itaas natin sa 40 ang limit para siksikan talaga
                if len(passengers_on_map) < 55: 
                    # Binabaan ko ang random (1, 100) para mas mabilis silang mag-appear
                    if random.randint(1, 100) == 1: 
                        new_p = Passenger(random.randint(50, 800), random.randint(50, 600))
                        # Siguraduhin na hindi sila sasakay agad, kailangan tumigil ka muna
                        passengers_on_map.append(new_p)
            else:
                is_rush_hour = False
                # Kapag normal hours, dahan-dahang ibalik sa 15 ang dami ng tao
                if len(passengers_on_map) > 15:
                    if random.randint(1, 30) == 1: # Bilis ng pag-alis ng multo
                        for p in passengers_on_map:
                            # Alisin lang ang mga tambay (hindi sumasakay, hindi nakasakay)
                            if not p.is_riding and not p.approaching and not p.is_leaving:
                                passengers_on_map.remove(p)
                                break # Isa-isa lang ang pag-alis para smooth
        
    screen.fill((0, 0, 0))

    # ======================================================
    # L O A D I N G  S C R E E N
    # ======================================================
    if loading:
        pygame.draw.rect(screen, (255, 255, 255), (5, height - 15, width - 10, 10), 1)

        fill_width = int((progress / 100) * (width - 10))
        pygame.draw.rect(screen, (0, 255, 0), (5, height - 15, fill_width, 10))

        progress += 5

        if pause_index < len(pause_points):
            if progress >= pause_points[pause_index]:
                progress = pause_points[pause_index]
                time.sleep(0.7)
                pause_index += 1

        if progress >= 100:
            progress = 100
            loading = False

        pygame.display.update()
        pygame.time.delay(25)

    # ======================================================
    # M A I N  S C R E E N S
    # ======================================================
    else:
        if not music_started:
            pygame.mixer.music.play(-1, fade_ms=2000)
            music_started = True

        # =========================
        # M E N U
        # =========================
        if state == "menu":
            ret, frame = video.read()

            if not ret:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(bg_surface, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            
            #===========================================
            # H O V E R + S O U N D
            #===========================================
            # S T A R T
            if start_rect.collidepoint(mouse_pos):
                if not hovered_start:
                    button_sound.play()
                    hovered_start = True
                screen.blit(button_start_hover, start_rect)
            else:
                screen.blit(button_start, start_rect)
                hovered_start = False

            # A B O U T
            if about_rect.collidepoint(mouse_pos):
                if not hovered_about:
                    button_sound.play()
                    hovered_about = True
                screen.blit(button_about_hover, about_rect)
            else:
                screen.blit(button_about, about_rect)
                hovered_about = False

            # E X I T
            if exit_rect.collidepoint(mouse_pos):
                if not hovered_exit:
                    button_sound.play()
                    hovered_exit = True
                    
                #S H A K E  O F  E X I T
                shake_x = random.randint(-2, 2)
                shake_y = random.randint(-2, 2)
                screen.blit(button_exit_hover, (exit_rect.x + shake_x, exit_rect.y + shake_y))
            else:
                screen.blit(button_exit, exit_rect)
                hovered_exit = False

        # =========================
        # U S E R N A M E  S C R E E N
        # =========================
        elif state == "username":
            ret, frame = blurdbg_vid.read()

            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(bg_surface, (0, 0))
                
            # O V E R L A Y
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 70))
            screen.blit(overlay, (0, 0))

            screen.blit(username_panel, (panel_x, panel_y))

            # === R E N D E R T E X T ===
            text_surf = custom_font.render(user_text, True, (0, 0, 0))
            screen.blit(text_surf, (input_rect.x + 10, input_rect.y + 5))

            # === B L I N K I N G  C U R S O R ===
            if input_active:
                curr_time = pygame.time.get_ticks()
                if curr_time - last_cursor_blink > 500:
                    cursor_visible = not cursor_visible
                    last_cursor_blink = curr_time
                
                if cursor_visible:
                    cursor_x = input_rect.x + 10 + text_surf.get_width() + 2
                    pygame.draw.line(screen, (0, 0, 0), (cursor_x, input_rect.y + 2), (cursor_x, input_rect.y + 25), 2)

            mouse_pos = pygame.mouse.get_pos()

            # C O N F I R M  H O V E R + S O U N D
            if confirm_rect.collidepoint(mouse_pos):
                if not hovered_confirm:
                    button_sound.play()
                    hovered_confirm = True
                screen.blit(button_confirm_hover, confirm_rect)
            else:
                screen.blit(button_confirm, confirm_rect)
                hovered_confirm = False

            # C A N C E L  H O V E R + S O U N D
            if cancel_rect.collidepoint(mouse_pos):
                if not hovered_cancel:
                    button_sound.play()
                    hovered_cancel = True
                screen.blit(button_cancel_hover, (cancel_rect.x + 5, cancel_rect.y))
            else:
                screen.blit(button_cancel, cancel_rect)
                hovered_cancel = False
                
        # =========================
        # A B O U T  S C R E E N 
        # =========================
        elif state == "about":
            ret, frame = blurdbg_vid.read()

            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(bg_surface, (0, 0))
                
            #O V E R L A Y
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            screen.blit(overlay, (0, 0))

            screen.blit(about_panel, (panel_x, panel_y))

            font = pygame.font.SysFont("arial", 18, bold=True)
            hint_text = font.render("Press anywhere to back", True, (255, 255, 255))

            hint_x = (width - hint_text.get_width()) // 2
            hint_y = height - 40

            screen.blit(hint_text, (hint_x, hint_y))
            
        #======================================
        # E X I T S C R E E N
        #======================================
        elif state == "exit":
            ret, frame = blurdbg_vid.read()

            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(bg_surface, (0, 0))
                
            #O V E R L A Y
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 70))
            screen.blit(overlay, (0, 0))

            screen.blit(exit_panel, (panel_x, panel_y))

            mouse_pos = pygame.mouse.get_pos()

            # E X I T  H O V E R + S O U N D
            if exit_confirm_rect.collidepoint(mouse_pos):
                if not hovered_exit_confirm:
                    button_sound.play()
                    hovered_exit_confirm = True
                    
                shake_x = random.randint(-2, 2)
                shake_y = random.randint(-2, 2)
                
                screen.blit(button_confirm_exit_hover, (exit_confirm_rect.x + shake_x, exit_confirm_rect.y + shake_y))
            else:
                screen.blit(button_confirm_exit, exit_confirm_rect)
                hovered_exit_confirm = False
                
            # C A N C E L  H O V E R + S O U N D
            if cancel_green_rect.collidepoint(mouse_pos):
                if not hovered_cancel_green:
                    button_sound.play()
                    hovered_cancel_green = True
                screen.blit(button_cancel_green_hover, (cancel_green_rect.x + 5, cancel_green_rect.y))
            else:
                screen.blit(button_cancel_green, cancel_green_rect)
                hovered_cancel_green = False
                
        # =============================
        # R O U T E  S E L E C T I O N 
        # ==============================
        elif state == "route":
            ret, frame = blurdbg_vid.read()
            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(bg_surface, (0, 0))
                
            # O V E R L A Y
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 70))
            screen.blit(overlay, (0, 0))

            screen.blit(route_panel, (panel_x, panel_y - 48))
            
            mouse_pos = pygame.mouse.get_pos()

            # --- DRAW BUTTONS WITH HOVER LOGIC ---
            
            # CAL DAG
            if caldag_rect.collidepoint(mouse_pos):
                if not hovered_caldag:
                    button_sound.play()
                    hovered_caldag = True
                screen.blit(button_caldag_hover, caldag_rect)
            else:
                screen.blit(button_caldag, caldag_rect)
                hovered_caldag = False

            # SAN DAG
            if sandag_rect.collidepoint(mouse_pos):
                if not hovered_sandag:
                    button_sound.play()
                    hovered_sandag = True
                screen.blit(button_sandag_hover, sandag_rect)
            else:
                screen.blit(button_sandag, sandag_rect)
                hovered_sandag = False

            # LIN DAG
            if lindag_rect.collidepoint(mouse_pos):
                if not hovered_lindag:
                    button_sound.play()
                    hovered_lindag = True
                screen.blit(button_lindag_hover, lindag_rect)
            else:
                screen.blit(button_lindag, lindag_rect)
                hovered_lindag = False

            # BACK MENU
            if backmenu_rect.collidepoint(mouse_pos):
                if not hovered_backmenu:
                    button_sound.play()
                    hovered_backmenu = True
                screen.blit(button_backmenu_hover, backmenu_rect)
            else:
                screen.blit(button_back_menu, backmenu_rect)
                hovered_backmenu = False

            # --- COMING SOON TEXT ONLY WITH FLOAT & FADE ---
            if show_coming_soon:
                current_time = pygame.time.get_ticks()
                elapsed = current_time - coming_soon_timer
                
                # 1. FADE LOGIC (Alpha: 0 to 255 then back to 0)
                if elapsed < 500: # Fade In
                    cs_alpha = int((elapsed / 500) * 255)
                elif elapsed > (coming_soon_duration - 500): # Fade Out
                    remaining = coming_soon_duration - elapsed
                    cs_alpha = int((remaining / 500) * 255)
                else:
                    cs_alpha = 255
                
                # 2. FLOAT LOGIC (Aangat ang text habang tumatagal)
                # Magsisimula sa 0, aakyat hanggang -40 pixels
                cs_y_offset = int((elapsed / coming_soon_duration) * -40)

                if elapsed < coming_soon_duration:
                    # Render the text
                    # Gumamit tayo ng matingkad na kulay (Yellow or Cyan) para lutang sa dark bg
                    cs_text = custom_font.render("COMING SOON!", True, (255, 215, 0)) 
                    
                    # I-apply ang Alpha (Fade) sa text surface
                    # Note: Kailangan convert_alpha() ang font surface or set_alpha
                    cs_text.set_alpha(cs_alpha)
                    
                    # Positions: Center x, and specific y with offset
                    text_x = (width // 2) - (cs_text.get_width() // 2)
                    text_y = 550 + cs_y_offset # 550 ang starting point, mababawasan ng offset kaya aangat
                    
                    # Draw a simple shadow behind the text (Optional, para mas mabasa)
                    shadow_surf = custom_font.render("COMING SOON!", True, (0, 0, 0))
                    shadow_surf.set_alpha(int(cs_alpha * 0.5)) # Mas transparent na shadow
                    screen.blit(shadow_surf, (text_x + 2, text_y + 2)) # Shadow offset
                    
                    # Draw the main fading/floating text
                    screen.blit(cs_text, (text_x, text_y))
                else:
                    show_coming_soon = False
            
        # ======================================================
            # C A L D A G   R O U T E   D I S P L A Y
            # ======================================================
        elif state == "caldag_screen":
            # 1. CAMERA LOGIC:
            cam_x = jeep_x - (width / 2) / zoom_factor
            cam_y = jeep_y - (height / 2) / zoom_factor

            if jeep_x < 20: jeep_x = 20
            if jeep_x > width - 20: jeep_x = width - 20
            if jeep_y < 35: jeep_y = 35
            if jeep_y > height - 35: jeep_y = height - 35
            
            cam_x = jeep_x - (width / 2) / zoom_factor
            cam_y = jeep_y - (height / 2) / zoom_factor
            
            # LIMITS: of the jeep sa mapa
            if cam_x < 0: cam_x = 0
            if cam_x > width - (width / zoom_factor): cam_x = width - (width / zoom_factor)
            
            if cam_y < 0: cam_y = 0
            if cam_y > height - (height / zoom_factor): cam_y = height - (height / zoom_factor)
            
            # 2. DRAW BACKGROUND 
            bg_w = int(width * zoom_factor)
            bg_h = int(height * zoom_factor)
            scaled_bg = pygame.transform.scale(route_caldag_img, (bg_w, bg_h))
            
            # --- SHAKE CALCULATION ---
            s_offset_x = 0
            s_offset_y = 0
            # Shake effect kapag bagong bangga (loob ng 150 milliseconds)
            if pygame.time.get_ticks() - last_damage_time < 150:
                s_offset_x = random.randint(-6, 6)
                s_offset_y = random.randint(-6, 6)

            bg_draw_x = (-cam_x * zoom_factor) + s_offset_x
            bg_draw_y = (-cam_y * zoom_factor) + s_offset_y
            screen.blit(scaled_bg, (bg_draw_x, bg_draw_y))
        
        # --- DEBUG DRAWING NG MGA BAHAY ---
            if SHOW_HITBOXES:
                for wall in house_hitboxes:
                    draw_x = (wall.x - cam_x) * zoom_factor
                    draw_y = (wall.y - cam_y) * zoom_factor
                    draw_w = wall.width * zoom_factor
                    draw_h = wall.height * zoom_factor
                    
                    debug_surf = pygame.Surface((draw_w, draw_h), pygame.SRCALPHA)
                    debug_surf.fill((255, 0, 0, 100)) 
                    screen.blit(debug_surf, (draw_x, draw_y))
                    pygame.draw.rect(screen, (255, 0, 0), (draw_x, draw_y, draw_w, draw_h), 2)
            
            # ------------------------------------------------------
            # 1. JEEP DEFINITION & DRAWING (MUNA)
            # ------------------------------------------------------
            # DITO NATIN GAGAWIN YUNG VARIABLE NA 'jeep_scaled' PARA HINDI NA MAG-ERROR
            jeep_scaled = pygame.transform.rotozoom(jeep_img_original, jeep_angle, zoom_factor)
            
            # Screen position ng jeep
            jeep_screen_x = (jeep_x - cam_x) * zoom_factor
            jeep_screen_y = (jeep_y - cam_y) * zoom_factor
            
            # --- ENGINE SHAKE CALCULATION ---
            engine_shake_x = 0
            engine_shake_y = 0
            if engine_on:
                if not idle_playing:
                    engine_idle_sound.play(-1)
                    idle_playing = True
                engine_shake_x = random.uniform(-0.7, 0.7)
                engine_shake_y = random.uniform(-0.7, 0.7)

            # Idagdag ang offset dito sa center
            # --- ENGINE SHAKE CALCULATION ---
            engine_shake_x = 0
            engine_shake_y = 0
            if engine_on:
                if not idle_playing:
                    engine_idle_sound.play(-1)
                    idle_playing = True
                # Subtle vibration
                engine_shake_x = random.uniform(-2.0, 2.0)
                engine_shake_y = random.uniform(-2.0, 2.0)
                # Mas malakas na shake pag nagcha-charge ng boost
                if ss_charging:
                    engine_shake_x = random.uniform(-2.5, 2.5)
                    engine_shake_y = random.uniform(-2.5, 2.5)

            # Idagdag ang shake sa final rect position
            rect = jeep_scaled.get_rect(center=(jeep_screen_x + s_offset_x + engine_shake_x, 
                                               jeep_screen_y + s_offset_y + engine_shake_y))

            # Drawing the Jeep based on SS/Boost state
            if (ss_charging or ss_is_active) and engine_on:
                glow_overlay = jeep_scaled.copy()
                glow_color = (255, 255, 0) if not ss_is_active else (255, 150, 0)
                glow_overlay.fill(glow_color, special_flags=pygame.BLEND_RGB_ADD)
                glow_overlay.set_alpha(random.randint(60, 160))
                
                if ss_charging:
                    rect.x += random.randint(-3, 3)
                    rect.y += random.randint(-3, 3)
                
                screen.blit(jeep_scaled, rect)
                screen.blit(glow_overlay, rect)
            else:
                screen.blit(jeep_scaled, rect)

            # ------------------------------------------------------
            # 2. DRAW USOK AT APOY (PAGKATAPOS NG JEEP - PARA NASA IBABAW)
            # ------------------------------------------------------
            for p in smoke_particles:
                p_draw_x = (p[0][0] - cam_x) * zoom_factor
                p_draw_y = (p[0][1] - cam_y) * zoom_factor
                p_radius = int(p[1] * zoom_factor)
                
                is_fire = p[3] if len(p) > 3 else False
                
                if is_fire:
                    color = p[4] if len(p) > 4 else (255, 100, 0)
                    p[0][1] -= 0.7  # Rising effect paitaas
                else:
                    color = (120, 120, 120)
                    p[0][1] -= 0.3

                # Surface para sa bawat particle
                s_surf = pygame.Surface((p_radius*2, p_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s_surf, (*color, p[2]), (p_radius, p_radius), p_radius)
                
                if is_fire:
                    screen.blit(s_surf, (p_draw_x - p_radius, p_draw_y - p_radius), special_flags=pygame.BLEND_RGBA_ADD)
                else:
                    screen.blit(s_surf, (p_draw_x - p_radius, p_draw_y - p_radius))
            
            # --- DRAW PASSENGERS ON MAP ---
            for p in passengers_on_map:
                if not p.is_riding and p.alpha > 0:
                    p_x = (p.pos.x - cam_x) * zoom_factor
                    p_y = (p.pos.y - cam_y) * zoom_factor
                    
                    p_surf = pygame.transform.scale(p.image, (int(25 * zoom_factor), int(25 * zoom_factor)))
                    if p.is_leaving:
                        p_surf.set_alpha(p.alpha) # Fade effect

                    p_rect = p_surf.get_rect(center=(p_x, p_y))
                    screen.blit(p_surf, p_rect)
                    
                    # --- SPEECH BUBBLE DRAWING ---
                    if p.message != "":
                        # Render text
                        m_surf = small_font.render(p.message, True, (0, 0, 0))
                        m_rect = m_surf.get_rect(center=(p_x, p_y - 40))
                        
                        # Bubble Background
                        bg_rect = m_rect.inflate(10, 10)
                        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=5)
                        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 1, border_radius=5)
                        
                        # Text blit
                        screen.blit(m_surf, m_rect)
                    
            # 4. DRAW JEEP (center camera follow)
            jeep_scaled = pygame.transform.rotozoom(jeep_img_original, jeep_angle, zoom_factor)
            
            # Screen position jeep
            jeep_screen_x = (jeep_x - cam_x) * zoom_factor
            jeep_screen_y = (jeep_y - cam_y) * zoom_factor
            
            # --- ENGINE SHAKE CALCULATION ---
            engine_shake_x = 0
            engine_shake_y = 0
            if engine_on:
                if not idle_playing:
                    engine_idle_sound.play(-1)
                    idle_playing = True
                engine_shake_x = random.uniform(-0.8, 0.8)
                engine_shake_y = random.uniform(-0.8, 0.8)

            # Idagdag ang engine_shake sa center calculation
            rect = jeep_scaled.get_rect(center=(jeep_screen_x + s_offset_x + engine_shake_x, 
                                               jeep_screen_y + s_offset_y + engine_shake_y))
            
            rect = jeep_scaled.get_rect(center=(jeep_screen_x, jeep_screen_y))
            
            # ======================================================
            # S U P E R  S A I Y A N  A U R A  (GLOW EFFECT)
            # ======================================================
            if (ss_charging or ss_is_active) and engine_on:
                aura_alpha = random.randint(100, 200) 
                
                if ss_is_active:
                    aura_color = (255, 100, 0, aura_alpha) # Orange/Fire mode
                else:
                    aura_color = (255, 255, 0, aura_alpha) # Normal Yellow charge
                
                for _ in range(random.randint(5, 10)):
                    offset_x = random.randint(int(-30 * zoom_factor), int(30 * zoom_factor))
                    offset_y = random.randint(int(-40 * zoom_factor), int(40 * zoom_factor))
                    glow_radius = random.randint(2, 6)
                    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surf, aura_color, (glow_radius, glow_radius), glow_radius)
                    screen.blit(glow_surf, (jeep_screen_x + offset_x, jeep_screen_y + offset_y))

                big_aura_radius = int(50 * zoom_factor)
                big_aura_surf = pygame.Surface((big_aura_radius * 2, big_aura_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(big_aura_surf, (255, 200, 0, 50), (big_aura_radius, big_aura_radius), big_aura_radius)
                screen.blit(big_aura_surf, (jeep_screen_x - big_aura_radius, jeep_screen_y - big_aura_radius))

            # ======================================================
            # J E E P  G L O W  &  S H A K E
            # ======================================================
            if (ss_charging or ss_is_active) and engine_on:
                glow_overlay = jeep_scaled.copy()
                glow_color = (255, 255, 0) if not ss_is_active else (255, 150, 0)
                glow_overlay.fill(glow_color, special_flags=pygame.BLEND_RGB_ADD)
                glow_overlay.set_alpha(random.randint(60, 160))
                
                if ss_charging:
                    rect.x += random.randint(-3, 3)
                    rect.y += random.randint(-3, 3)
                
                screen.blit(jeep_scaled, rect)
                screen.blit(glow_overlay, rect)
            else:
                screen.blit(jeep_scaled, rect)
            
            # ======================================================
            # DRAW BOOST CHARGE BAR (ABOVE JEEP)
            # ======================================================
            if (ss_charging or ss_is_active or ss_charge_power > 0) and engine_on:
                bar_w = int(40 * zoom_factor)
                bar_h = int(5 * zoom_factor)
                bar_x = jeep_screen_x - (bar_w // 2)
                bar_y = jeep_screen_y - (rect.height // 2) - int(10 * zoom_factor)
                pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_w, bar_h))
                fill_w = int((ss_charge_power / max_boost_power) * bar_w)
                bar_color = (255, 215, 0) # Gold
                if ss_charge_power >= 100: bar_color = (255, 100, 0) # Orange
                if ss_charge_power > 0:
                    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
                if ss_charge_power >= 100:
                    ss_text = custom_font.render("SUPER JEEP!", True, (255, 255, 0))
                    text_x = jeep_screen_x - (ss_text.get_width() // 2)
                    text_y = bar_y - ss_text.get_height() - 5
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                         outline_surf = custom_font.render("SUPER JEEP!", True, (150, 0, 0))
                         screen.blit(outline_surf, (text_x + dx, text_y + dy))
                    screen.blit(ss_text, (text_x, text_y))
            
            # === WIFI DRAWING ===
            for wave in horn_waves[:]:
                wave[1] += 3   
                wave[2] -= 15  
                if wave[2] <= 0:
                    horn_waves.remove(wave)
                else:
                    d_x = (wave[0][0] - cam_x) * zoom_factor
                    d_y = (wave[0][1] - cam_y) * zoom_factor
                    s_rad = int(wave[1] * zoom_factor)
                    surf = pygame.Surface((s_rad * 2, s_rad * 2), pygame.SRCALPHA)
                    s_arc = math.radians(wave[3] + 65)
                    e_arc = math.radians(wave[3] + 115)
                    pygame.draw.arc(surf, (255, 255, 255, wave[2]), (0, 0, s_rad * 2, s_rad * 2), s_arc, e_arc, 3)
                    screen.blit(surf, (d_x - s_rad, d_y - s_rad))
            
            # --- NIGHT OVERLAY DRAWING ---
            if night_alpha > 0:
                night_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                night_overlay.fill((0, 0, 20, int(night_alpha))) 

                if headlight_on:
                    rad = math.radians(jeep_angle)
                    
                    # 1. Distansya mula sa center
                    forward_dist = 35 * zoom_factor 
                    side_dist = 11 * zoom_factor 
                    
                    light_positions = [
                        (jeep_screen_x - forward_dist * math.sin(rad) - side_dist * math.cos(rad),
                         jeep_screen_y - forward_dist * math.cos(rad) + side_dist * math.sin(rad)),
                        (jeep_screen_x - forward_dist * math.sin(rad) + side_dist * math.cos(rad),
                         jeep_screen_y - forward_dist * math.cos(rad) - side_dist * math.sin(rad))
                    ]

                    combined_beams = pygame.Surface((width, height), pygame.SRCALPHA)
                    
                    for pos in light_positions:
                        for layer in range(6):
                            beam_len = (180 + (layer * 20)) * zoom_factor 
                            spread = math.radians(15 + (layer * 5))
                            
                            p1 = pos
                            p2 = (pos[0] - beam_len * math.sin(rad - spread),
                                  pos[1] - beam_len * math.cos(rad - spread))
                            p3 = (pos[0] - beam_len * math.sin(rad + spread),
                                  pos[1] - beam_len * math.cos(rad + spread))

                            base_brightness = 450
                            alpha_val = min(255, max(0, int(base_brightness - (layer * 20))))
                            
                            pygame.draw.polygon(combined_beams, (0, 0, 0, alpha_val), [p1, p2, p3])   
                    night_overlay.blit(combined_beams, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)     
                screen.blit(night_overlay, (0, 0))
            
            # --- PFP PANEL (KALIWA) ---
            screen.blit(pfp_panel, (pfp_display_x, pfp_display_y))
            pfp_user_surf = custom_font.render(user_text, True, (255, 255, 255))
            screen.blit(pfp_user_surf, (pfp_display_x + 65, pfp_display_y + 19))

            # --- PASSENGER PANEL (SA ILALIM NG PFP) ---
            pass_panel_y_pos = pfp_display_y + pfp_panel.get_height() + 5
            screen.blit(passenger_panel, (pfp_display_x, pass_panel_y_pos))

            # --- JEEP RADIO PANEL (TOP RIGHT) ---
            radio_x = width - 180
            radio_y = 75
            
            # Panel Background
            radio_bg_rect = pygame.Rect(radio_x, radio_y, 160, 65)
            # Gumawa ng semi-transparent box
            radio_surf = pygame.Surface((160, 65), pygame.SRCALPHA)
            radio_surf.fill((0, 0, 0, 150)) 
            screen.blit(radio_surf, (radio_x, radio_y))
            pygame.draw.rect(screen, (255, 255, 255), radio_bg_rect, 2, border_radius=8)

            # Arrows Text
            l_arrow = custom_font.render("<", True, (255, 255, 255))
            r_arrow = custom_font.render(">", True, (255, 255, 255))
            screen.blit(l_arrow, (radio_x + 15, radio_y + 35))
            screen.blit(r_arrow, (radio_x + 130, radio_y + 35))

            # Radio Label
            radio_label = small_font.render("JEEP RADIO", True, (200, 200, 200))
            screen.blit(radio_label, (radio_x + 23, radio_y + 10)) 

            # Current Song Name
            curr_song = playlist[current_music_index]["name"]
            if curr_song == "OFF":
                song_txt = small_font.render(curr_song, True, (255, 0, 0))
            else:
                song_txt = small_font.render(curr_song, True, (255, 215, 0))

            song_x_pos = radio_x + (80 - (song_txt.get_width() // 2)) + 3
            screen.blit(song_txt, (song_x_pos, radio_y + 35))    
                
            if jeep_passengers_count >= 18:
                indicator_surf = small_font.render("FULL!", True, (255, 0, 0))
            else:
                indicator_surf = small_font.render(f"{jeep_passengers_count}/18", True, (255, 255, 255))
            screen.blit(indicator_surf, (pfp_display_x + 73, pass_panel_y_pos + 27))
            
            # --- DIGITAL CLOCK DISPLAY ---
            display_hour = game_hour
            am_pm = "AM"
            if game_hour >= 12:
                am_pm = "PM"
                if game_hour > 12: display_hour -= 12
            
            time_string = f"{display_hour:02}:{game_minute:02} {am_pm}"
            time_surf = custom_font.render(time_string, True, (255, 255, 255))
            
            box_width = 200 
            box_height = 50
            box_x = (width // 2) - (box_width // 2)
            box_y = 15
            
            time_bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, (0, 0, 0, 150), time_bg_rect, border_radius=12) 
            pygame.draw.rect(screen, (255, 255, 255), time_bg_rect, 2, border_radius=12) 
            
            text_x = (width // 2) - (time_surf.get_width() // 2)
            text_y = box_y + (box_height // 2) - (time_surf.get_height() // 2)
            screen.blit(time_surf, (text_x, text_y))
            
            # # ------------------------------------------------------
            # # DITO MO I-PASTE (ENGINE INDICATOR)
            # # ------------------------------------------------------
            # eng_col = (0, 255, 0) if engine_on else (255, 0, 0)
            # if is_starting: eng_col = (255, 255, 0)
            # eng_txt = "ENGINE: ON" if engine_on else "ENGINE: OFF"
            # if is_starting: eng_txt = "STARTING..."
            
            # eng_surf = small_font.render(eng_txt, True, eng_col)
            # screen.blit(eng_surf, (gas_x, gas_y - 35)) 

            # # # --- GAS & CONDITION BARS WITH PERCENTAGE ---
            # # bar_w, bar_h = 130, 18
            
            # # --- Fuel Bar ---
            # gas_x, gas_y = 25, height - 35
            
            # # --- GAS & CONDITION BARS WITH PERCENTAGE ---
            # bar_w, bar_h = 130, 18
            
            # # 1. I-define muna ang Gas positions (DAPAT NASA ITAAS ITO)
            # gas_x, gas_y = 25, height - 35
            # bar_w, bar_h = 130, 18

            # --- UI MEASUREMENTS ---
            gas_x, gas_y = 25, height - 35
            bar_w, bar_h = 130, 18

            # --- ENGINE INDICATOR ---
            eng_col = (0, 255, 0) if engine_on else (255, 0, 0)
            if is_starting: eng_col = (255, 255, 0)
            eng_txt = "ENGINE: ON" if engine_on else "ENGINE: OFF"
            if is_starting: eng_txt = "STARTING..."
            
            eng_surf = small_font.render(eng_txt, True, eng_col)
            screen.blit(eng_surf, (gas_x, gas_y - 35)) 

            # --- FUEL BAR DRAWING ---
            pygame.draw.rect(screen, (30, 30, 30), (gas_x, gas_y, bar_w, bar_h))
            fill_g = int((current_gas / max_gas) * (bar_w - 4))
            pygame.draw.rect(screen, (0, 255, 0) if current_gas > 25 else (255, 0, 0), (gas_x + 2, gas_y + 2, max(0, fill_g), bar_h - 4))
            
            gas_txt = small_font.render(f"FUEL: {int(current_gas)}%", True, (255, 255, 255))
            screen.blit(gas_txt, (gas_x, gas_y - 18))
            
            # 2. Ngayon, pwede mo na gamitin sa Engine Indicator
            # --- ENGINE INDICATOR ---
            eng_col = (0, 255, 0) if engine_on else (255, 0, 0)
            if is_starting: eng_col = (255, 255, 0)
            eng_txt = "ENGINE: ON" if engine_on else "ENGINE: OFF"
            if is_starting: eng_txt = "STARTING..."
            
            eng_surf = small_font.render(eng_txt, True, eng_col)
            screen.blit(eng_surf, (gas_x, gas_y - 35)) 

            # 3. Drawing ng Fuel Bar (Existing code mo)
            pygame.draw.rect(screen, (30, 30, 30), (gas_x, gas_y, bar_w, bar_h))
            fill_g = int((current_gas / max_gas) * (bar_w - 4))
            pygame.draw.rect(screen, (0, 255, 0) if current_gas > 25 else (255, 0, 0), (gas_x + 2, gas_y + 2, max(0, fill_g), bar_h - 4))
            
            gas_txt = small_font.render(f"FUEL: {int(current_gas)}%", True, (255, 255, 255))
            screen.blit(gas_txt, (gas_x, gas_y - 18))

            # --- Condition Bar (Health) ---
            health_x = gas_x + bar_w + 20
            pygame.draw.rect(screen, (30, 30, 30), (health_x, gas_y, bar_w, bar_h))
            
            fill_h = int((max(0, current_health) / max_health) * (bar_w - 4))
            h_col = (0, 255, 0) if current_health > 60 else (255, 255, 0) if current_health > 30 else (255, 0, 0)
            
            if current_health <= 0: # DAGDAG ITO
                current_health = 0
                if not show_lose_panel:
                    show_lose_panel = True
                    # 1. Patayin ang lahat ng ingay ng makina at radyo
                    engine_idle_sound.stop()
                    reverse_sound.stop()
                    powerup_sound.stop()
                    speedup_sound.stop()
                    start_jeep_radio(0) # I-off ang radyo ng jeep
                    
                    idle_playing = False
                    reverse_playing = False
                    
                    # 2. Patugtugin ang music ng pagkatalo
                    if not lose_music_playing:
                        lose_sound.play(-1) # -1 para tuloy-tuloy ang music habang nka-panel
                        lose_music_playing = True
            
            if current_health > 0:
                pygame.draw.rect(screen, h_col, (health_x + 2, gas_y + 2, fill_h, bar_h - 4))
            
            # ======================================================
            # W A R N I N G   S I G N S   (LOW FUEL & CRITICAL CONDITION)
            # ======================================================
            warn_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 15)
            warn_y = height - 70 # Pwesto sa taas ng bars
            
            # LOW FUEL WARNING
            if current_gas <= 25:
                # Mag-blink base sa oras (500ms intervals)
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    fuel_warn = warn_font.render("⚠ LOW FUEL!", True, (255, 0, 0))
                    screen.blit(fuel_warn, (25, warn_y - 20))
            
            # CRITICAL CONDITION WARNING
            if current_health <= 25:
                # Mag-blink din base sa oras
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    health_warn = warn_font.render("LOW HEALTH!", True, (255, 165, 0))
                    # Itatabi natin sa kabila para hindi magpatong
                    screen.blit(health_warn, (health_x, warn_y))
            
            # Balik natin ang Health Percentage text
            health_txt = small_font.render(f"HEALTH: {int(max(0, current_health))}%", True, (255, 255, 255))
            screen.blit(health_txt, (health_x, gas_y - 18))
            
            if not is_jeep_moving and jeep_passengers_count > 0:
                hint_txt_str = "[F] para pababain"
                hint_x = pfp_display_x
                hint_y = pass_panel_y_pos + passenger_panel.get_height() + 10
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    border_surf = medium_font.render(hint_txt_str, True, (0, 0, 0))
                    screen.blit(border_surf, (hint_x + dx, hint_y + dy))
                main_hint_surf = medium_font.render(hint_txt_str, True, (255, 255, 255))
                screen.blit(main_hint_surf, (hint_x, hint_y))

            # PARA! INDICATOR
            if anyone_wants_to_stop:
                # --- DITO MO I-PASTE ITO ---
                if not para_sound_played:
                    knocking_sound.play()
                    para_sound_played = True
                # ---------------------------
                
            # --- AUTO SMOKE & FIRE LOGIC (UPDATED) ---
            if current_health < 50: 
                if random.randint(0, 10) == 0:
                    # Normal na usok (Gray) - False ang is_fire
                    smoke_particles.append([[jeep_x, jeep_y], random.randint(3, 6), 150, False])
            
            if current_health < 25: 
                if random.randint(0, 5) == 0:
                    # Random position sa paligid ng jeep
                    fire_x = jeep_x + random.randint(-12, 12)
                    fire_y = jeep_y + random.randint(-12, 12)
                    
                    # Random "Fire" colors: Red, Orange, Yellow
                    fire_color = random.choice([(255, 30, 0), (255, 120, 0), (255, 200, 0)])
                    
                    # FORMAT: [[x, y], radius, alpha, is_fire, color]
                    smoke_particles.append([[fire_x, fire_y], random.randint(3, 8), 255, True, fire_color])
                    
            # --- PARA! INDICATOR (DAPAT NAKALABAS ITO SA HEALTH LOGIC) ---
            if anyone_wants_to_stop:
                if not para_sound_played:
                    knocking_sound.play()
                    para_sound_played = True

                para_w, para_h = 120, 35
                para_x = (width // 2) - (para_w // 2)
                para_y = 110 
                
                pygame.draw.rect(screen, (200, 0, 0), (para_x, para_y, para_w, para_h), border_radius=8)
                para_txt = custom_font.render("PARA!", True, (255, 255, 255))
                
                para_txt_x = para_x + (para_w // 2) - (para_txt.get_width() // 2)
                para_txt_y = para_y + (para_h // 2) - (para_txt.get_height() // 2)
                screen.blit(para_txt, (para_txt_x, para_txt_y))
            else:
                para_sound_played = False
        # ======================================================
            # UI: QUOTA (TOP RIGHT - ABOVE RADIO)
            # ======================================================
            q_x, q_y = width - 180, 15
            pygame.draw.rect(screen, (0, 0, 0, 150), (q_x, q_y, 160, 55), border_radius=5)
            pygame.draw.rect(screen, (255, 255, 255), (q_x, q_y, 160, 55), 2, border_radius=5)
            
            q_prog = min(1.0, total_earnings / daily_quota)
            pygame.draw.rect(screen, (0, 150, 0), (q_x + 10, q_y + 30, 140, 15)) # Background bar
            pygame.draw.rect(screen, (0, 255, 0), (q_x + 10, q_y + 30, 140 * q_prog, 15)) # Progress
            
            q_text = quota_font.render(f"QUOTA: {total_earnings}/{daily_quota}", True, (255, 255, 255))
            screen.blit(q_text, (q_x + 12, q_y + 12))

            # ======================================================
            # UI: DASHBOARD (BOTTOM RIGHT)
            # ======================================================
            d_w, d_h = 175, 110
            d_x, d_y = width - d_w - 15, height - d_h - 15
            
            dash_surf = pygame.Surface((d_w, d_h), pygame.SRCALPHA)
            dash_surf.fill((0, 0, 0, 180))
            screen.blit(dash_surf, (d_x, d_y))
            pygame.draw.rect(screen, (255, 215, 0), (d_x, d_y, d_w, d_h), 2, border_radius=10)
            
            screen.blit(medium_font.render("DASHBOARD", True, (255, 215, 0)), (d_x + 18, d_y + 5))
            
            y_gap = 28
            for p_type, count in stats.items():
                f_val = 11 if p_type != "Regular" else 13
                s_txt = dash_info_font.render(f"{p_type}(P{f_val}): {count}", True, (240, 240, 240))
                screen.blit(s_txt, (d_x + 10, d_y + y_gap))
                y_gap += 18

            # ======================================================
            # FLOATING PAYMENT NOTIFS (ANIMATION)
            # ======================================================
            for n in payment_notifs[:]:
                n[0][1] -= 1 # Taas effect
                n[2] -= 5    # Fade effect
                if n[2] <= 0: payment_notifs.remove(n)
                else:
                    pay_surf = medium_font.render(n[1], True, (255, 255, 0))
                    pay_surf.set_alpha(n[2])
                    screen.blit(pay_surf, (n[0][0], n[0][1]))
        
        # --- RUSH HOUR MESSAGE DISPLAY ---
            curr_t = pygame.time.get_ticks()
            if rush_status != "NORMAL" and (curr_t - rush_notif_timer < rush_notif_duration):
                if rush_status == "WARNING":
                    b_col = (255, 165, 0, 180) # Orange Bar
                    txt1 = "COMING SOON: RUSH HOUR!"
                    txt2 = "MALAPIT NA ANG DAGSA NG TAO, MAG-READY NA!"
                else: # ACTIVE
                    b_col = (200, 0, 0, 200)   # Red Bar
                    txt1 = "RUSH HOUR ACTIVE!"
                    txt2 = "DAGSA ANG PASAHERO! BILISAN ANG PASADA!"

                r_overlay = pygame.Surface((width, 80), pygame.SRCALPHA)
                r_overlay.fill(b_col)
                screen.blit(r_overlay, (0, height // 2 - 40))

                m_s = custom_font.render(txt1, True, (255, 255, 255))
                s_s = small_font.render(txt2, True, (255, 255, 0))
                screen.blit(m_s, (width//2 - m_s.get_width()//2, height//2 - 25))
                screen.blit(s_s, (width//2 - s_s.get_width()//2, height//2 + 5))
            
        if show_saved_panel:
            if fade_state == "in":
                saved_alpha += fade_speed
                if saved_alpha >= 255:
                    saved_alpha = 255
                    fade_state = "stay"
                    saved_panel_time = pygame.time.get_ticks()
            elif fade_state == "stay":
                if pygame.time.get_ticks() - saved_panel_time > saved_duration: fade_state = "out"
            elif fade_state == "out":
                saved_alpha -= fade_speed
                if saved_alpha <= 0:
                    saved_alpha = 0
                    show_saved_panel = False
            saved_panel.set_alpha(saved_alpha)
            saved_rect = saved_panel.get_rect(topleft=((width - saved_panel.get_width()) // 2, 450))
            screen.blit(saved_panel, saved_rect)
        
        # ======================================================
        # W I N / S U M M A R Y   P A N E L   (8:30 PM)
        # ======================================================
        if show_win_panel:
            # 1. UPDATE ANIMATION COUNTER (Dito sa loob)
            win_anim_counter += 0.25 

            # 2. BACKGROUND & OVERLAY
            ret, frame = blurdbg_vid.read()
            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))
            bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            
            # Screen Dance
            sway_x = math.sin(win_anim_counter * 0.8) * 12
            sway_y = math.cos(win_anim_counter * 0.8) * 8
            screen.blit(bg_surface, (sway_x, sway_y))
            
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            screen.blit(overlay, (0, 0))

            # 3. PANEL BOUNCE LOGIC
            bounce_y = int(abs(math.sin(win_anim_counter)) * -15) 
            
            # GAMITIN ANG ORIGINAL PANEL (Huwag i-scale para HD ang text)
            panel_rect = win_panel.get_rect(center=(width // 2, (height // 2) + bounce_y))
            screen.blit(win_panel, panel_rect)

            # 4. TEXT DISPLAY (IBINALIK SA DATI MONG COORDINATES)
            gas_used = max_gas - current_gas
            gas_expense = int(gas_used * gas_price_per_unit)
            take_home = total_earnings - daily_quota - gas_expense
            
            px, py = panel_rect.x, panel_rect.y
            text_col = (0, 0, 0)

            # Eto na yung original positions mo, Joshua:
            screen.blit(medium_font.render(f" {total_earnings}", True, text_col), (px + 300, py + 70))
            screen.blit(medium_font.render(f" {daily_quota}", True, text_col), (px + 300, py + 117))
            screen.blit(medium_font.render(f" {gas_expense}", True, text_col), (px + 320, py + 140))
            
            subtotal = total_earnings - daily_quota - gas_expense
            screen.blit(medium_font.render(f" {subtotal}", True, text_col), (px + 300, py + 168))
            
            final_col = (20, 120, 20) if take_home > 0 else (180, 0, 0)
            screen.blit(medium_font.render(f" {take_home}", True, final_col), (px + 310, py + 214))

            # 5. HINT TEXT
            hint_f = pygame.font.SysFont("arial", 18, bold=True)
            hint_s = hint_f.render("Press anywhere to back to main menu", True, (255, 255, 255))
            screen.blit(hint_s, ((width - hint_s.get_width()) // 2, height - 40))

            # 6. BEAT FLASH
            if abs(math.sin(win_anim_counter)) > 0.9:
                flash = pygame.Surface((width, height))
                flash.set_alpha(40)
                flash.fill((255, 255, 255))
                screen.blit(flash, (0,0))
            
            # ======================================================
        # L O S E / G L I T C H   S Y S T E M
        # ======================================================
        if show_lose_panel:
            # 1. GENERATE SHAKE OFFSET
            # Ito ang magpapakalog sa screen
            shake_offset_x = random.randint(-10, 10)
            shake_offset_y = random.randint(-10, 10)

            # 2. Background Blur (Dating logic mo)
            ret, frame = blurdbg_vid.read()
            if not ret:
                blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = blurdbg_vid.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))
            bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # 3. DRAW BACKGROUND WITH SHAKE
            # Imbes na (0,0), gagamitin natin ang shake offset
            screen.blit(bg_surface, (shake_offset_x, shake_offset_y))

            # 4. GLITCH EFFECT (RGB SPLIT)
            # Minsan (randomly), mag-do-draw tayo ng "ghost" image na kulay Pula o Cyan
            if random.randint(0, 5) == 0:
                glitch_surf = bg_surface.copy()
                # Gawing mapula ang ghost image
                glitch_surf.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                glitch_surf.set_alpha(120)
                # I-offset ng kaunti para sa "ghosting" look
                screen.blit(glitch_surf, (shake_offset_x + 15, shake_offset_y))

            # 5. DARK OVERLAY
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((20, 0, 0, 180)) # Nilagyan natin ng kaunting pula (20) ang dilim
            screen.blit(overlay, (0, 0))
            
            # 6. DRAW LOSE PANEL WITH SHAKE
            l_rect = lose_panel.get_rect(center=(width // 2 + shake_offset_x, height // 2 + shake_offset_y))
            screen.blit(lose_panel, l_rect)

            # 7. ADD STATIC NOISE (Optional: para sa "TV glitch" feel)
            if random.randint(0, 3) == 0:
                for _ in range(20):
                    noise_y = random.randint(0, height)
                    pygame.draw.line(screen, (200, 200, 200), (0, noise_y), (width, noise_y), 1)

            # 8. Hint Text (Press anywhere to back)
            hint_f = pygame.font.SysFont("arial", 18, bold=True)
            hint_s = hint_f.render("Press anywhere to back to main menu", True, (255, 100, 100))
            screen.blit(hint_s, ((width - hint_s.get_width()) // 2 + shake_offset_x, height - 40))
            
        pygame.display.update()
        clock.tick(60)

# ======================================================
# C L E A N  U P
# ======================================================
video.release()
blurdbg_vid.release()
pygame.quit()
sys.exit()
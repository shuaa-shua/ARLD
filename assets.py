# =========================================================
# A S S E T S   L O A D E R
# =========================================================
from imports import *
from settings import *

# =========================================================
# I N I T I A L I Z A T I O N
# =========================================================
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("All Roads Lead to Dagupan (ARLD)")
clock = pygame.time.Clock()

# =========================================================
# F O N T S
# =========================================================
custom_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 20)
small_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 12)
medium_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 16)
dash_info_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 10)
quota_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 10)

# =========================================================
# S O U N D S  &  M U S I C
# =========================================================
# --- Engine & Cars ---
engine_start_sound = pygame.mixer.Sound("music/car starting.mp3") 
engine_idle_sound = pygame.mixer.Sound("music/car sound.mp3")   
engine_start_sound.set_volume(0.6)
engine_idle_sound.set_volume(0.4)

reverse_sound = pygame.mixer.Sound("music/reverse.mp3") 
reverse_sound.set_volume(0.3) 

jeep_horn_sound = pygame.mixer.Sound("music/horn.mp3")
jeep_horn_sound.set_volume(5.0)

# --- Gameplay Effects ---
accident_sound = pygame.mixer.Sound("music/Accident sound.mp3")
accident_sound.set_volume(0.6)
powerup_sound = pygame.mixer.Sound("music/powerup.mp3")
powerup_sound.set_volume(1.0)
speedup_sound = pygame.mixer.Sound("music/speedup.mp3")
speedup_sound.set_volume(0.8)

# --- Passengers & UI ---
knocking_sound = pygame.mixer.Sound("music/knocking.mp3")
knocking_sound.set_volume(1.0)
money_sound = pygame.mixer.Sound("music/Money.mp3")
money_sound.set_volume(0.8)
button_sound = pygame.mixer.Sound("music/button sound.wav")
button_sound.set_volume(0.5)
click_sound = pygame.mixer.Sound("music/click.wav")
click_sound.set_volume(1.0)

# --- Win / Lose Music ---
win_music = pygame.mixer.Sound("music/win music.mp3") 
win_music.set_volume(0.6)
lose_sound = pygame.mixer.Sound("music/lose sound.wav")
lose_sound.set_volume(1.0)

win_video_audio = pygame.mixer.Sound("music/win_video.mp3") 
win_video_audio.set_volume(1.0)

# --- Jeep Radio Tracks ---
jeep_sound1 = pygame.mixer.Sound("music/bagyo.mp3")
jeep_sound1.set_volume(0.5)
jeep_sound2 = pygame.mixer.Sound("music/Binibirocha.mp3")
jeep_sound2.set_volume(0.5)
jeep_sound3 = pygame.mixer.Sound("music/Hawak Mo Ang Beat Remix.mp3")
jeep_sound3.set_volume(0.5)
jeep_sound4 = pygame.mixer.Sound("music/Kahit Maputi Na Ang Buhok ko.mp3")
jeep_sound4.set_volume(0.5)
jeep_sound5 = pygame.mixer.Sound("music/Malunggay Pandesal.mp3")
jeep_sound5.set_volume(0.5)
jeep_sound6 = pygame.mixer.Sound("music/Manok Na Pula.mp3")
jeep_sound6.set_volume(0.5)
jeep_sound7 = pygame.mixer.Sound("music/Modelong Charing.mp3")
jeep_sound7.set_volume(0.5)
jeep_sound8 = pygame.mixer.Sound("music/Totoy Bibbo.mp3")
jeep_sound8.set_volume(0.5)
jeep_sound9 = pygame.mixer.Sound("music/Touch By Touch.mp3")
jeep_sound9.set_volume(0.5)
jeep_sound10 = pygame.mixer.Sound("music/papadudut.mp3")
jeep_sound10.set_volume(0.6)

# =======================================================
# M U S I C   P L A Y L I S T
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

pygame.mixer.music.load("music/main bg music beep.mp3")
pygame.mixer.music.set_volume(0.4)

# ======================================================
# V I D E O  B A C K G R O U N D S
# ======================================================
video = cv2.VideoCapture("backgrounds/moving bg.mp4")
blurdbg_vid = cv2.VideoCapture("backgrounds/blurd vid bg.mp4")
win_cutscene_vid = cv2.VideoCapture("backgrounds/win_video.mp4")
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

# ======================================================
# G A M E  B A C K G R O U N D S
# ======================================================
route_caldag_img = pygame.image.load("route/caldag.png").convert()
route_caldag_img = pygame.transform.scale(route_caldag_img, (width, height))

# ======================================================
# J E E P  I M A G E
# ======================================================
jeep_img_original = pygame.image.load("Jeep/caldag_jeep.png").convert_alpha() 
jeep_img_original = pygame.transform.scale(jeep_img_original, (40, 71)) 

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
passenger_panel = pygame.image.load("panel/passenger_total.png").convert_alpha()
passenger_panel = pygame.transform.scale(passenger_panel, (150, 50))

# P A N E L  P O S I T I O N S
panel_x = (width - 430) // 2
panel_y = (height - 230) // 2
pfp_display_x = 15 #left right
pfp_display_y = 15 # up down

# ======================================================
# P A S S E N G E R S
# ======================================================
passenger1 = pygame.image.load("passenger/person1.png").convert_alpha()
passenger1 = pygame.transform.scale(passenger1, (200, 60))
passenger2 = pygame.image.load("passenger/person2.png").convert_alpha()
passenger2 = pygame.transform.scale(passenger2, (200, 60))
passenger3 = pygame.image.load("passenger/person3.png").convert_alpha()
passenger3 = pygame.transform.scale(passenger3, (200, 60))
passenger4 = pygame.image.load("passenger/person4.png").convert_alpha()
passenger4 = pygame.transform.scale(passenger4, (200, 60))
passenger5 = pygame.image.load("passenger/person5.png").convert_alpha()
passenger5 = pygame.transform.scale(passenger5, (200, 60))
passenger6 = pygame.image.load("passenger/person6.png").convert_alpha()
passenger6 = pygame.transform.scale(passenger6, (200, 60))
passenger7 = pygame.image.load("passenger/person7.png").convert_alpha()
passenger7 = pygame.transform.scale(passenger7, (200, 60))

# 1. Re-scale existing loaded images to be small (25x25 pixels)
passenger_imgs = [passenger1, passenger2, passenger3, passenger4, passenger5, passenger6, passenger7]
passenger_imgs = [pygame.transform.scale(img, (25, 25)) for img in passenger_imgs]

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

# T E X T  B O X
input_rect = pygame.Rect(panel_x + 49, panel_y + 90, 310, 35)
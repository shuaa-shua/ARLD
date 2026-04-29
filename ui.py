# =========================================================
# U I   S T A T E S   &   V A R I A B L E S
# =========================================================
from imports import *
from settings import *

# ======================================================
# T E X T   I N P U T   ( U S E R N A M E )
# ======================================================
user_text = ""
input_active = False 
cursor_visible = False
last_cursor_blink = 0

# ======================================================
# H O V E R   S T A T E S
# ======================================================
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

# ======================================================
# P A N E L   S T A T E S
# ======================================================
show_saved_panel = False
saved_alpha = 0          
fade_state = "in"        
saved_panel_time = 0

show_win_panel = False        
show_lose_panel = False
win_anim_counter = 0
win_cutscene_finished = False

# --- COMING SOON NOTIFICATION ---
show_coming_soon = False
coming_soon_timer = 0
cs_alpha = 0
cs_y_offset = 0

# ======================================================
# L O A D I N G   S C R E E N
# ======================================================
loading = True
progress = 0
pause_points = [20, 40, 60, 80]
pause_index = 0

# ======================================================
# S T A T S   &   E A R N I N G S
# ======================================================
total_earnings = 0
stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
payment_notifs = [] # Para sa floating "+11" or "+13"

# ======================================================
# T I M E   &   R U S H   H O U R   S T A T E
# ======================================================
game_hour = 5
game_minute = 30
time_counter = 0

rush_status = "NORMAL"
rush_notif_timer = 0

# ======================================================
# N I G H T   M O D E   S T A T E
# ======================================================
night_alpha = 0  # 0 = Umaga (Maliwanag), 255 = Sobrang dilim
# =========================================================
# A U D I O   M A N A G E R
# =========================================================
from imports import *
from assets import playlist

# =======================================================
# A U D I O   S T A T E   F L A G S
# =======================================================
win_music_playing = False     
lose_music_playing = False
idle_playing = False
reverse_playing = False      
charge_playing = False
boost_sound_playing = False
para_sound_played = False
horn_playing = False
music_started = False

current_music_index = 0

# =======================================================
# M U S I C   P L A Y E R   L O G I C
# =======================================================
def start_jeep_radio(index):
    global current_music_index
    current_music_index = index
    
    pygame.mixer.music.stop()
    
    for item in playlist:
        if item["sound"] is not None:
            item["sound"].stop()
            
    selected_item = playlist[index]
    
    if selected_item["sound"] is not None:
        selected_item["sound"].play(-1)
    else:
        print("Radio turned OFF")
# =========================================================
# A U D I O   M A N A G E R
# =========================================================
from imports import *
from assets import playlist

# =======================================================
# A U D I O   S T A T E   F L A G S
# =======================================================
win_music_playing = False     # Flag para hindi mag-loop ang pag-play
lose_music_playing = False
idle_playing = False
reverse_playing = False       # Flag para hindi mag-overlap ang tunog ng pag-atras
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
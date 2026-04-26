# =========================================================
# R O U T E   S E L E C T I O N   S T A T E
# =========================================================
from imports import *
from settings import width, height, coming_soon_duration
import assets
import ui
import audio_manager

# =========================================================
# E V E N T   H A N D L I N G
# =========================================================
def handle_route_events(event, current_state):
    """
    Sinasalo nito yung click sa mga ruta at back button.
    """
    new_state = current_state
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        # --- BACK MENU CLICK ---
        if assets.backmenu_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "menu" 
            print("Back to Menu")
            
        # --- CAL DAG CLICK ---
        elif assets.caldag_rect.collidepoint(event.pos):
            assets.button_sound.play()
            print("Starting Route: CALASIAO - DAGUPAN")
            new_state = "caldag_screen"
            # Simulan agad ang radyo pagpasok
            audio_manager.start_jeep_radio(audio_manager.current_music_index) 
            
        # --- SAN DAG CLICK ---
        elif assets.sandag_rect.collidepoint(event.pos):
            assets.button_sound.play()
            ui.show_coming_soon = True
            ui.coming_soon_timer = pygame.time.get_ticks()
            print("Starting Route: SAN CARLOS - DAGUPAN")
            
        # --- LIN DAG CLICK ---
        elif assets.lindag_rect.collidepoint(event.pos):
            assets.button_sound.play()
            ui.show_coming_soon = True
            ui.coming_soon_timer = pygame.time.get_ticks() 
            print("Starting Route: LINGAYEN - DAGUPAN")
            
    return new_state

# =========================================================
# D R A W I N G   L O G I C
# =========================================================
def draw_route(screen):
    # 1. B L U R R E D   V I D E O   B A C K G R O U N D
    ret, frame = assets.blurdbg_vid.read()
    if not ret:
        assets.blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = assets.blurdbg_vid.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width, height))
        bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(bg_surface, (0, 0))
        
    # 2. O V E R L A Y
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 70))
    screen.blit(overlay, (0, 0))
    screen.blit(assets.route_panel, (assets.panel_x, assets.panel_y - 48))
    
    mouse_pos = pygame.mouse.get_pos()
    
    # ======================================================
    # D R A W   B U T T O N S   W I T H   H O V E R   L O G I C
    # ======================================================
    
    # CAL DAG
    if assets.caldag_rect.collidepoint(mouse_pos):
        if not ui.hovered_caldag:
            assets.button_sound.play()
            ui.hovered_caldag = True
        screen.blit(assets.button_caldag_hover, assets.caldag_rect)
    else:
        screen.blit(assets.button_caldag, assets.caldag_rect)
        ui.hovered_caldag = False
        
    # SAN DAG
    if assets.sandag_rect.collidepoint(mouse_pos):
        if not ui.hovered_sandag:
            assets.button_sound.play()
            ui.hovered_sandag = True
        screen.blit(assets.button_sandag_hover, assets.sandag_rect)
    else:
        screen.blit(assets.button_sandag, assets.sandag_rect)
        ui.hovered_sandag = False
        
    # LIN DAG
    if assets.lindag_rect.collidepoint(mouse_pos):
        if not ui.hovered_lindag:
            assets.button_sound.play()
            ui.hovered_lindag = True
        screen.blit(assets.button_lindag_hover, assets.lindag_rect)
    else:
        screen.blit(assets.button_lindag, assets.lindag_rect)
        ui.hovered_lindag = False
        
    # BACK MENU
    if assets.backmenu_rect.collidepoint(mouse_pos):
        if not ui.hovered_backmenu:
            assets.button_sound.play()
            ui.hovered_backmenu = True
        screen.blit(assets.button_backmenu_hover, assets.backmenu_rect)
    else:
        screen.blit(assets.button_back_menu, assets.backmenu_rect)
        ui.hovered_backmenu = False
        
    # ======================================================
    # C O M I N G   S O O N   N O T I F I C A T I O N
    # ======================================================
    if ui.show_coming_soon:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - ui.coming_soon_timer
        
        # 1. FADE LOGIC (Alpha: 0 to 255 then back to 0)
        if elapsed < 500: # Fade In
            ui.cs_alpha = int((elapsed / 500) * 255)
        elif elapsed > (coming_soon_duration - 500): # Fade Out
            remaining = coming_soon_duration - elapsed
            ui.cs_alpha = int((remaining / 500) * 255)
        else:
            ui.cs_alpha = 255
            
        # 2. FLOAT LOGIC (Aangat ang text habang tumatagal)
        ui.cs_y_offset = int((elapsed / coming_soon_duration) * -40)
        
        if elapsed < coming_soon_duration:
            cs_text = assets.custom_font.render("NO EVENTS, COMING SOON!", True, (255, 215, 0)) 
            cs_text.set_alpha(ui.cs_alpha)
            
            text_x = (width // 2) - (cs_text.get_width() // 2)
            text_y = 550 + ui.cs_y_offset 
            
            # Draw a simple shadow behind the text (Optional, para mas mabasa)
            shadow_surf = assets.custom_font.render("NO EVENTS, COMING SOON!", True, (0, 0, 0))
            shadow_surf.set_alpha(int(ui.cs_alpha * 0.5)) 
            screen.blit(shadow_surf, (text_x + 2, text_y + 2)) 
            
            # Draw the main fading/floating text
            screen.blit(cs_text, (text_x, text_y))
        else:
            ui.show_coming_soon = False
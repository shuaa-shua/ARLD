# =========================================================
# U S E R N A M E   S T A T E
# =========================================================
from imports import *
from settings import width, height, backspace_delay, backspace_speed
import assets
import ui

# =========================================================
# L O C A L   V A R I A B L E S   (Keyboard Hold)
# =========================================================
backspace_held = False
last_backspace_time = 0
space_held = False
last_space_time = 0

# =========================================================
# E V E N T   H A N D L I N G
# =========================================================
def handle_username_events(event, current_state):
    global backspace_held, last_backspace_time, space_held, last_space_time
    new_state = current_state
    
    # M O U S E   C L I C K S
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if assets.input_rect.collidepoint(event.pos):
            ui.input_active = True
            ui.cursor_visible = True
            ui.last_cursor_blink = pygame.time.get_ticks()
        else:
            ui.input_active = False
            ui.cursor_visible = False
            
        if assets.confirm_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "route"
            ui.show_saved_panel = True
            ui.saved_alpha = 0
            ui.fade_state = "in"
            print("USERNAME:", ui.user_text)
        elif assets.cancel_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "menu"
            ui.user_text = ""
            ui.input_active = False

    # K E Y B O A R D   P R E S S
    if event.type == pygame.KEYDOWN and ui.input_active:
        if event.key == pygame.K_BACKSPACE:
            ui.user_text = ui.user_text[:-1]
            backspace_held = True
            last_backspace_time = pygame.time.get_ticks()
        elif event.key == pygame.K_SPACE:
            if len(ui.user_text) < 6:
                ui.user_text += " "
                space_held = True
                last_space_time = pygame.time.get_ticks()
        elif event.key == pygame.K_RETURN:
            ui.input_active = False
        else:
            if len(ui.user_text) < 6:
                ui.user_text += event.unicode
                
    # K E Y B O A R D   R E L E A S E
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_BACKSPACE:
            backspace_held = False
        if event.key == pygame.K_SPACE:
            space_held = False
            
    return new_state

# =========================================================
# U P D A T E   L O G I C   ( H o l d i n g   K e y s )
# =========================================================
def update_username_state():
    global backspace_held, last_backspace_time, space_held, last_space_time
    
    # B A C K S P A C E   R E P E A T   L O G I C
    if backspace_held and ui.input_active:
        now = pygame.time.get_ticks()
        if now - last_backspace_time > backspace_delay:
            ui.user_text = ui.user_text[:-1]
            last_backspace_time = now - (backspace_delay - backspace_speed)
            
    # S P A C E   R E P E A T   L O G I C
    if space_held and ui.input_active:
        now = pygame.time.get_ticks()
        if now - last_space_time > backspace_delay:
            if len(ui.user_text) < 16:
                ui.user_text += " "
                last_space_time = now - (backspace_delay - backspace_speed)

# =========================================================
# D R A W I N G   L O G I C
# =========================================================
def draw_username(screen):
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
        
    # 2. O V E R L A Y   &   P A N E L
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 70))
    screen.blit(overlay, (0, 0))
    screen.blit(assets.username_panel, (assets.panel_x, assets.panel_y))
    
    # 3. R E N D E R   T E X T
    text_surf = assets.custom_font.render(ui.user_text, True, (0, 0, 0))
    screen.blit(text_surf, (assets.input_rect.x + 10, assets.input_rect.y + 5))
    
    # 4. B L I N K I N G   C U R S O R
    if ui.input_active:
        curr_time = pygame.time.get_ticks()
        if curr_time - ui.last_cursor_blink > 500:
            ui.cursor_visible = not ui.cursor_visible
            ui.last_cursor_blink = curr_time
        
        if ui.cursor_visible:
            cursor_x = assets.input_rect.x + 10 + text_surf.get_width() + 2
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, assets.input_rect.y + 2), (cursor_x, assets.input_rect.y + 25), 2)
            
    mouse_pos = pygame.mouse.get_pos()
    
    # 5. C O N F I R M   H O V E R + S O U N D
    if assets.confirm_rect.collidepoint(mouse_pos):
        if not ui.hovered_confirm:
            assets.button_sound.play()
            ui.hovered_confirm = True
        screen.blit(assets.button_confirm_hover, assets.confirm_rect)
    else:
        screen.blit(assets.button_confirm, assets.confirm_rect)
        ui.hovered_confirm = False
        
    # 6. C A N C E L   H O V E R + S O U N D
    if assets.cancel_rect.collidepoint(mouse_pos):
        if not ui.hovered_cancel:
            assets.button_sound.play()
            ui.hovered_cancel = True
        screen.blit(assets.button_cancel_hover, (assets.cancel_rect.x + 5, assets.cancel_rect.y))
    else:
        screen.blit(assets.button_cancel, assets.cancel_rect)
        ui.hovered_cancel = False
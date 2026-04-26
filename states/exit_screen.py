# =========================================================
# E X I T   S C R E E N   S T A T E
# =========================================================
from imports import *
from settings import width, height
import assets
import ui

# =========================================================
# E V E N T   H A N D L I N G
# =========================================================
def handle_exit_events(event, current_state, running):
    """
    Sinasalo nito yung click sa confirm exit or cancel.
    Nagbabalik ng (new_state, running)
    """
    new_state = current_state
    is_running = running
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if assets.cancel_green_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "menu"
            
        elif assets.exit_confirm_rect.collidepoint(event.pos):
            assets.button_sound.play()
            is_running = False  # Patayin ang buong main loop
            
    return new_state, is_running

# =========================================================
# D R A W I N G   L O G I C
# =========================================================
def draw_exit(screen):
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
    
    # 3. E X I T   P A N E L
    screen.blit(assets.exit_panel, (assets.panel_x, assets.panel_y))
    mouse_pos = pygame.mouse.get_pos()
    
    # ======================================================
    # H O V E R + S O U N D   L O G I C
    # ======================================================
    
    # E X I T   H O V E R + S O U N D
    if assets.exit_confirm_rect.collidepoint(mouse_pos):
        if not ui.hovered_exit_confirm:
            assets.button_sound.play()
            ui.hovered_exit_confirm = True
            
        # S H A K E  O F  E X I T
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)
        
        screen.blit(assets.button_confirm_exit_hover, (assets.exit_confirm_rect.x + shake_x, assets.exit_confirm_rect.y + shake_y))
    else:
        screen.blit(assets.button_confirm_exit, assets.exit_confirm_rect)
        ui.hovered_exit_confirm = False
        
    # C A N C E L   H O V E R + S O U N D
    if assets.cancel_green_rect.collidepoint(mouse_pos):
        if not ui.hovered_cancel_green:
            assets.button_sound.play()
            ui.hovered_cancel_green = True
        screen.blit(assets.button_cancel_green_hover, (assets.cancel_green_rect.x + 5, assets.cancel_green_rect.y))
    else:
        screen.blit(assets.button_cancel_green, assets.cancel_green_rect)
        ui.hovered_cancel_green = False
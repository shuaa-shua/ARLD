# =========================================================
# M A I N   M E N U   S T A T E
# =========================================================
from imports import *
from settings import width, height
import assets
import ui

# =========================================================
# E V E N T   H A N D L I N G
# =========================================================
def handle_menu_events(event, current_state):
    """
    Sinasalo nito yung mga clicks sa Main Menu.
    Nagbabalik ng bagong state (hal. 'username', 'about', 'exit')
    """
    new_state = current_state
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if assets.start_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "username"
        elif assets.about_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "about"
        elif assets.exit_rect.collidepoint(event.pos):
            assets.button_sound.play()
            new_state = "exit"
            
    return new_state

# =========================================================
# D R A W I N G   L O G I C
# =========================================================
def draw_menu(screen):
    """
    Dito ang drawing ng video background at hover effects ng buttons.
    """
    # 1. B A C K G R O U N D   V I D E O
    ret, frame = assets.video.read()
    if not ret:
        assets.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = assets.video.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width, height))
        bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(bg_surface, (0, 0))
        
    mouse_pos = pygame.mouse.get_pos()
    
    # ===========================================
    # H O V E R + S O U N D
    # ===========================================
    
    # S T A R T
    if assets.start_rect.collidepoint(mouse_pos):
        if not ui.hovered_start:
            assets.button_sound.play()
            ui.hovered_start = True
        screen.blit(assets.button_start_hover, assets.start_rect)
    else:
        screen.blit(assets.button_start, assets.start_rect)
        ui.hovered_start = False
        
    # A B O U T
    if assets.about_rect.collidepoint(mouse_pos):
        if not ui.hovered_about:
            assets.button_sound.play()
            ui.hovered_about = True
        screen.blit(assets.button_about_hover, assets.about_rect)
    else:
        screen.blit(assets.button_about, assets.about_rect)
        ui.hovered_about = False
        
    # E X I T
    if assets.exit_rect.collidepoint(mouse_pos):
        if not ui.hovered_exit:
            assets.button_sound.play()
            ui.hovered_exit = True
            
        # S H A K E  O F  E X I T
        shake_x = random.randint(-2, 2)
        shake_y = random.randint(-2, 2)
        screen.blit(assets.button_exit_hover, (assets.exit_rect.x + shake_x, assets.exit_rect.y + shake_y))
    else:
        screen.blit(assets.button_exit, assets.exit_rect)
        ui.hovered_exit = False
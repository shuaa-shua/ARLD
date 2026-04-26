# =========================================================
# A B O U T   S T A T E
# =========================================================
from imports import *
from settings import width, height
import assets

# =========================================================
# E V E N T   H A N D L I N G
# =========================================================
def handle_about_events(event, current_state):
    """
    Kahit saan mag-click si player, babalik sa menu.
    -reminder ni shua
    """
    new_state = current_state
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        new_state = "menu"
    return new_state

# =========================================================
# D R A W I N G   L O G I C
# =========================================================
def draw_about(screen):
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
    overlay.fill((0, 0, 0, 80))
    screen.blit(overlay, (0, 0))
    
    # 3. A B O U T   P A N E L
    screen.blit(assets.about_panel, (assets.panel_x, assets.panel_y))
    
    # 4. H I N T   T E X T
    font = pygame.font.SysFont("arial", 18, bold=True)
    hint_text = font.render("Press anywhere to back", True, (255, 255, 255))
    hint_x = (width - hint_text.get_width()) // 2
    hint_y = height - 40
    screen.blit(hint_text, (hint_x, hint_y))
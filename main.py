# =========================================================
# M A I N   L O O P   ( ALL ROADS LEAD TO DAGUPAN )
# =========================================================
from imports import *
from settings import width, height
import assets
import ui
import audio_manager

# Import all states
import states.menu
import states.username
import states.about
import states.exit_screen
import states.route_select
import states.caldag_screen

# =======================================================
# S T A T E S   I N I T I A L I Z A T I O N
# =======================================================
state = "menu"
running = True

# ======================================================
# M A I N   L O O P
# ======================================================
while running:
    dt = assets.clock.get_time()
    
    # ======================================================
    # E V E N T   H A N D L I N G   ( Dispatcher )
    # ======================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not ui.loading:
            if state == "menu":
                state = states.menu.handle_menu_events(event, state)
            elif state == "username":
                state = states.username.handle_username_events(event, state)
            elif state == "about":
                state = states.about.handle_about_events(event, state)
            elif state == "exit":
                state, running = states.exit_screen.handle_exit_events(event, state, running)
            elif state == "route":
                state = states.route_select.handle_route_events(event, state)
            elif state == "caldag_screen":
                state = states.caldag_screen.handle_caldag_events(event, state)

    # ======================================================
    # L O A D I N G   S C R E E N
    # ======================================================
    if ui.loading:
        assets.screen.fill((0, 0, 0))
        pygame.draw.rect(assets.screen, (255, 255, 255), (5, height - 15, width - 10, 10), 1)
        fill_width = int((ui.progress / 100) * (width - 10))
        pygame.draw.rect(assets.screen, (0, 255, 0), (5, height - 15, fill_width, 10))
        
        ui.progress += 5
        if ui.pause_index < len(ui.pause_points):
            if ui.progress >= ui.pause_points[ui.pause_index]:
                ui.progress = ui.pause_points[ui.pause_index]
                time.sleep(0.7)
                ui.pause_index += 1
                
        if ui.progress >= 100:
            ui.progress = 100
            ui.loading = False
            
        pygame.display.update()
        pygame.time.delay(25)
        
    # ======================================================
    # M A I N   S C R E E N S   ( D R A W I N G )
    # ======================================================
    else:
        # Update holding logic para sa username screen
        if state == "username":
            states.username.update_username_state()

        # --- UNIVERSAL HORN PARA SA MAIN MENU ---
        keys = pygame.key.get_pressed()
        if state == "menu":
            if keys[pygame.K_SPACE]:
                if not audio_manager.horn_playing:
                    assets.jeep_horn_sound.play(-1)
                    audio_manager.horn_playing = True
            else:
                if audio_manager.horn_playing:
                    assets.jeep_horn_sound.stop()
                    audio_manager.horn_playing = False
        
        # Start main menu music if not already playing and not in gameplay
        if not audio_manager.music_started and state != "caldag_screen":
            pygame.mixer.music.play(-1, fade_ms=2000)
            audio_manager.music_started = True

        # Render current state
        if state == "menu":
            states.menu.draw_menu(assets.screen)
        elif state == "username":
            states.username.draw_username(assets.screen)
        elif state == "about":
            states.about.draw_about(assets.screen)
        elif state == "exit":
            states.exit_screen.draw_exit(assets.screen)
        elif state == "route":
            states.route_select.draw_route(assets.screen)
        elif state == "caldag_screen":
            keys = pygame.key.get_pressed()
            states.caldag_screen.run_caldag_frame(assets.screen, keys)

        # ======================================================
        # G L O B A L   S A V E D   P A N E L   O V E R L A Y
        # ======================================================
        if ui.show_saved_panel:
            if ui.fade_state == "in":
                ui.saved_alpha += ui.fade_speed
                if ui.saved_alpha >= 255:
                    ui.saved_alpha = 255
                    ui.fade_state = "stay"
                    ui.saved_panel_time = pygame.time.get_ticks()
            elif ui.fade_state == "stay":
                if pygame.time.get_ticks() - ui.saved_panel_time > ui.saved_duration: 
                    ui.fade_state = "out"
            elif ui.fade_state == "out":
                ui.saved_alpha -= ui.fade_speed
                if ui.saved_alpha <= 0:
                    ui.saved_alpha = 0
                    ui.show_saved_panel = False
                    
            assets.saved_panel.set_alpha(ui.saved_alpha)
            saved_rect = assets.saved_panel.get_rect(topleft=((width - assets.saved_panel.get_width()) // 2, 450))
            assets.screen.blit(assets.saved_panel, saved_rect)

        pygame.display.update()
        assets.clock.tick(60)

# ======================================================
# C L E A N  U P
# ======================================================
assets.video.release()
assets.blurdbg_vid.release()
pygame.quit()
sys.exit()
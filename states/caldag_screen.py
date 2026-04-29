# =========================================================
# C A L D A G   R O U T E   S T A T E   (MAIN GAMEPLAY)
# =========================================================
from imports import *
from settings import *
import assets
import ui
import jeep
import passenger
import audio_manager
import effects
import camera

# =========================================================
# E V E N T   H A N D L I N G   ( K e y s  &  C l i c k s )
# =========================================================
def handle_caldag_events(event, current_state):
    new_state = current_state

    # ======================================================
    # G L O B A L   B O O S T   I N P U T (HOLD TO CHARGE)
    # ======================================================
    if jeep.current_gas > 0 and jeep.engine_on and not (ui.show_win_panel or ui.show_lose_panel):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left Click
                if not jeep.ss_is_active:
                    jeep.ss_charging = True
                    # --- START CHARGE SOUND ---
                    if not audio_manager.charge_playing:
                        assets.powerup_sound.play(-1)
                        audio_manager.charge_playing = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Pag bitaw ng click
                # --- STOP CHARGE SOUND AGAD ---
                assets.powerup_sound.stop()
                audio_manager.charge_playing = False
                
                if jeep.ss_charge_power >= 100 and not jeep.ss_is_active:
                    jeep.ss_is_active = True
                    jeep.ss_boost_timer = pygame.time.get_ticks()
                    jeep.jeep_speed = jeep_speed_original * ss_speed_multiplier
                else:
                    jeep.ss_charge_power = 0
                
                jeep.ss_charging = False

    # ===============================
    # K E Y B O A R D   I N P U T
    # ===============================
    if event.type == pygame.KEYDOWN:
        # --- CALDAG SCREEN KEYS ---
        if event.key == pygame.K_ESCAPE: 
            # --- 1. STOP ALL SOUNDS ---
            audio_manager.start_jeep_radio(0) 
            assets.engine_idle_sound.stop()
            assets.reverse_sound.stop()
            assets.powerup_sound.stop()
            assets.speedup_sound.stop()
            audio_manager.idle_playing = False
            audio_manager.reverse_playing = False
            audio_manager.music_started = False # Para bumalik ang main menu music
            
            # --- 2. RESET GAMEPLAY VARIABLES ---
            jeep.current_gas = 100
            jeep.current_health = 100
            ui.total_earnings = 0
            jeep.jeep_passengers_count = 0
            ui.stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
            
            # --- 3. RESET POSITION & PHYSICS ---
            jeep.jeep_x = width // 2 
            jeep.jeep_y = height - 150
            jeep.jeep_angle = 0
            jeep.jeep_speed = jeep_speed_original
            jeep.engine_on = False
            jeep.is_starting = False
            
            # --- 4. RESET TIME & SYSTEMS ---
            ui.game_hour = 5
            ui.game_minute = 30
            ui.time_counter = 0
            ui.rush_status = "NORMAL"
            passenger.is_rush_hour = False
            ui.night_alpha = 0
            jeep.headlight_on = False
            
            # --- 5. CLEAN UP OBJECTS ---
            effects.smoke_particles.clear()
            effects.horn_waves.clear()
            ui.payment_notifs.clear()
            
            # I-respawn ang mga passsenger sa random locations
            passenger.passengers_on_map = [passenger.Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
            
            # --- 6. SWITCH STATE ---
            new_state = "route"
            print("Game Reset and Back to Route Selection")

       
        if not (ui.show_win_panel or ui.show_lose_panel):
            if event.key == pygame.K_e:
                jeep.headlight_on = not jeep.headlight_on
                assets.click_sound.play()
                
            if event.key == pygame.K_r:
                if not jeep.engine_on and not jeep.is_starting:
                    jeep.is_starting = True
                    assets.engine_start_sound.play()
                    jeep.engine_start_timer = pygame.time.get_ticks() 
                elif jeep.engine_on:
                    jeep.engine_on = False
                    assets.engine_idle_sound.stop()
                    audio_manager.idle_playing = False
                    assets.click_sound.play()
                    jeep.ss_charging = False
                    jeep.ss_charge_power = 0
                    assets.powerup_sound.stop()
                    audio_manager.charge_playing = False
            
            # ITO UNG CHOICES NUNG MUSIC SA RADIO
            if event.key == pygame.K_RIGHT:
                assets.button_sound.play()
                audio_manager.current_music_index = (audio_manager.current_music_index + 1) % len(assets.playlist)
                audio_manager.start_jeep_radio(audio_manager.current_music_index)
                
            if event.key == pygame.K_LEFT:
                assets.button_sound.play()
                audio_manager.current_music_index = (audio_manager.current_music_index - 1) % len(assets.playlist)
                audio_manager.start_jeep_radio(audio_manager.current_music_index)

    # =========================
    # C L I C K   E V E N T S
    # =========================
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if ui.show_win_panel or ui.show_lose_panel:
            assets.button_sound.play()
            
            # 1. STOP LOSE MUSIC
            assets.lose_sound.stop()
            assets.win_music.stop()
            audio_manager.lose_music_playing = False
            audio_manager.music_started = False
            
            # --- ETO ANG "FORCE RESTART" NG MUSIC ---
            pygame.mixer.music.load("music/main bg music beep.mp3") 
            pygame.mixer.music.set_volume(0.4) 
            pygame.mixer.music.play(-1) 
            # ----------------------------------------
            
            # RESET ALL FOR NEXT DAY / RETRY
            ui.total_earnings = 0
            jeep.current_gas = 100
            jeep.current_health = 100
            jeep.jeep_passengers_count = 0
            ui.stats = {"Regular": 0, "Student": 0, "Senior": 0, "PWD": 0}
            
            # 2. POSITION & PHYSICS RESET
            jeep.jeep_x = width // 2 
            jeep.jeep_y = height - 150
            jeep.jeep_angle = 0
            jeep.jeep_speed = jeep_speed_original
            jeep.engine_on = False
            jeep.is_starting = False
            
            # 3. TIME & SYSTEM RESET
            ui.game_hour = 5
            ui.game_minute = 30
            ui.time_counter = 0
            ui.rush_status = "NORMAL"
            passenger.is_rush_hour = False
            ui.night_alpha = 0
            jeep.headlight_on = False
            
            # 4. OBJECTS & PARTICLES RESET (Linisin ang Map)
            effects.smoke_particles.clear()
            effects.horn_waves.clear()
            ui.payment_notifs.clear()
            # I-reset ang mga passenger sa map (babalik sa 15 na random)
            passenger.passengers_on_map = [passenger.Passenger(random.randint(100, 750), random.randint(100, 550)) for _ in range(15)]
            
            # 5. STATE & AUDIO RESET
            ui.show_win_panel = False
            ui.show_lose_panel = False
            ui.cutscene_started = False
            ui.win_cutscene_finished = False # Reset video flag
            assets.win_cutscene_vid.set(cv2.CAP_PROP_POS_FRAMES, 0) # I-rewind ang video pabalik sa zero
            new_state = "menu"
            
            # --- SUPER JEEP RESET ---
            jeep.ss_charging = False
            jeep.ss_is_active = False
            jeep.ss_charge_power = 0
            jeep.ss_boost_timer = 0
            audio_manager.charge_playing = False
            audio_manager.boost_sound_playing = False
            jeep.jeep_speed = jeep_speed_original # Balik to normal ang speed
            
            # Patayin ang mga sounds na baka nag-lo-loop
            assets.engine_idle_sound.stop()
            assets.reverse_sound.stop()
            assets.speedup_sound.stop()
            assets.powerup_sound.stop()
            audio_manager.idle_playing = False
            
            audio_manager.start_jeep_radio(0) 

    return new_state


# =========================================================
# G A M E P L A Y   L O O P   
# =========================================================
def run_caldag_frame(screen, keys):
    is_jeep_moving = False
    
    # ==========================================
    # U N I V E R S A L  H O R N  C O N T R O L
    # ==========================================
    if not (ui.show_win_panel or ui.show_lose_panel):
        if keys[pygame.K_SPACE]:
            if not audio_manager.horn_playing:
                assets.jeep_horn_sound.play(-1)
                audio_manager.horn_playing = True
            
            # WIFI EFFECT 
            if random.randint(0, 5) == 0:
                radians = math.radians(jeep.jeep_angle)
                front_dist = 35 
                wave_x = jeep.jeep_x - front_dist * math.sin(radians)
                wave_y = jeep.jeep_y - front_dist * math.cos(radians)
                effects.horn_waves.append([[wave_x, wave_y], 5, 255, jeep.jeep_angle])
        else:
            if audio_manager.horn_playing:
                assets.jeep_horn_sound.stop()
                audio_manager.horn_playing = False              

    radians = math.radians(jeep.jeep_angle) 
    game_active = not (ui.show_win_panel or ui.show_lose_panel)
    
    if game_active:
        # --- STEERING (A at D) ---
        if keys[pygame.K_a]:
            jeep.jeep_angle += rotation_speed
        if keys[pygame.K_d]:
            jeep.jeep_angle -= rotation_speed
            
        # --- PASSENGER CORE LOGIC ---
        is_jeep_moving = keys[pygame.K_w] or keys[pygame.K_s]
        jeep_vec = pygame.Vector2(jeep.jeep_x, jeep.jeep_y)
        
        # ======================================================
        # B O O S T   L O G I C   &   G A S   C O N S U M P T I O N
        # ======================================================
        jeep.current_consume_rate = 0 # variable para sa total bawas gas sa frame na ito
        
        # 1. (Normal gas consumption) - Check engine_on
        if (keys[pygame.K_w] or keys[pygame.K_s]) and jeep.engine_on:
            jeep.current_consume_rate = gas_consume_normal
            
        # 2. Habang nagcha-charge (MOUSE HOLD)
        if jeep.ss_charging and not jeep.ss_is_active and jeep.current_gas > 0:
            jeep.ss_charge_power += ss_charge_speed # Dagdag power
            jeep.current_consume_rate = gas_consume_charging # Mas mabilis bawas gas
            # Limit sa 100%
            if jeep.ss_charge_power > 100: 
                jeep.ss_charge_power = 100
                
        # 3. Habang nka-boost (TURBO ACTIVE)
        if jeep.ss_is_active:
            jeep.current_consume_rate = gas_consume_boosting 
            
            # --- START BOOST SOUND ---
            if not audio_manager.boost_sound_playing:
                assets.speedup_sound.play(-1)
                audio_manager.boost_sound_playing = True
            
            # Check timer para patayin ang boost
            if pygame.time.get_ticks() - jeep.ss_boost_timer > ss_boost_duration:
                jeep.ss_is_active = False
                jeep.jeep_speed = jeep_speed_original # Balik sa normal speed
                jeep.ss_charge_power = 0 # Reset charge
                
                # --- STOP BOOST SOUND ---
                assets.speedup_sound.stop()
                audio_manager.boost_sound_playing = False
                print("Boost ended.")
        
        # 4. APPLY GAS CONSUMPTION
        if jeep.current_consume_rate > 0 and jeep.engine_on:
            jeep.current_gas -= jeep.current_consume_rate
            if jeep.current_gas <= 0:
                jeep.current_gas = 0
                
                
                if not ui.show_win_panel:
                    pygame.mixer.stop()
                    ui.show_win_panel = True # Lalabas na ang panel pag 0 gas na
                    
                # ------------------------------
                # --- STOP ALL SOUNDS ---
                assets.powerup_sound.stop()
                assets.speedup_sound.stop()
                assets.engine_idle_sound.stop() 
                audio_manager.charge_playing = False
                audio_manager.boost_sound_playing = False
                audio_manager.idle_playing = False
                
                audio_manager.start_jeep_radio(0) 
                
                ui.show_win_panel = True
                
                # Patay ang boost kung naubusan ng gas
                if jeep.ss_is_active:
                    jeep.ss_is_active = False
                    jeep.jeep_speed = jeep_speed_original
                    jeep.ss_charging = False

        anyone_wants_to_stop = any(p.has_requested for p in passenger.passengers_on_map)
        
        for p in passenger.passengers_on_map:
            was_riding = p.is_riding
            p.update(jeep_vec, is_jeep_moving, jeep.jeep_passengers_count)
    
            if p.is_riding and not was_riding:
                if jeep.jeep_passengers_count < 18:
                    jeep.jeep_passengers_count += 1
                    # --- BAYAD LOGIC ---
                    p_type = random.choice(passenger_types)
                    fare = 11 if p_type in ["Student", "Senior", "PWD"] else 13
                    ui.total_earnings += fare
                    ui.stats[p_type] += 1
                    
                    cam_x, cam_y = camera.update_camera(jeep.jeep_x, jeep.jeep_y)
                    jeep_screen_x = (jeep.jeep_x - cam_x) * zoom_factor
                    jeep_screen_y = (jeep.jeep_y - cam_y) * zoom_factor
                    
                    # --- ASSIGN SPECIAL MISSION  ---
                    if p.is_special and jeep.active_mission_dest is None:
                        jeep.active_mission_dest = random.choice(special_destinations)
                        jeep.active_mission_passenger = p
                        jeep.mission_notif_timer = pygame.time.get_ticks() # TRIGGER ANG BANNER
                        ui.payment_notifs.append([[jeep_screen_x, jeep_screen_y - 60], "SPECIAL DROPOFF!", 255])
                        assets.click_sound.play() # Sound notification na may mission
                    else:
                        ui.payment_notifs.append([[jeep_screen_x, jeep_screen_y - 30], f"P{fare}", 255])
                    
                    assets.money_sound.play()
                    
                    # --- ASSIGN SPECIAL MISSION KUNG WALA PANG ACTIVE ---
                    if p.is_special and jeep.active_mission_dest is None:
                        jeep.active_mission_dest = random.choice(special_destinations)
                        jeep.active_mission_passenger = p
                        ui.payment_notifs.append([[jeep_screen_x, jeep_screen_y - 60], "SPECIAL DROPOFF!", 255])
                        assets.click_sound.play() # Sound notification na may mission
                    else:
                        ui.payment_notifs.append([[jeep_screen_x, jeep_screen_y - 30], f"P{fare}", 255])
                    
                    assets.money_sound.play() 
                else:
                    p.is_riding = False
                    
        # --- SEQUENTIAL DROP-OFF ---
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_f] and not is_jeep_moving:
            for p in passenger.passengers_on_map:
                if p.is_riding and p.has_requested:
                    if current_time - jeep.last_drop_time > 1600:
                        p.is_riding = False
                        p.is_leaving = True
                        p.has_requested = False
                        p.pos = pygame.Vector2(jeep.jeep_x + random.randint(-15, 15), jeep.jeep_y + random.randint(-15, 15))
                        jeep.jeep_passengers_count -= 1
                        jeep.last_drop_time = current_time # Reset timer
                        
                        # --- CLEAR MISSION KUNG SIYA YUNG BUMABA ---
                        if p == jeep.active_mission_passenger:
                            jeep.active_mission_dest = None
                            jeep.active_mission_passenger = None
                            ui.total_earnings += 50 # BONUS TIP!
                            # Kuha ng coords for notif
                            cam_x_n, cam_y_n = camera.update_camera(jeep.jeep_x, jeep.jeep_y)
                            j_scr_x = (jeep.jeep_x - cam_x_n) * zoom_factor
                            j_scr_y = (jeep.jeep_y - cam_y_n) * zoom_factor
                            ui.payment_notifs.append([[j_scr_x, j_scr_y - 40], "BONUS TIP: P50!", 255])
                            assets.money_sound.play()
                            
                        break 

        # --- ENGINE START DELAY CHECK ---
        if jeep.is_starting:
            if pygame.time.get_ticks() - jeep.engine_start_timer > 2000: 
                jeep.engine_on = True
                jeep.is_starting = False
                
        # --- MOVEMENT CONDITION ---
        can_move = jeep.engine_on and jeep.current_gas > 0 and jeep.current_health > 0 and not ui.show_win_panel
        
        if (keys[pygame.K_w] or keys[pygame.K_s]) and can_move:
            # --- LOW FUEL BEEP ---
            if jeep.current_gas <= 15 and random.randint(0, 80) == 0:
                assets.reverse_sound.play()
                
            if keys[pygame.K_w]:
                new_x = jeep.jeep_x - jeep.jeep_speed * math.sin(radians)
                new_y = jeep.jeep_y - jeep.jeep_speed * math.cos(radians)
                jeep_rect = pygame.Rect(0, 0, 25, 45)
                jeep_rect.center = (new_x, new_y)
                
                collision = False
                for wall in house_hitboxes:
                    if jeep_rect.colliderect(wall):
                        collision = True
                        curr_t = pygame.time.get_ticks()
                        if curr_t - jeep.last_damage_time > damage_cooldown:
                            jeep.current_health -= collision_damage
                            jeep.last_damage_time = curr_t
                            assets.accident_sound.play() 
                            
                            # --- SMOKE ON COLLISION ---
                            for _ in range(8):
                                effects.smoke_particles.append([[jeep.jeep_x, jeep.jeep_y], random.randint(4, 8), 200])
                        break
                if not collision: 
                    jeep.jeep_x, jeep.jeep_y = new_x, new_y
                    
            elif keys[pygame.K_s]:
                if not audio_manager.reverse_playing:
                    assets.reverse_sound.play(-1)
                    audio_manager.reverse_playing = True
                    
                new_x = jeep.jeep_x + reverse_speed * math.sin(radians)
                new_y = jeep.jeep_y + reverse_speed * math.cos(radians)
                jeep_rect = pygame.Rect(0, 0, 25, 45)
                jeep_rect.center = (new_x, new_y)
                
                collision = False
                for wall in house_hitboxes:
                    if jeep_rect.colliderect(wall):
                        collision = True
                        curr_t = pygame.time.get_ticks()
                        if curr_t - jeep.last_damage_time > damage_cooldown:
                            jeep.current_health -= collision_damage
                            jeep.last_damage_time = curr_t
                            assets.accident_sound.play()
                        break
                if not collision: 
                    jeep.jeep_x, jeep.jeep_y = new_x, new_y
                    
        # --- STOP REVERSE SOUND ---
        if not keys[pygame.K_s] or jeep.current_gas <= 0:
            if audio_manager.reverse_playing:
                assets.reverse_sound.stop()
                audio_manager.reverse_playing = False

        if (keys[pygame.K_w] or keys[pygame.K_s]) and jeep.current_gas > 0 and jeep.current_health > 0:
            #FOR SMOKE
            offset = 40 
            smoke_x = jeep.jeep_x + offset * math.sin(radians)
            smoke_y = jeep.jeep_y + offset * math.cos(radians)
            effects.smoke_particles.append([[smoke_x, smoke_y], random.randint(3, 8), 200])
            
        # Update at Fade-out logic ng smoke
        for particle in effects.smoke_particles[:]:
            particle[2] -= 8  
            particle[1] += 0.5 
            if particle[2] <= 0:
                effects.smoke_particles.remove(particle) 
                
        # --- TIME PROGRESSION LOGIC ---
        ui.time_counter += time_tick_speed
        if ui.time_counter >= 60:
            ui.game_minute += 1
            ui.time_counter = 0
            
        if ui.game_minute >= 60:
            ui.game_hour += 1
            ui.game_minute = 0
            
        if ui.game_hour >= 20 and ui.game_minute >= 30: # Stop sa 8:30 PM
            ui.game_hour = 20
            ui.game_minute = 30
            if not ui.show_win_panel:
                pygame.mixer.stop()
                ui.show_win_panel = True
                
        # --- DYNAMIC DARKNESS LOGIC (6 PM - 7 PM) ---
        if ui.game_hour == 18: # 6 PM
            ui.night_alpha = ui.game_minute * 2.5 
        elif ui.game_hour >= 19: # 7 PM onwards
            ui.night_alpha = 200 # Max na dilim
        else:
            ui.night_alpha = 0 # Umaga
            
        # --- RUSH HOUR TRACKER LOGIC ---
        new_status = "NORMAL"
        # 7:30 AM - 7:59 AM (Warning) | 3:30 PM - 3:59 PM (Warning)
        if (ui.game_hour == 7 and ui.game_minute >= 30) or (ui.game_hour == 15 and ui.game_minute >= 30):
            new_status = "WARNING"
        # 8:00 AM - 10:00 AM (Active) | 4:00 PM - 7:00 PM (Active)
        elif (8 <= ui.game_hour < 10) or (16 <= ui.game_hour < 19):
            new_status = "ACTIVE"
            
        if new_status != ui.rush_status:
            ui.rush_status = new_status
            ui.rush_notif_timer = pygame.time.get_ticks() 
            if ui.rush_status != "NORMAL":
                assets.button_sound.play()
                
        # --- RUSH HOUR SPAWNING ---
        if ui.rush_status == "ACTIVE":
            passenger.is_rush_hour = True
            
            if len(passenger.passengers_on_map) < 55: 
                
                if random.randint(1, 100) == 1: 
                    new_p = passenger.Passenger(random.randint(50, 800), random.randint(50, 600))
                    passenger.passengers_on_map.append(new_p)
        else:
            passenger.is_rush_hour = False
            # Kapag normal hours
            if len(passenger.passengers_on_map) > 15:
                if random.randint(1, 30) == 1: 
                    for p in passenger.passengers_on_map:
                        
                        if not p.is_riding and not p.approaching and not p.is_leaving:
                            passenger.passengers_on_map.remove(p)
                            break # Isa-isa lang ang pag-alis para smooth

    # ======================================================
    # C A M E R A   S E T U P   &   D R A W I N G
    # ======================================================
    screen.fill((0, 0, 0))
    
    # camera and get coords
    cam_x, cam_y = camera.update_camera(jeep.jeep_x, jeep.jeep_y)
    
    # 2. DRAW BACKGROUND 
    bg_w = int(width * zoom_factor)
    bg_h = int(height * zoom_factor)
    scaled_bg = pygame.transform.scale(assets.route_caldag_img, (bg_w, bg_h))
    
    # --- SHAKE CALCULATION ---
    s_offset_x, s_offset_y = camera.get_shake_offset(jeep.last_damage_time)
    
    bg_draw_x = (-cam_x * zoom_factor) + s_offset_x
    bg_draw_y = (-cam_y * zoom_factor) + s_offset_y
    screen.blit(scaled_bg, (bg_draw_x, bg_draw_y))

    # --- DRAWING NG MGA BAHAY ---
    if SHOW_HITBOXES:
        for wall in house_hitboxes:
            draw_x = (wall.x - cam_x) * zoom_factor
            draw_y = (wall.y - cam_y) * zoom_factor
            draw_w = wall.width * zoom_factor
            draw_h = wall.height * zoom_factor
            
            debug_surf = pygame.Surface((draw_w, draw_h), pygame.SRCALPHA)
            debug_surf.fill((255, 0, 0, 100)) 
            screen.blit(debug_surf, (draw_x, draw_y))
            pygame.draw.rect(screen, (255, 0, 0), (draw_x, draw_y, draw_w, draw_h), 2)

    # ------------------------------------------------------
    # 1. JEEP DEFINITION & DRAWING (MUNA)
    # ------------------------------------------------------
    jeep_scaled = pygame.transform.rotozoom(assets.jeep_img_original, jeep.jeep_angle, zoom_factor)
    
    # Screen position ng jeep
    jeep_screen_x = (jeep.jeep_x - cam_x) * zoom_factor
    jeep_screen_y = (jeep.jeep_y - cam_y) * zoom_factor
    
    # --- ENGINE SHAKE CALCULATION ---
    jeep.engine_shake_x = 0
    jeep.engine_shake_y = 0
    if jeep.engine_on:
        if not audio_manager.idle_playing:
            assets.engine_idle_sound.play(-1)
            audio_manager.idle_playing = True
            
        # Subtle vibration
        jeep.engine_shake_x = random.uniform(-2.0, 2.0)
        jeep.engine_shake_y = random.uniform(-2.0, 2.0)
        
        if jeep.ss_charging:
            jeep.engine_shake_x = random.uniform(-2.5, 2.5)
            jeep.engine_shake_y = random.uniform(-2.5, 2.5)
            
    # Idagdag ang shake sa final rect position
    rect = jeep_scaled.get_rect(center=(jeep_screen_x + s_offset_x + jeep.engine_shake_x, 
                                        jeep_screen_y + s_offset_y + jeep.engine_shake_y))
                                        
    # ======================================================
    # S U P E R  S A I Y A N  A U R A  (GLOW EFFECT)
    # ======================================================
    if (jeep.ss_charging or jeep.ss_is_active) and jeep.engine_on:
        jeep.aura_alpha = random.randint(100, 200) 
        if jeep.ss_is_active:
            aura_color = (255, 100, 0, jeep.aura_alpha) # Orange/Fire mode
        else:
            aura_color = (255, 255, 0, jeep.aura_alpha) # Normal Yellow charge
        
        for _ in range(random.randint(5, 10)):
            offset_x = random.randint(int(-30 * zoom_factor), int(30 * zoom_factor))
            offset_y = random.randint(int(-40 * zoom_factor), int(40 * zoom_factor))
            glow_radius = random.randint(2, 6)
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, aura_color, (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surf, (jeep_screen_x + offset_x, jeep_screen_y + offset_y))
            
        big_aura_radius = int(50 * zoom_factor)
        big_aura_surf = pygame.Surface((big_aura_radius * 2, big_aura_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(big_aura_surf, (255, 200, 0, 50), (big_aura_radius, big_aura_radius), big_aura_radius)
        screen.blit(big_aura_surf, (jeep_screen_x - big_aura_radius, jeep_screen_y - big_aura_radius))

    # ======================================================
    # J E E P  G L O W  &  S H A K E
    # ======================================================
    if (jeep.ss_charging or jeep.ss_is_active) and jeep.engine_on:
        glow_overlay = jeep_scaled.copy()
        glow_color = (255, 255, 0) if not jeep.ss_is_active else (255, 150, 0)
        glow_overlay.fill(glow_color, special_flags=pygame.BLEND_RGB_ADD)
        glow_overlay.set_alpha(random.randint(60, 160))
        
        if jeep.ss_charging:
            rect.x += random.randint(-3, 3)
            rect.y += random.randint(-3, 3)
        
        screen.blit(jeep_scaled, rect)
        screen.blit(glow_overlay, rect)
    else:
        screen.blit(jeep_scaled, rect)

    # ------------------------------------------------------
    # 2. DRAW USOK AT APOY (PAGKATAPOS NG JEEP - PARA NASA IBABAW)
    # ------------------------------------------------------
    for p in effects.smoke_particles:
        p_draw_x = (p[0][0] - cam_x) * zoom_factor
        p_draw_y = (p[0][1] - cam_y) * zoom_factor
        p_radius = int(p[1] * zoom_factor)
        
        is_fire = p[3] if len(p) > 3 else False
        
        if is_fire:
            color = p[4] if len(p) > 4 else (255, 100, 0)
            p[0][1] -= 0.7  # Rising effect paitaas
        else:
            color = (120, 120, 120)
            p[0][1] -= 0.3
            
        s_surf = pygame.Surface((p_radius*2, p_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s_surf, (*color, p[2]), (p_radius, p_radius), p_radius)
        
        if is_fire:
            screen.blit(s_surf, (p_draw_x - p_radius, p_draw_y - p_radius), special_flags=pygame.BLEND_RGBA_ADD)
        else:
            screen.blit(s_surf, (p_draw_x - p_radius, p_draw_y - p_radius))

    # --- DRAW PASSENGERS ON MAP ---
    for p in passenger.passengers_on_map:
        if not p.is_riding and p.alpha > 0:
            p_x = (p.pos.x - cam_x) * zoom_factor
            p_y = (p.pos.y - cam_y) * zoom_factor
            
            p_surf = pygame.transform.scale(p.image, (int(25 * zoom_factor), int(25 * zoom_factor)))
            if p.is_leaving:
                p_surf.set_alpha(p.alpha) # Fade effect
            p_rect = p_surf.get_rect(center=(p_x, p_y))
            screen.blit(p_surf, p_rect)
            
            # --- SPEECH BUBBLE DRAWING ---
            if p.message != "":
                m_surf = assets.small_font.render(p.message, True, (0, 0, 0))
                m_rect = m_surf.get_rect(center=(p_x, p_y - 40))
                
                bg_rect = m_rect.inflate(10, 10)
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=5)
                pygame.draw.rect(screen, (0, 0, 0), bg_rect, 1, border_radius=5)
                screen.blit(m_surf, m_rect)

    # ======================================================
    # DRAW BOOST CHARGE BAR (ABOVE JEEP)
    # ======================================================
    if (jeep.ss_charging or jeep.ss_is_active or jeep.ss_charge_power > 0) and jeep.engine_on:
        bar_w = int(40 * zoom_factor)
        bar_h = int(5 * zoom_factor)
        bar_x = jeep_screen_x - (bar_w // 2)
        bar_y = jeep_screen_y - (rect.height // 2) - int(10 * zoom_factor)
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        fill_w = int((jeep.ss_charge_power / max_boost_power) * bar_w)
        bar_color = (255, 215, 0) # Gold
        if jeep.ss_charge_power >= 100: bar_color = (255, 100, 0) # Orange
        if jeep.ss_charge_power > 0:
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
        if jeep.ss_charge_power >= 100:
            ss_text = assets.custom_font.render("SUPER JEEP!", True, (255, 255, 0))
            text_x = jeep_screen_x - (ss_text.get_width() // 2)
            text_y = bar_y - ss_text.get_height() - 5
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                 outline_surf = assets.custom_font.render("SUPER JEEP!", True, (150, 0, 0))
                 screen.blit(outline_surf, (text_x + dx, text_y + dy))
            screen.blit(ss_text, (text_x, text_y))

    # === WIFI DRAWING ===
    for wave in effects.horn_waves[:]:
        wave[1] += 3   
        wave[2] -= 15  
        if wave[2] <= 0:
            effects.horn_waves.remove(wave)
        else:
            d_x = (wave[0][0] - cam_x) * zoom_factor
            d_y = (wave[0][1] - cam_y) * zoom_factor
            s_rad = int(wave[1] * zoom_factor)
            surf = pygame.Surface((s_rad * 2, s_rad * 2), pygame.SRCALPHA)
            s_arc = math.radians(wave[3] + 65)
            e_arc = math.radians(wave[3] + 115)
            pygame.draw.arc(surf, (255, 255, 255, wave[2]), (0, 0, s_rad * 2, s_rad * 2), s_arc, e_arc, 3)
            screen.blit(surf, (d_x - s_rad, d_y - s_rad))

    # ======================================================
    # S P E C I A L  M I S S I O N  G R A P H I C S  &  G P S
    # ======================================================
    if jeep.active_mission_dest:
        dest_x = (jeep.active_mission_dest.x - cam_x) * zoom_factor
        dest_y = (jeep.active_mission_dest.y - cam_y) * zoom_factor

        # 1. DRAW GPS LINE (Animated Dashed Line)
        dx = dest_x - jeep_screen_x
        dy = dest_y - jeep_screen_y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            dash_length = 15
            dash_gap = 10
            total_dashes = int(dist / (dash_length + dash_gap))
            
            for i in range(total_dashes):
                offset = (pygame.time.get_ticks() / 15) % (dash_length + dash_gap)
                
                start_ratio = max(0, (i * (dash_length + dash_gap) + offset) / dist)
                end_ratio = min(1, (i * (dash_length + dash_gap) + dash_length + offset) / dist)
                
                start_pos = (jeep_screen_x + dx * start_ratio, jeep_screen_y + dy * start_ratio)
                end_pos = (jeep_screen_x + dx * end_ratio, jeep_screen_y + dy * end_ratio)
                
                # Kulay Cyan (Blue-Green) na line
                pygame.draw.line(screen, (0, 255, 255), start_pos, end_pos, 3) 

        # 2. DRAW DROP-OFF CIRCLE SA MAP
        pulse = abs(math.sin(pygame.time.get_ticks() / 300)) * 10
        pygame.draw.circle(screen, (0, 255, 0), (int(dest_x), int(dest_y)), int(30 * zoom_factor + pulse), 3)

        # 3. DRAW ARROW POINTING TO DESTINATION)
        angle_to_dest = math.atan2(dy, dx)
        arrow_dist = 70 * zoom_factor 
        arrow_x = jeep_screen_x + math.cos(angle_to_dest) * arrow_dist
        arrow_y = jeep_screen_y + math.sin(angle_to_dest) * arrow_dist
        
        p1 = (arrow_x + math.cos(angle_to_dest) * 15, arrow_y + math.sin(angle_to_dest) * 15)
        p2 = (arrow_x + math.cos(angle_to_dest + 2.5) * 10, arrow_y + math.sin(angle_to_dest + 2.5) * 10)
        p3 = (arrow_x + math.cos(angle_to_dest - 2.5) * 10, arrow_y + math.sin(angle_to_dest - 2.5) * 10)
        pygame.draw.polygon(screen, (255, 215, 0), [p1, p2, p3]) 
        pygame.draw.polygon(screen, (0, 0, 0), [p1, p2, p3], 2)   

        dist_to_dest = math.hypot(jeep.active_mission_dest.x - jeep.jeep_x, jeep.active_mission_dest.y - jeep.jeep_y)
        if dist_to_dest < 40 and not jeep.active_mission_passenger.has_requested:
            jeep.active_mission_passenger.has_requested = True
            jeep.active_mission_passenger.message = "Dito na lang po!"
            if not audio_manager.para_sound_played:
                assets.knocking_sound.play()
                audio_manager.para_sound_played = True

    # ======================================================
    # S P E C I A L  M I S S I O N  N O T I F I C A T I O N
    # ======================================================
    # Magpapakita ang banner sa loob ng 4 seconds
    if jeep.active_mission_dest and pygame.time.get_ticks() - jeep.mission_notif_timer < 4000:
        notif_w, notif_h = 360, 60
        notif_x = (width // 2) - (notif_w // 2)
        notif_y = 80 # Sa ilalim ng time/quota bar
        
        # Transparent Blue Background
        banner_surf = pygame.Surface((notif_w, notif_h), pygame.SRCALPHA)
        pygame.draw.rect(banner_surf, (0, 50, 150, 200), (0, 0, notif_w, notif_h), border_radius=10)
        screen.blit(banner_surf, (notif_x, notif_y))
        pygame.draw.rect(screen, (0, 255, 255), (notif_x, notif_y, notif_w, notif_h), 2, border_radius=10)
        
        txt1 = assets.medium_font.render("NEW PASSENGER MISSION!", True, (255, 255, 0))
        txt2 = assets.small_font.render("line papunta sa destination.", True, (255, 255, 255))
        
        screen.blit(txt1, (notif_x + (notif_w//2) - (txt1.get_width()//2), notif_y + 10))
        screen.blit(txt2, (notif_x + (notif_w//2) - (txt2.get_width()//2), notif_y + 35))
    
    # --- NIGHT OVERLAY DRAWING ---
    if ui.night_alpha > 0:
        night_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        night_overlay.fill((0, 0, 20, int(ui.night_alpha))) 
        if jeep.headlight_on:
            rad_l = math.radians(jeep.jeep_angle)
            
            forward_dist = 35 * zoom_factor 
            side_dist = 11 * zoom_factor 
            
            light_positions = [
                (jeep_screen_x - forward_dist * math.sin(rad_l) - side_dist * math.cos(rad_l),
                 jeep_screen_y - forward_dist * math.cos(rad_l) + side_dist * math.sin(rad_l)),
                (jeep_screen_x - forward_dist * math.sin(rad_l) + side_dist * math.cos(rad_l),
                 jeep_screen_y - forward_dist * math.cos(rad_l) - side_dist * math.sin(rad_l))
            ]
            combined_beams = pygame.Surface((width, height), pygame.SRCALPHA)
            
            for pos in light_positions:
                for layer in range(6):
                    beam_len = (180 + (layer * 20)) * zoom_factor 
                    spread = math.radians(15 + (layer * 5))
                    
                    p1 = pos
                    p2 = (pos[0] - beam_len * math.sin(rad_l - spread),
                          pos[1] - beam_len * math.cos(rad_l - spread))
                    p3 = (pos[0] - beam_len * math.sin(rad_l + spread),
                          pos[1] - beam_len * math.cos(rad_l + spread))
                    base_brightness = 450
                    alpha_val = min(255, max(0, int(base_brightness - (layer * 20))))
                    
                    pygame.draw.polygon(combined_beams, (0, 0, 0, alpha_val), [p1, p2, p3])   
            night_overlay.blit(combined_beams, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)     
        screen.blit(night_overlay, (0, 0))

    # --- PFP PANEL (KALIWA) ---
    screen.blit(assets.pfp_panel, (assets.pfp_display_x, assets.pfp_display_y))
    pfp_user_surf = assets.custom_font.render(ui.user_text, True, (255, 255, 255))
    screen.blit(pfp_user_surf, (assets.pfp_display_x + 65, assets.pfp_display_y + 19))
    
    # --- PASSENGER PANEL ---
    pass_panel_y_pos = assets.pfp_display_y + assets.pfp_panel.get_height() + 5
    screen.blit(assets.passenger_panel, (assets.pfp_display_x, pass_panel_y_pos))
    
    # --- JEEP RADIO PANEL (TOP RIGHT) ---
    radio_x = width - 180
    radio_y = 75
    radio_bg_rect = pygame.Rect(radio_x, radio_y, 160, 65)
    radio_surf = pygame.Surface((160, 65), pygame.SRCALPHA)
    radio_surf.fill((0, 0, 0, 150)) 
    screen.blit(radio_surf, (radio_x, radio_y))
    pygame.draw.rect(screen, (255, 255, 255), radio_bg_rect, 2, border_radius=8)
    
    l_arrow = assets.custom_font.render("<", True, (255, 255, 255))
    r_arrow = assets.custom_font.render(">", True, (255, 255, 255))
    screen.blit(l_arrow, (radio_x + 15, radio_y + 35))
    screen.blit(r_arrow, (radio_x + 130, radio_y + 35))
    
    radio_label = assets.small_font.render("JEEP RADIO", True, (200, 200, 200))
    screen.blit(radio_label, (radio_x + 23, radio_y + 10)) 
    
    curr_song = assets.playlist[audio_manager.current_music_index]["name"]
    if curr_song == "OFF":
        song_txt = assets.small_font.render(curr_song, True, (255, 0, 0))
    else:
        song_txt = assets.small_font.render(curr_song, True, (255, 215, 0))
    song_x_pos = radio_x + (80 - (song_txt.get_width() // 2)) + 3
    screen.blit(song_txt, (song_x_pos, radio_y + 35))    
        
    if jeep.jeep_passengers_count >= 18:
        indicator_surf = assets.small_font.render("FULL!", True, (255, 0, 0))
    else:
        indicator_surf = assets.small_font.render(f"{jeep.jeep_passengers_count}/18", True, (255, 255, 255))
    screen.blit(indicator_surf, (assets.pfp_display_x + 73, pass_panel_y_pos + 27))
    
    # --- DIGITAL CLOCK DISPLAY ---
    display_hour = ui.game_hour
    am_pm = "AM"
    if ui.game_hour >= 12:
        am_pm = "PM"
        if ui.game_hour > 12: display_hour -= 12
    
    time_string = f"{display_hour:02}:{ui.game_minute:02} {am_pm}"
    time_surf = assets.custom_font.render(time_string, True, (255, 255, 255))
    
    box_width = 200 
    box_height = 50
    box_x = (width // 2) - (box_width // 2)
    box_y = 15
    
    time_bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, (0, 0, 0, 150), time_bg_rect, border_radius=12) 
    pygame.draw.rect(screen, (255, 255, 255), time_bg_rect, 2, border_radius=12) 
    
    text_x = (width // 2) - (time_surf.get_width() // 2)
    text_y = box_y + (box_height // 2) - (time_surf.get_height() // 2)
    screen.blit(time_surf, (text_x, text_y))
    
    # ------------------------------------------------------
    # (ENGINE INDICATOR)
    # ------------------------------------------------------
    gas_x, gas_y = 25, height - 35
    bar_w, bar_h = 130, 18
    
    # --- ENGINE INDICATOR ---
    eng_col = (0, 255, 0) if jeep.engine_on else (255, 0, 0)
    if jeep.is_starting: eng_col = (255, 255, 0)
    eng_txt = "ENGINE: ON" if jeep.engine_on else "ENGINE: OFF"
    if jeep.is_starting: eng_txt = "STARTING..."
    
    eng_surf = assets.small_font.render(eng_txt, True, eng_col)
    screen.blit(eng_surf, (gas_x, gas_y - 35)) 
    
    # --- FUEL BAR DRAWING ---
    pygame.draw.rect(screen, (30, 30, 30), (gas_x, gas_y, bar_w, bar_h))
    fill_g = int((jeep.current_gas / max_gas) * (bar_w - 4))
    pygame.draw.rect(screen, (0, 255, 0) if jeep.current_gas > 25 else (255, 0, 0), (gas_x + 2, gas_y + 2, max(0, fill_g), bar_h - 4))
    
    gas_txt = assets.small_font.render(f"FUEL: {int(jeep.current_gas)}%", True, (255, 255, 255))
    screen.blit(gas_txt, (gas_x, gas_y - 18))
    
    # --- Condition Bar (Health) ---
    health_x = gas_x + bar_w + 20
    pygame.draw.rect(screen, (30, 30, 30), (health_x, gas_y, bar_w, bar_h))
    
    fill_h = int((max(0, jeep.current_health) / max_health) * (bar_w - 4))
    h_col = (0, 255, 0) if jeep.current_health > 60 else (255, 255, 0) if jeep.current_health > 30 else (255, 0, 0)
    
    if jeep.current_health <= 0:
        jeep.current_health = 0
        if not ui.show_lose_panel:
            ui.show_lose_panel = True
            assets.engine_idle_sound.stop()
            assets.reverse_sound.stop()
            assets.powerup_sound.stop()
            assets.speedup_sound.stop()
            audio_manager.start_jeep_radio(0) 
            
            audio_manager.idle_playing = False
            audio_manager.reverse_playing = False
            
            if not audio_manager.lose_music_playing:
                assets.lose_sound.play(-1) 
                audio_manager.lose_music_playing = True
                
    if jeep.current_health > 0:
        pygame.draw.rect(screen, h_col, (health_x + 2, gas_y + 2, fill_h, bar_h - 4))
        
    # ======================================================
    # W A R N I N G   S I G N S   (LOW FUEL & CRITICAL CONDITION)
    # ======================================================
    warn_font = pygame.font.Font("Fonts/pixelated fonts.ttf", 15)
    warn_y = height - 70 # Pwesto sa taas ng bars
    
    # LOW FUEL WARNING
    if jeep.current_gas <= 25:
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            fuel_warn = warn_font.render("⚠ LOW FUEL!", True, (255, 0, 0))
            screen.blit(fuel_warn, (25, warn_y - 20))
            
    # CRITICAL CONDITION WARNING
    if jeep.current_health <= 25:
        if (pygame.time.get_ticks() // 400) % 2 == 0:
            health_warn = warn_font.render("LOW HEALTH!", True, (255, 165, 0))
            screen.blit(health_warn, (health_x, warn_y))
            
    health_txt = assets.small_font.render(f"HEALTH: {int(max(0, jeep.current_health))}%", True, (255, 255, 255))
    screen.blit(health_txt, (health_x, gas_y - 18))
    
    if not is_jeep_moving and jeep.jeep_passengers_count > 0:
        hint_txt_str = "[F] para pababain"
        hint_x = assets.pfp_display_x
        hint_y = pass_panel_y_pos + assets.passenger_panel.get_height() + 10
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            border_surf = assets.medium_font.render(hint_txt_str, True, (0, 0, 0))
            screen.blit(border_surf, (hint_x + dx, hint_y + dy))
        main_hint_surf = assets.medium_font.render(hint_txt_str, True, (255, 255, 255))
        screen.blit(main_hint_surf, (hint_x, hint_y))

    # --- AUTO SMOKE & FIRE LOGIC ---
    if jeep.current_health < 50: 
        if random.randint(0, 10) == 0:
            effects.smoke_particles.append([[jeep.jeep_x, jeep.jeep_y], random.randint(3, 6), 150, False])
            
    if jeep.current_health < 25: 
        if random.randint(0, 5) == 0:
            fire_x = jeep.jeep_x + random.randint(-12, 12)
            fire_y = jeep.jeep_y + random.randint(-12, 12)
            fire_color = random.choice([(255, 30, 0), (255, 120, 0), (255, 200, 0)])
            effects.smoke_particles.append([[fire_x, fire_y], random.randint(3, 8), 255, True, fire_color])
            
    # --- PARA! INDICATOR ---
    anyone_wants_to_stop = any(p.has_requested for p in passenger.passengers_on_map)
    if anyone_wants_to_stop:
        if not audio_manager.para_sound_played:
            assets.knocking_sound.play()
            audio_manager.para_sound_played = True
        # ---------------------------
        para_w, para_h = 120, 35
        para_x = (width // 2) - (para_w // 2)
        para_y = 110 
        pygame.draw.rect(screen, (200, 0, 0), (para_x, para_y, para_w, para_h), border_radius=8)
        para_txt = assets.custom_font.render("PARA!", True, (255, 255, 255))
        para_txt_x = para_x + (para_w // 2) - (para_txt.get_width() // 2)
        para_txt_y = para_y + (para_h // 2) - (para_txt.get_height() // 2)
        screen.blit(para_txt, (para_txt_x, para_txt_y))
    else:
        audio_manager.para_sound_played = False

    # ======================================================
    # UI: QUOTA (TOP RIGHT - ABOVE RADIO)
    # ======================================================
    q_x, q_y = width - 180, 15
    pygame.draw.rect(screen, (0, 0, 0, 150), (q_x, q_y, 160, 55), border_radius=5)
    pygame.draw.rect(screen, (255, 255, 255), (q_x, q_y, 160, 55), 2, border_radius=5)
    
    q_prog = min(1.0, ui.total_earnings / daily_quota)
    pygame.draw.rect(screen, (0, 150, 0), (q_x + 10, q_y + 30, 140, 15)) # Background bar
    pygame.draw.rect(screen, (0, 255, 0), (q_x + 10, q_y + 30, 140 * q_prog, 15)) # Progress
    
    q_text = assets.quota_font.render(f"QUOTA: {ui.total_earnings}/{daily_quota}", True, (255, 255, 255))
    screen.blit(q_text, (q_x + 12, q_y + 12))

    # ======================================================
    # UI: DASHBOARD (BOTTOM RIGHT)
    # ======================================================
    d_w, d_h = 175, 110
    d_x, d_y = width - d_w - 15, height - d_h - 15
    dash_surf = pygame.Surface((d_w, d_h), pygame.SRCALPHA)
    dash_surf.fill((0, 0, 0, 180))
    screen.blit(dash_surf, (d_x, d_y))
    pygame.draw.rect(screen, (255, 215, 0), (d_x, d_y, d_w, d_h), 2, border_radius=10)
    screen.blit(assets.medium_font.render("DASHBOARD", True, (255, 215, 0)), (d_x + 18, d_y + 5))
    
    y_gap = 28
    for p_type, count in ui.stats.items():
        f_val = 11 if p_type != "Regular" else 13
        s_txt = assets.dash_info_font.render(f"{p_type}(P{f_val}): {count}", True, (240, 240, 240))
        screen.blit(s_txt, (d_x + 10, d_y + y_gap))
        y_gap += 18

    # ======================================================
    # FLOATING PAYMENT NOTIFS (ANIMATION)
    # ======================================================
    for n in ui.payment_notifs[:]:
        n[0][1] -= 1 
        n[2] -= 5    
        if n[2] <= 0: 
            ui.payment_notifs.remove(n)
        else:
            pay_surf = assets.medium_font.render(n[1], True, (255, 255, 0))
            pay_surf.set_alpha(n[2])
            screen.blit(pay_surf, (n[0][0], n[0][1]))

    # --- RUSH HOUR MESSAGE DISPLAY ---
    curr_t = pygame.time.get_ticks()
    if ui.rush_status != "NORMAL" and (curr_t - ui.rush_notif_timer < rush_notif_duration):
        if ui.rush_status == "WARNING":
            b_col = (255, 165, 0, 180) # Orange Bar
            txt1 = "COMING SOON: RUSH HOUR!"
            txt2 = "MALAPIT NA ANG DAGSA NG TAO, MAG-READY NA!"
        else: # ACTIVE
            b_col = (200, 0, 0, 200)   # Red Bar
            txt1 = "RUSH HOUR ACTIVE!"
            txt2 = "DAGSA ANG PASAHERO! BILISAN ANG PASADA!"
            
        r_overlay = pygame.Surface((width, 80), pygame.SRCALPHA)
        r_overlay.fill(b_col)
        screen.blit(r_overlay, (0, height // 2 - 40))
        m_s = assets.custom_font.render(txt1, True, (255, 255, 255))
        s_s = assets.small_font.render(txt2, True, (255, 255, 0))
        screen.blit(m_s, (width//2 - m_s.get_width()//2, height//2 - 25))
        screen.blit(s_s, (width//2 - s_s.get_width()//2, height//2 + 5))

# ======================================================
    # W I N / S U M M A R Y   P A N E L   (8:30 PM)
    # ======================================================
    if ui.show_win_panel:
        # --- VIDEO CUTSCENE ---
        if not ui.win_cutscene_finished:
            current_time = pygame.time.get_ticks()

            if not getattr(ui, 'cutscene_started', False):
                pygame.mixer.stop()  
                assets.win_video_audio.play() 
                
                # REWIND: Siguraduhin na ang video ay nasa frame 0
                assets.win_cutscene_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                
                ui.cutscene_started = True
                ui.last_vid_time = 0
                ui.cutscene_surf = None
                print("Cutscene Started!") 

            # B. VIDEO PLAYER (30 FPS)
            if current_time - ui.last_vid_time > 33:
                ret, frame = assets.win_cutscene_vid.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (width, height))
                    ui.cutscene_surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    ui.last_vid_time = current_time
                else:
                    print("Video Finished. Switching to Panel.")
                    ui.win_cutscene_finished = True
                    assets.win_video_audio.stop()
                    assets.win_music.play(-1) # Start win music

            # C. BLIT THE VIDEO FRAME
            if ui.cutscene_surf:
                screen.blit(ui.cutscene_surf, (0, 0))
                
                # ======================================================
                # ADDING "CONGRATULATIONS" AT THE BOTTOM
                # ======================================================
                congrat_txt = assets.custom_font.render("CONGRATULATIONS! MISSION ACCOMPLISHED!", True, (255, 215, 0))
                
                txt_x = (width // 2) - (congrat_txt.get_width() // 2)
                txt_y = height - 60 # 60 pixels mula sa baba
                
                # black outline
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    outline_surf = assets.custom_font.render("CONGRATULATIONS! MISSION ACCOMPLISHED!", True, (0, 0, 0))
                    screen.blit(outline_surf, (txt_x + dx, txt_y + dy))
                
                screen.blit(congrat_txt, (txt_x, txt_y))
              
            else:
                screen.fill((0, 0, 0))
                
        # --- WIN PANEL DRAWING ---
        else:
            ui.win_anim_counter += 0.25 
            # 2. BACKGROUND & OVERLAY
            ret, frame = assets.blurdbg_vid.read()
            if not ret:
                assets.blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = assets.blurdbg_vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (width, height))
                bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            
            # Screen Dance
            sway_x = math.sin(ui.win_anim_counter * 0.8) * 12
            sway_y = math.cos(ui.win_anim_counter * 0.8) * 8
            screen.blit(bg_surface, (sway_x, sway_y))
            
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            screen.blit(overlay, (0, 0))
            
            # 3. PANEL BOUNCE LOGIC
            bounce_y = int(abs(math.sin(ui.win_anim_counter)) * -15) 
            panel_rect = assets.win_panel.get_rect(center=(width // 2, (height // 2) + bounce_y))
            screen.blit(assets.win_panel, panel_rect)
            
            # 4. TEXT DISPLAY 
            gas_used = max_gas - jeep.current_gas
            gas_expense = int(gas_used * gas_price_per_unit)
            take_home = ui.total_earnings - daily_quota - gas_expense
            
            px, py = panel_rect.x, panel_rect.y
            text_col = (0, 0, 0)
            
            screen.blit(assets.medium_font.render(f" {ui.total_earnings}", True, text_col), (px + 300, py + 70))
            screen.blit(assets.medium_font.render(f" {daily_quota}", True, text_col), (px + 300, py + 117))
            screen.blit(assets.medium_font.render(f" {gas_expense}", True, text_col), (px + 320, py + 140))
            
            subtotal = ui.total_earnings - daily_quota - gas_expense
            screen.blit(assets.medium_font.render(f" {subtotal}", True, text_col), (px + 300, py + 168))
            
            final_col = (20, 120, 20) if take_home > 0 else (180, 0, 0)
            screen.blit(assets.medium_font.render(f" {take_home}", True, final_col), (px + 310, py + 214))
            
            # 5. HINT TEXT
            hint_f = pygame.font.SysFont("arial", 18, bold=True)
            hint_s = hint_f.render("Press anywhere to back to main menu", True, (255, 255, 255))
            screen.blit(hint_s, ((width - hint_s.get_width()) // 2, height - 40))
            
            # 6. BEAT FLASH
            if abs(math.sin(ui.win_anim_counter)) > 0.9:
                flash = pygame.Surface((width, height))
                flash.set_alpha(40)
                flash.fill((255, 255, 255))
                screen.blit(flash, (0,0))

    # ======================================================
    # L O S E / G L I T C H   S Y S T E M
    # ======================================================
    if ui.show_lose_panel:
        # 1. SHAKE OFFSET
        shake_offset_x, shake_offset_y = camera.get_glitch_shake_offset()
        
        # 2. Background Blur
        ret, frame = assets.blurdbg_vid.read()
        if not ret:
            assets.blurdbg_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = assets.blurdbg_vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width, height))
        bg_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        
        # 3. DRAW BACKGROUND WITH SHAKE
        screen.blit(bg_surface, (shake_offset_x, shake_offset_y))
        
        # 4. GLITCH EFFECT (RGB SPLIT)
        if random.randint(0, 5) == 0:
            glitch_surf = bg_surface.copy()
            glitch_surf.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
            glitch_surf.set_alpha(120)
            screen.blit(glitch_surf, (shake_offset_x + 15, shake_offset_y))
            
        # 5. DARK OVERLAY
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((20, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))
        
        # 6. DRAW LOSE PANEL WITH SHAKE
        l_rect = assets.lose_panel.get_rect(center=(width // 2 + shake_offset_x, height // 2 + shake_offset_y))
        screen.blit(assets.lose_panel, l_rect)
        
        # 7. ADD STATIC NOISE 
        if random.randint(0, 3) == 0:
            for _ in range(20):
                noise_y = random.randint(0, height)
                pygame.draw.line(screen, (200, 200, 200), (0, noise_y), (width, noise_y), 1)
                
        # 8. Hint Text (Press anywhere to back)
        hint_f = pygame.font.SysFont("arial", 18, bold=True)
        hint_s = hint_f.render("Press anywhere to back to main menu", True, (255, 100, 100))
        screen.blit(hint_s, ((width - hint_s.get_width()) // 2 + shake_offset_x, height - 40))
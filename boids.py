import pygame
from Environment.env_1 import Env1
from Environment.env_2 import Env2

pygame.init()
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

env = Env2(WIDTH, HEIGHT)
env.populate_environment()

# For Victors Test
env.create_target()

# button layout
FONT = pygame.font.SysFont(None, 24)
BTN_W, BTN_H, M = 140, 30, 10
align_btn    = pygame.Rect(M, M, BTN_W, BTN_H)
cohesion_btn = pygame.Rect(M, M+BTN_H+M, BTN_W, BTN_H)
separ_btn    = pygame.Rect(M, M+2*(BTN_H+M), BTN_W, BTN_H)
target_btn = pygame.Rect(M, M + 3*(BTN_H + M), BTN_W, BTN_H)
obstacle_btn = pygame.Rect(M, M + 4*(BTN_H + M), BTN_W, BTN_H)  
clear_obs_btn = pygame.Rect(M, M + 5*(BTN_H + M), BTN_W, BTN_H)

def draw_button(rect, text, active):
    col = (  0,200,  0) if active else (200,  0,  0)
    pygame.draw.rect(screen, col, rect)
    lbl = FONT.render(text, True, (255,255,255))
    screen.blit(lbl, lbl.get_rect(center=rect.center))

def draw_round_button(rect, text, active):
    col = (  0,120,  0) if active else (120,  0,  0)       
    pygame.draw.rect(screen, col, rect, border_radius=12)  
    pygame.draw.rect(screen, (255,255,255), rect, width=2, border_radius=12)
    lbl = FONT.render(text, True, (255,255,255))
    screen.blit(lbl, lbl.get_rect(center=rect.center))

running = True
start_time = pygame.time.get_ticks()
time_list = []
target_pos = []
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            x,y = ev.pos
            if   align_btn.collidepoint(x,y):
                env.use_alignment = not env.use_alignment
            elif cohesion_btn.collidepoint(x,y):
                env.use_cohesion  = not env.use_cohesion
            elif separ_btn.collidepoint(x,y):
                env.use_separation = not env.use_separation
            elif target_btn.collidepoint(x, y):
                env.use_targets = not env.use_targets           
                if env.use_targets:
                    env.create_target()                        
                else:
                    env.clear_targets()                         
            elif obstacle_btn.collidepoint(x, y):
                env.create_random_obstacle()            
            elif clear_obs_btn.collidepoint(x, y):
                env.clear_obstacles()
            else:
                env.add_bird(x, y)
    
    
    env.update_birds_in_target()
    if env.check_birds_in_target() == True:
        print(pygame.time.get_ticks() - start_time)
        time_list.append(pygame.time.get_ticks() - start_time)
        start_time = pygame.time.get_ticks()
        target_pos.append(env.targets[0][0])
        env.clear_targets()
        env.clear_birds_target()
        env.create_target()
        

    # update & draw flock
    env.update()
    env.render()

    # overlay buttons
    draw_button(separ_btn,    "Separation", env.use_separation)
    draw_button(align_btn,    "Alignment",  env.use_alignment)
    draw_button(cohesion_btn, "Cohesion",   env.use_cohesion)
    draw_round_button(target_btn, "Enable targets", env.use_targets)
    draw_round_button(obstacle_btn, "Add obstacle", True)
    draw_round_button(clear_obs_btn, "Clear obstacles", True)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print(time_list)
print([[x, y] for x, y in target_pos])
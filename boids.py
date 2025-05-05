# boids.py
import pygame
from Environment.env_1 import Env1
from Environment.env_2 import Env2

pygame.init()
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

env = Env2(WIDTH, HEIGHT)
env.populate_environment()

# button layout
FONT = pygame.font.SysFont(None, 24)
BTN_W, BTN_H, M = 140, 30, 10
align_btn    = pygame.Rect(M, M, BTN_W, BTN_H)
cohesion_btn = pygame.Rect(M, M+BTN_H+M, BTN_W, BTN_H)
separ_btn    = pygame.Rect(M, M+2*(BTN_H+M), BTN_W, BTN_H)

def draw_button(rect, text, active):
    col = (  0,200,  0) if active else (200,  0,  0)
    pygame.draw.rect(screen, col, rect)
    lbl = FONT.render(text, True, (255,255,255))
    screen.blit(lbl, lbl.get_rect(center=rect.center))

running = True
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

    # update & draw flock
    env.update()
    env.render()

    # overlay buttons
    draw_button(separ_btn,    "Separation", env.use_separation)
    draw_button(align_btn,    "Alignment",  env.use_alignment)
    draw_button(cohesion_btn, "Cohesion",   env.use_cohesion)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

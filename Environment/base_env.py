# Environment/base_env.py
import pygame, random
from Animats.bird import Bird

NUM_BIRDS = 30

class BaseEnvironment:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boids with Toggles")

        # Flocking toggles (default True)
        self.use_alignment  = True
        self.use_cohesion   = True
        self.use_separation = True

        # create birds
        self.birds = []
    def populate_environment(self):
        for _ in range(NUM_BIRDS):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.birds.append(Bird(x, y))

    def update(self):
        for b in self.birds:
            # apply only the rules that are switched on
            if self.use_alignment:
                b.apply_force( b.alignment(self.birds) )
            if self.use_cohesion:
                b.apply_force( b.cohesion(self.birds) )
            if self.use_separation:
                b.apply_force( b.separation(self.birds) )
            b.update()
            # wrap‐around
            b.position.x %= self.width
            b.position.y %= self.height

    def render(self):
        self.screen.fill((0,0,0))
        for b in self.birds:
            b.draw(self.screen)

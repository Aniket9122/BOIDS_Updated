import pygame, random
from Animats.bird import Bird

NUM_BIRDS = 30

class BaseEnvironment:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.birds  = []
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Boids Environment')

    def populate_environment(self):
        for _ in range(NUM_BIRDS):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.birds.append(Bird(x, y))

    def update(self):
        for bird in self.birds:
            bird.flock(self.birds)
            bird.update()
            # wrap‐around boundaries
            bird.position.x %= self.width
            bird.position.y %= self.height

    def render(self):
        self.screen.fill((0, 0, 0))
        for bird in self.birds:
            bird.draw(self.screen)
        pygame.display.flip()

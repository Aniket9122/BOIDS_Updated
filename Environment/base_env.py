import pygame, random
from Animats.bird import Bird

NUM_BIRDS = 30

class BaseEnvironment:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.birds  = []
        self.obstacles = []
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Boids Environment')

    def populate_environment(self):
        for _ in range(NUM_BIRDS):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.birds.append(Bird(x, y))
            
    def create_obstacle(self, shape, **kwargs):
        """
        Add an obstacle to the world.
        shape: 'rectangle' or 'circle'
        kwargs for rectangle: x, y, width, height, (optional) color
        kwargs for circle:    x, y, radius,    (optional) color
        """
        color = kwargs.get('color', (255, 255, 255))
        if shape == 'rectangle':
            rect = pygame.Rect(kwargs['x'], kwargs['y'],
                               kwargs['width'], kwargs['height'])
            self.obstacles.append(('rect', rect, color))
        elif shape == 'circle':
            center = (int(kwargs['x']), int(kwargs['y']))
            radius = int(kwargs['radius'])
            self.obstacles.append(('circle', center, radius, color))
        else:
            raise ValueError(f"Unknown shape: {shape}")

    def update(self):
        for bird in self.birds:
            bird.flock(self.birds)
            bird.update()
            # wrap‐around boundaries
            bird.position.x %= self.width
            bird.position.y %= self.height

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Draw obstacles
        for obs in self.obstacles:
            if obs[0] == 'rect':
                _, rect, color = obs
                pygame.draw.rect(self.screen, color, rect)
            elif obs[0] == 'circle':
                _, center, radius, color = obs
                pygame.draw.circle(self.screen, color, center, radius)
        
        # Draw birds
        for bird in self.birds:
            bird.draw(self.screen)
        pygame.display.flip()

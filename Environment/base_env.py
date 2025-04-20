# Environment/base_env.py
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
    
    def add_bird(self, x, y):
        """Spawn a new bird at the given screen coordinates."""
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
        
    def _resolve_collision(self, bird):
        """
        Prevent birds from entering obstacles by clamping them to the surface
        and removing the velocity component into the obstacle (no reflection).
        """
        for obs in self.obstacles:
            if obs[0] == 'rect':
                _, rect, _ = obs
                if rect.collidepoint(bird.position):
                    # distances to each side
                    d_left   = bird.position.x - rect.left
                    d_right  = rect.right - bird.position.x
                    d_top    = bird.position.y - rect.top
                    d_bottom = rect.bottom - bird.position.y
                    min_pen = min(d_left, d_right, d_top, d_bottom)

                    if min_pen == d_left:
                        bird.position.x = rect.left
                        if bird.velocity.x < 0:
                            bird.velocity.x = 0
                    elif min_pen == d_right:
                        bird.position.x = rect.right
                        if bird.velocity.x > 0:
                            bird.velocity.x = 0
                    elif min_pen == d_top:
                        bird.position.y = rect.top
                        if bird.velocity.y < 0:
                            bird.velocity.y = 0
                    else:  # bottom
                        bird.position.y = rect.bottom
                        if bird.velocity.y > 0:
                            bird.velocity.y = 0

            elif obs[0] == 'circle':
                _, center, radius, _ = obs
                center_v = pygame.Vector2(center)
                to_bird  = bird.position - center_v
                dist     = to_bird.length()

                if dist < radius:
                    # compute outward normal
                    normal = (to_bird / dist) if dist != 0 else pygame.Vector2(1, 0)
                    # clamp position to rim
                    bird.position = center_v + normal * radius
                    # remove only the inward (negative) velocity component
                    vn = bird.velocity.dot(normal)
                    if vn < 0:
                        bird.velocity -= normal * vn


    def update(self):
        for b in self.birds:
            # apply only the rules that are switched on
            if self.use_alignment:
                b.apply_force( b.alignment(self.birds) )
            if self.use_cohesion:
                b.apply_force( b.cohesion(self.birds) )
            if self.use_separation:
                b.apply_force( b.separation(self.birds) )
            # apply force to prevent obstacle collisions
            obs_force = b.avoid_obstacles(self.obstacles)
            b.apply_force(obs_force)
            b.apply_force(b.avoid_obstacles(self.obstacles))
            b.update()
            # wrap‐around
            b.position.x %= self.width
            b.position.y %= self.height
            # prevent obstacle pass through
            self._resolve_collision(b)

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

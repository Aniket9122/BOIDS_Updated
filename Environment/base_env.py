# Environment/base_env.py
import pygame, random, math
from Animats.bird import Bird

NUM_BIRDS = 50
TARGET_X = 0
TARGET_Y = 0
RESPAWN_DIST = 200
TIME_BUCKETS = [5, 10, 15, 20, 25, 30]          # seconds

class BaseEnvironment:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.birds  = []
        self.obstacles = []
        self.use_targets = True          # GUI toggle – default OFF
        self.targets = []
        # ── metrics for each target ────────────────────────────────
        self.initial_target_time = 0
        self.current_counts    = {}   # {1:0,3:0,…}
        self.all_metrics       = []      # list of dicts, one per target

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
        
    # def create_target(self, radius=80, color=(0, 255, 0)):
    #     # Create random spawning of target
    #     x = random.uniform(radius, self.width - radius)
    #     y = random.uniform(radius, self.height - radius)
        
    #     self.targets.append((pygame.Vector2(x, y), radius, color))
    
    def create_target(self, radius=80, color=(0, 255, 0), max_tries=1000):
        self.current_counts  = {t: 0 for t in TIME_BUCKETS}
        self.initial_target_time = pygame.time.get_ticks()
        for _ in range(max_tries):
            x = random.uniform(radius, self.width  - radius)
            y = random.uniform(radius, self.height - radius)
            pos = pygame.Vector2(x, y)
            # ----- check against every obstacle --------------------
            clear = True
            for obs in self.obstacles:
                if obs[0] == 'rect':
                    _, rect, _ = obs
                    # inflate rect by target radius and test point‑inside
                    if rect.inflate(radius * 2, radius * 2).collidepoint(pos):
                        clear = False
                        break
                elif obs[0] == 'circle':
                    _, centre, r_obs, _ = obs
                    if pos.distance_to(pygame.Vector2(centre)) < r_obs + radius:
                        clear = False
                        break
            if clear:
                self.targets.append((pos, radius, color))
                return

    def clear_targets(self):
        """Remove all current targets (called when the toggle is switched off)."""
        self.targets.clear()

    def create_random_obstacle(self):
        """
        Spawn ONE random obstacle (rectangle or circle) that fits
        entirely on‑screen.  Size and colour are picked from sensible
        ranges so the birds can still find a path around them.
        """
        # 50 % chance rectangle vs. circle
        if random.random() < 0.5:
            w  = random.randint(80, 200)
            h  = random.randint(80, 200)
            x  = random.randint(0,  self.width  - w)
            y  = random.randint(0,  self.height - h)
            col = (random.randint(100,255), 50, 50)  # reddish tone
            self.create_obstacle(
                'rectangle',
                x=x, y=y, width=w, height=h, color=col
            )
        else:
            r  = random.randint(40, 120)
            x  = random.randint(r, self.width  - r)
            y  = random.randint(r, self.height - r)
            col = (50, 50, random.randint(100,255))  # bluish tone
            self.create_obstacle(
                'circle',
                x=x, y=y, radius=r, color=col
            )
    
        # ───────────────────────────── clear ─────────────────────────────
    def clear_obstacles(self):
        """Remove all obstacles currently in the scene."""
        self.obstacles.clear()

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

    def check_birds_in_target(self):
        counter = 0
        for b in self.birds:
            if b.target == True:
                counter += 1
        if counter > 0.8 * len(self.birds):
            return True
        else:
            return False
    
    def update_birds_in_target(self):
        for t in self.targets:
            for b in self.birds:
                dx = b.position.x - t[0].x
                dy = b.position.y - t[0].y
                distance = math.hypot(dx, dy)
                if distance <= t[1]:
                    b.target = True
                    b.target_time = pygame.time.get_ticks()
    
    def time_to_target(self):
        for b in self.birds:
            time = 0
            if b.target == True:
                time = (b.target_time - self.initial_target_time) / 1000
                print(time, self.initial_target_time)
                for t in TIME_BUCKETS:
                    if time <= t:
                        self.current_counts[t] += 1
                        break
        self.all_metrics.append(self.current_counts.copy())

    def clear_birds_target(self):
        for b in self.birds:
            b.target = False

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
            #obs_force = b.avoid_obstacles(self.obstacles)
            #b.apply_force(obs_force)
            #b.apply_force(b.avoid_obstacles(self.obstacles))
            #b.update()
            # wrap‐around
            b.position.x %= self.width
            b.position.y %= self.height
            # prevent obstacle pass through
            self._resolve_collision(b)
            b.apply_force(b.avoid_obstacles(self.obstacles))
            # ── only when toggle is ON ───────────────────────────────────────
            if self.use_targets and self.targets:
                b.apply_force(b.seek_target(self.targets))
            # physics integration + housekeeping
            b.update()
            b.position.x %= self.width
            b.position.y %= self.height
            #self._resolve_collision(b)

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
        
        # Draw targets
        for target, radius, color in self.targets:
            pygame.draw.circle(self.screen, color, (int(target.x), int(target.y)), radius, width=2)


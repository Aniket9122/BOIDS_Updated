import pygame
import random

class Bird:
    def __init__(self, x, y):
        # Position, random initial velocity, and physics
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2),
                                       random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4     
        self.max_force = 0.1    
        self.perception = 50    # perception radius
        self.target = False # checks whether the bird has reached the target
        self.target_time = 0 # time when the bird reached the target

    def apply_force(self, force):
        """Accumulate steering force into acceleration."""
        self.acceleration += force

    def alignment(self, boids):
        """
        Steer towards average heading of local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception:
                    steering += other.velocity
                    total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, boids):
        """
        Steer towards average position of local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception:
                    steering += other.position
                    total += 1
        if total > 0:
            steering /= total
            steering = (steering - self.position)
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separation(self, boids):
        """
        Steer to avoid crowding local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception and distance > 0:
                    diff = (self.position - other.position) / distance
                    steering += diff
                    total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def avoid_obstacles(self, obstacles):
        """
        Steer away from nearby obstacles.
        obstacles: list of tuples as defined in BaseEnvironment.obstacles
        """
        steer = pygame.Vector2(0, 0)
        total = 0

        for obs in obstacles:
            if obs[0] == 'rect':
                _, rect, _ = obs
                # closest point on rect to bird
                cx = max(rect.left,   min(self.position.x, rect.right))
                cy = max(rect.top,    min(self.position.y, rect.bottom))
                diff = self.position - pygame.Vector2(cx, cy)
                dist = diff.length()
                if 0 < dist < self.perception:
                    diff.normalize_ip()
                    steer += diff / dist
                    total += 1

            elif obs[0] == 'circle':
                _, center, radius, _ = obs
                diff = self.position - pygame.Vector2(center)
                dist = diff.length() - radius
                if 0 < dist < self.perception:
                    diff.normalize_ip()
                    steer += diff / dist
                    total += 1

        if total > 0:
            steer /= total
            steer.scale_to_length(self.max_speed)
            steer -= self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)

        return steer

    def flock(self, boids):
        """
        Calculate and apply steering from alignment, cohesion, and separation.
        """
        alignment_weight = 0.4
        cohesion_weight = 0.4
        separation_weight = 5
        
        align_force = self.alignment(boids) * alignment_weight
        coh_force   = self.cohesion(boids) * cohesion_weight
        sep_force   = self.separation(boids) * separation_weight

        self.apply_force(align_force)
        self.apply_force(coh_force)
        self.apply_force(sep_force)

    def seek_target(self, targets):
        """
        Return a steering force that guides the bird toward the nearest
        target centre but switches off once the bird is *inside* the
        target circle.

        targets: list of tuples  (Vector2 centre, radius, color)
        """
        if not targets:
            return pygame.Vector2(0, 0)

        # —— pick the closest target (centre‑to‑rim distance) ——————
        nearest_c   = None
        nearest_rad = 0
        min_dist    = float("inf")

        for centre, radius, _ in targets:
            dist = self.position.distance_to(centre) - radius
            if dist < min_dist:
                min_dist, nearest_c, nearest_rad = dist, centre, radius

        # —— already inside the circle?  no extra steering ————
        if min_dist <= 0:
            return pygame.Vector2(0, 0)

        # —— classic “seek” behaviour ————————————————
        desired = (nearest_c - self.position).normalize() * self.max_speed
        steer   = desired - self.velocity
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer * 0.3


    def update(self):
        """Integrate acceleration into velocity and position."""
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, screen):
        """Draw the bird as a triangle pointing in direction of its velocity."""
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        head  = self.position + pygame.Vector2(10, 0).rotate(-angle)
        left  = self.position + pygame.Vector2(-5, 5).rotate(-angle)
        right = self.position + pygame.Vector2(-5, -5).rotate(-angle)
        pygame.draw.polygon(screen, (255, 255, 255), [head, left, right])
 
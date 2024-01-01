import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, acceleration, lifespan):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.acceleration = pygame.math.Vector2(acceleration)
        self.lifespan = lifespan

    def update(self):
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.lifespan -= 1

        if self.lifespan <= 0:
            self.kill()
            
class ParticleEngine:
    def __init__(self):
        self.particles = pygame.sprite.Group()

    def generate_particles(self, num_particles, pos):
        for _ in range(num_particles):
            particle = Particle(pos, (0, 0), (0, 0.1), 100)
            self.particles.add(particle)

    def update_particles(self):
        self.particles.update()

    def draw_particles(self, surface):
        self.particles.draw(surface)


class Fireworks:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-15, -5)
        self.gravity = 0.5
    
    def update(self):
        self.vx *= 0.98
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


def explode(x, y):
    particles = []
    for _ in range(100):
        color = random.choice([RED, YELLOW, ORANGE, GREEN, BLUE, PURPLE])
        particle = Fireworks(x, y, color)
        particles.append(particle)
    
    return particles


if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Smoky Effect")
    particle_engine = ParticleEngine()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        if pygame.mouse.get_pressed()[0]:
            particle_engine.generate_particles(10, pygame.mouse.get_pos())
            # mx, my = pygame.mouse.get_pos()
            # particles = explode(mx, my)
            # for particle in particles:
            #     particle.update()
            #     particle.draw(screen)
        # 生成粒子
        particle_engine.generate_particles(10, pygame.mouse.get_pos())
        # 更新粒子
        particle_engine.update_particles()
        # 绘制粒子
        particle_engine.draw_particles(screen)
        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)
    # 退出PyGame
    pygame.quit()

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
    """
    A class to represent a particle in the game.

    Attributes
    ----------
    pos : pygame.math.Vector2
        The position of the particle.
    velocity : pygame.math.Vector2
        The velocity of the particle.
    acceleration : pygame.math.Vector2
        The acceleration of the particle.
    lifespan : int
        The lifespan of the particle.

    Methods
    -------
    update():
        Updates the particle's position, velocity, and lifespan.
        If the lifespan reaches zero, the particle is killed.
    """

    def __init__(self, pos, velocity, acceleration, lifespan):
        """
        Constructs all the necessary attributes for the Particle object.

        Parameters
        ----------
        pos : tuple
            The initial position of the particle as a tuple (x, y).
        velocity : tuple
            The initial velocity of the particle as a tuple (vx, vy).
        acceleration : tuple
            The acceleration of the particle as a tuple (ax, ay).
        lifespan : int
            The lifespan of the particle.
        """
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.acceleration = pygame.math.Vector2(acceleration)
        self.lifespan = lifespan

    def update(self):
        """
        Updates the particle's position, velocity, and lifespan.
        If the lifespan reaches zero, the particle is killed.
        """
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.lifespan -= 1

        if self.lifespan <= 0:
            self.kill()
            
class ParticleEngine:
    """
    A class to manage and control a group of particles.

    Attributes
    ----------
    particles : pygame.sprite.Group
        A group of particles.

    Methods
    -------
    generate_particles(num_particles, pos):
        Generates a specified number of particles at a given position.
    update_particles():
        Updates the state of all particles in the group.
    draw_particles(surface):
        Draws all particles in the group to a given surface.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the ParticleEngine object.
        """
        self.particles = pygame.sprite.Group()

    def generate_particles(self, num_particles, pos):
        """
        Generates a specified number of particles at a given position.

        Parameters
        ----------
        num_particles : int
            The number of particles to generate.
        pos : tuple
            The position at which to generate the particles as a tuple (x, y).
        """
        for _ in range(num_particles):
            particle = Particle(pos, (0, 0), (0, 0.1), 100)
            self.particles.add(particle)

    def update_particles(self):
        """
        Updates the state of all particles in the group.
        """
        self.particles.update()

    def draw_particles(self, surface):
        """
        Draws all particles in the group to a given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the particles on.
        """
        self.particles.draw(surface)


class Fireworks:
    """
    A class to represent a fireworks particle.

    Attributes
    ----------
    x : float
        The x-coordinate of the particle.
    y : float
        The y-coordinate of the particle.
    color : tuple
        The color of the particle.
    radius : int
        The radius of the particle.
    vx : float
        The x-component of the velocity of the particle.
    vy : float
        The y-component of the velocity of the particle.
    gravity : float
        The acceleration due to gravity.

    Methods
    -------
    update():
        Updates the position and velocity of the particle.
    draw(surface):
        Draws the particle to a given surface.
    """

    def __init__(self, x, y, color):
        """
        Constructs all the necessary attributes for the Fireworks object.

        Parameters
        ----------
        x : float
            The initial x-coordinate of the particle.
        y : float
            The initial y-coordinate of the particle.
        color : tuple
            The color of the particle.
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-15, -5)
        self.gravity = 0.5

    def update(self):
        """
        Updates the position and velocity of the particle.
        """
        self.vx *= 0.98
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        """
        Draws the particle to a given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the particle on.
        """
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


def explode(x, y):
    """
    This function generates a list of Fireworks objects (particles) that explode at a given position.

    Parameters:
    x (float): The x-coordinate of the explosion position.
    y (float): The y-coordinate of the explosion position.

    Returns:
    list: A list of Fireworks objects representing the explosion particles.

    """
    particles = []
    for _ in range(100):
        # Randomly choose a color for the particle
        color = random.choice([RED, YELLOW, ORANGE, GREEN, BLUE, PURPLE])
        # Create a new Fireworks object with the chosen color and position
        particle = Fireworks(x, y, color)
        # Add the particle to the list
        particles.append(particle)

    # Return the list of particles
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

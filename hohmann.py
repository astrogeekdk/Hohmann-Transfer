import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

SUN_MASS = 2e30
EARTH_MASS = 5.97e24
MARS_MASS = 6.39e23

G = 6.67e-11

SPACECRAFT_MASS = 10e3

scale = 1e-9

SUN_EARTH_DIST = 150e9
SUN_MARS_DIST = 228e9

MARS_ORB_V = 24000
EARTH_ORB_V = 30000

class Planet:
    def __init__(self, dist_from_sun, mass, orb_v):
        self.dist_from_sun = dist_from_sun
        self.mass = mass
        self.orb_v = orb_v

center = pygame.Vector2(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

SUN_POS = pygame.Vector2(center.x, center.y)
Earth = Planet(SUN_EARTH_DIST, EARTH_MASS, EARTH_ORB_V)
Mars = Planet(SUN_MARS_DIST, MARS_MASS, MARS_ORB_V)
        
Earth.position = pygame.Vector2(center.x+SUN_EARTH_DIST, center.y)
Earth.v = pygame.Vector2(0, Earth.orb_v)

Mars.position = pygame.Vector2(center.x+SUN_MARS_DIST,center.y)
Mars.v = pygame.Vector2(0, Mars.orb_v)


planets = [Earth, Mars]

dt = 10000

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill("black")


    pygame.draw.circle(screen, (255,255,0), center, 10)

    for i in range(len(planets)):
        force = G*planets[i].mass*SUN_MASS/(SUN_POS-planets[i].position).length_squared()
        force_direction = (SUN_POS-planets[i].position).normalize()
        a = force/planets[i].mass*force_direction
        planets[i].v += a*dt
        planets[i].position += planets[i].v* dt


        
    pygame.draw.circle(screen, (255,0,0), (center.x+Earth.position.x*scale, center.y+Earth.position.y*scale), 2)
    pygame.draw.circle(screen, (0,255,0), (center.x+Mars.position.x*scale, center.y+Mars.position.y*scale), 2)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
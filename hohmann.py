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

scale = 1e-9

SUN_EARTH_DIST = 150e9
SUN_MARS_DIST = 228e9

MARS_ORB_V = 24200
EARTH_ORB_V = 29800

class Planet:
    def __init__(self, dist_from_sun, mass, orb_v):
        self.dist_from_sun = dist_from_sun
        self.mass = mass
        self.orb_v = orb_v

class Spacecraft:
    def __init__(self, dist, mass, initial_v):
        self.dist = dist
        self.mass = mass
        self.initial_v = initial_v

center = pygame.Vector2(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

SUN_POS = pygame.Vector2(center.x, center.y)

Earth = Planet(SUN_EARTH_DIST, EARTH_MASS, EARTH_ORB_V)
Mars = Planet(SUN_MARS_DIST, MARS_MASS, MARS_ORB_V)
        
Earth.position = pygame.Vector2(center.x+SUN_EARTH_DIST, center.y)
Earth.v = pygame.Vector2(0, Earth.orb_v)

Mars.position = pygame.Vector2(center.x+SUN_MARS_DIST,center.y)
Mars.v = pygame.Vector2(0, Mars.orb_v)


planets = [Earth, Mars]


delv1 = (G*SUN_MASS/SUN_EARTH_DIST)**0.5*((2*SUN_MARS_DIST/(SUN_EARTH_DIST+SUN_MARS_DIST))**0.5-1)

spacecraft = Spacecraft(0, 10e3, 7e3)
spacecraft.v = pygame.Vector2(0, EARTH_ORB_V+delv1)
spacecraft.position = Earth.position + pygame.Vector2(spacecraft.dist, 0)
print(delv1)

dt = 100000 


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # screen.fill("black")

    pygame.draw.circle(screen, (255,255,0), center, 10)

    for i in range(len(planets)):
        force = G*planets[i].mass*SUN_MASS/(SUN_POS-planets[i].position).length_squared()
        force_direction = (SUN_POS-planets[i].position).normalize()
        a = force/planets[i].mass*force_direction
        planets[i].v += a*dt
        planets[i].position += planets[i].v* dt

    force = (G*spacecraft.mass*Earth.mass/(Earth.position-spacecraft.position).length()**2)*(Earth.position-spacecraft.position).normalize()
    force += (G*spacecraft.mass*SUN_MASS/(SUN_POS-spacecraft.position).length()**2)*(SUN_POS-spacecraft.position).normalize()
    force += (G*spacecraft.mass*Mars.mass/(Mars.position-spacecraft.position).length()**2)*(Mars.position-spacecraft.position).normalize()
    a = force/spacecraft.mass
    spacecraft.v += a*dt
    spacecraft.position += spacecraft.v * dt



        
    pygame.draw.circle(screen, (0,255,0), (center.x+Earth.position.x*scale, center.y+Earth.position.y*scale), 2)
    pygame.draw.circle(screen, (255,0,0), (center.x+Mars.position.x*scale, center.y+Mars.position.y*scale), 2)
    pygame.draw.circle(screen, (255,255,255), (center.x+spacecraft.position.x*scale, center.y+spacecraft.position.y*scale), 2)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
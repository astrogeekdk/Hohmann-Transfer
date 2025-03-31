import pygame
from skyfield.api import load
import numpy as np

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


planets = load('de421.bsp')
sun, earth, mars = planets['SUN'], planets['EARTH BARYCENTER'], planets['MARS BARYCENTER']
ts = load.timescale()
t = ts.now()


earth_position = earth.at(t).position.m
earth_velocity = earth.at(t).velocity.m_per_s

mars_position = mars.at(t).position.m
mars_velocity = mars.at(t).velocity.m_per_s

sun_position = sun.at(t).position.m
sun_position = pygame.Vector3(sun_position[0], sun_position[1], sun_position[2])


class Planet:
    def __init__(self, mass, v, position):
        self.mass = mass
        self.v = pygame.Vector3(v[0], v[1], v[2])
        self.position = pygame.Vector3(position[0], position[1], position[2])

class Spacecraft:
    def __init__(self, mass, v, position):
        self.mass = mass
        self.v = pygame.Vector3(v[0], v[1], v[2])
        self.position = pygame.Vector3(position[0], position[1], position[2])


center = pygame.Vector2(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

Earth = Planet(EARTH_MASS, earth_velocity, earth_position)
Mars = Planet(MARS_MASS, mars_velocity, mars_position)


planets = [Earth, Mars]


mu = G*SUN_MASS
r1 = np.linalg.norm(sun_position - earth_position)
r2 = np.linalg.norm(sun_position - mars_position)

del_v1 = (mu/r1)**0.5 * ((2*r2/(r1+r2))**0.5 - 1)

time_hohmann = np.pi * ((r1+r2)**3/(8*mu))**0.5

r_vec = earth_position - sun_position
v_dir = np.cross(r_vec, [0,0,1])
v_dir = v_dir / np.linalg.norm(v_dir)

# print(v_dir, Earth.v.normalize())

spacecraft = Spacecraft(10e3, Earth.v + v_dir*del_v1, Earth.position)

t = 0
dt = 10000

mode = "XY"

frame = 0

while running:

    t+=dt
    print(t/86400)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "XY"
                screen.fill("black")
            if event.key == pygame.K_2:
                mode = "YZ"
                screen.fill("black")
            if event.key == pygame.K_3:
                mode = "XZ"
                screen.fill("black")
            # if event.key == pygame.K_SPACE:
            #     spacecraft = Spacecraft(10e3, Earth.v+Earth.v.normalize()*2100, Earth.position)


    # screen.fill("black")

    pygame.draw.circle(screen, (255,255,0), center, 10)

    for i in range(len(planets)):
        force = G*planets[i].mass*SUN_MASS/(sun_position-planets[i].position).length_squared()
        force_direction = (sun_position-planets[i].position).normalize()
        a = force/planets[i].mass*force_direction
        planets[i].v += a*dt
        planets[i].position += planets[i].v* dt

        force = (G*spacecraft.mass*Earth.mass/(Earth.position-spacecraft.position).length()**2)*(Earth.position-spacecraft.position).normalize()
        force += (G*spacecraft.mass*SUN_MASS/(sun_position-spacecraft.position).length()**2)*(sun_position-spacecraft.position).normalize()
        force += (G*spacecraft.mass*Mars.mass/(Mars.position-spacecraft.position).length()**2)*(Mars.position-spacecraft.position).normalize()
        a = force/spacecraft.mass
        spacecraft.v += a*dt
        spacecraft.position += spacecraft.v * dt

    if mode=="XY":
        pygame.draw.circle(screen, (255,255,0), (center.x, center.y), 5)
        pygame.draw.circle(screen, (0,255,0), (center.x+Earth.position.x*scale, center.y+Earth.position.y*scale), 2)
        pygame.draw.circle(screen, (255,0,0), (center.x+Mars.position.x*scale, center.y+Mars.position.y*scale), 2)
        pygame.draw.circle(screen, (255,255,255), (center.x+spacecraft.position.x*scale, center.y+spacecraft.position.y*scale), 2)
        
    elif mode=="YZ":
        pygame.draw.circle(screen, (255,255,0), (center.x, center.y), 5)
        pygame.draw.circle(screen, (0,255,0), (center.x+Earth.position.y*scale, center.y+Earth.position.z*scale), 2)
        pygame.draw.circle(screen, (255,0,0), (center.x+Mars.position.y*scale, center.y+Mars.position.z*scale), 2)
        pygame.draw.circle(screen, (255,255,255), (center.x+spacecraft.position.y*scale, center.y+spacecraft.position.z*scale), 1)
    elif mode=="XZ":
        pygame.draw.circle(screen, (255,255,0), (center.x, center.y), 5)
        pygame.draw.circle(screen, (0,255,0), (center.x+Earth.position.x*scale, center.y+Earth.position.z*scale), 2)
        pygame.draw.circle(screen, (255,0,0), (center.x+Mars.position.x*scale, center.y+Mars.position.z*scale), 2)
        pygame.draw.circle(screen, (255,255,255), (center.x+spacecraft.position.x*scale, center.y+spacecraft.position.z*scale), 1)

    pygame.display.flip()

    clock.tick(100)

pygame.quit()
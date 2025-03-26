from skyfield.api import load
import numpy as np

planets = load('de421.bsp')

sun, earth, mars = planets['SUN'], planets['EARTH BARYCENTER'], planets['MARS BARYCENTER']

ts = load.timescale()
t = ts.now()

earth_position = earth.at(t).position.m
earth_velocity = earth.at(t).velocity.m_per_s
print(earth_position, earth_velocity)

mars_position = mars.at(t).position.m
mars_velocity = mars.at(t).velocity.m_per_s
print(mars_position, mars_velocity)

sun_position = sun.at(t).position.m
print(sun_position)
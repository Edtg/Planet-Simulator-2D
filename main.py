import pygame, math, numpy as np, json, os, random
from numpy import array
from pygame.constants import K_r
pygame.init()

size = width, height = 1920, 1080

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 20)
green = (0, 255, 0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Planet Simulator")

running = True
FPS = 60
clock = pygame.time.Clock()

bodies = []
#G = 0.0000000000674
G = 0.05

def SqrDistanceBetween(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

class Body(object):
    def __init__(self, mass, size, pos, vel):
        self.mass = mass
        self.size = size
        self.pos = pos
        self.vel = vel
        self.color = (random.randrange(30, 255), random.randrange(30, 255), random.randrange(30, 255))
    
    def Draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size)
    
    def UpdateVelocity(self, otherBody):
        sqrDist = SqrDistanceBetween(otherBody.pos, self.pos)
        forceDir = normalized(otherBody.pos - self.pos)
        force = forceDir * G * self.mass * otherBody.mass / sqrDist
        acceleration = force * self.mass
        self.vel += acceleration[0]
    
    def UpdatePosition(self):
        self.pos += self.vel / 10
    
    def DrawVelocity(self, surface):
        pygame.draw.line(surface, (255, 0, 0), self.pos, self.pos + (self.vel * 5))


sun = Body(400, 30, array([800.0, 500.0]), array([0.0, 0.0]))
bodies.append(Body(15, 14, array([500.0, 500.0]), array([0.0, 12.0])))
bodies.append(Body(22, 20, array([200.0, 500.0]), array([0.0, 12.0])))



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)

    sun.Draw(screen)

    for b in bodies:
        b.UpdateVelocity(sun)
        for b2 in bodies:
            if b != b2:
                b.UpdateVelocity(b2)
        b.UpdatePosition()
        b.Draw(screen)
        b.DrawVelocity(screen)
    

    pygame.display.update()
    clock.tick(FPS)



pygame.quit()
quit()
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

def GetAcceleration(body1, body2):
    sqrDist = SqrDistanceBetween(body2.pos, body1.pos)
    forceDir = normalized(body2.pos - body1.pos)
    force = forceDir * G * body1.mass * body2.mass / sqrDist
    acceleration = force * body1.mass
    return acceleration

class Body(object):
    def __init__(self, mass, size, pos, vel, color=(0,0,0)):
        self.mass = mass
        self.size = size
        self.pos = pos
        self.vel = vel
        if color == (0,0,0):
            self.color = (random.randrange(30, 255), random.randrange(30, 255), random.randrange(30, 255))
        else:
            self.color = color
    
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


sun = Body(400, 30, array([800.0, 500.0]), array([0.0, 0.0]), (255, 255, 0))
bodies.append(Body(15, 14, array([500.0, 500.0]), array([0.0, 12.0])))
bodies.append(Body(22, 20, array([200.0, 500.0]), array([0.0, 12.0])))


predictionBodies = []
predictionBodies.append(Body(15, 14, array([500.0, 500.0]), array([0.0, 12.0])))
predictionBodies.append(Body(22, 20, array([200.0, 500.0]), array([0.0, 12.0])))
predictionPoints = {}
seconds = 120

for pb in range(len(predictionBodies)):
    predictionPoints[pb] = []

print(predictionPoints)

for i in range(50 * seconds):
    for pb in range(len(predictionBodies)):
        predictionBodies[pb].UpdateVelocity(sun)
        for pb2 in predictionBodies:
            if predictionBodies[pb] != pb2:
                predictionBodies[pb].UpdateVelocity(pb2)
        predictionBodies[pb].UpdatePosition()
        predictionPoints[pb].append((predictionBodies[pb].pos[0], predictionBodies[pb].pos[1]))



# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)

    sun.Draw(screen)

    for p in range(len(predictionPoints)):
        #print(predictionPoints[p][0])
        for i in range(1, len(predictionPoints[p])):
            pygame.draw.line(screen, bodies[p].color, predictionPoints[p][i-1], predictionPoints[p][i])


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
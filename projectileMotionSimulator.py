from math import sin, cos, asin, atan, radians
from matplotlib import pyplot as plt
from numpy import arange

class Projectile:

    def __init__(self, v, angle):

        self.x = 0
        self.y = 0

        self.vx = v * cos(radians(angle))
        self.vy = v * sin(radians(angle))

        self.ax = 0
        self.ay = -9.8

        self.time = 0

        self.xarr = [self.x]
        self.yarr = [self.y]

    def updateVx(self, dt):
        self.vx = self.vx + self.ax * dt
        return self.vx

    def updateVy(self, dt):
        self.vy = self.vy + self.ay * dt
        return self.vy

    def updateX(self, dt):
        self.x = self.x + 0.5 * (self.vx + self.updateVx(dt)) * dt
        return self.x

    def updateY(self, dt):
        self.y = self.y + 0.5 * (self.vy + self.updateVy(dt)) * dt
        return self.y

    def step(self, dt):
        self.xarr.append(self.updateX(dt))
        self.yarr.append(self.updateY(dt))
        self.time += dt
    
def shot(v, angle):

    throw = Projectile(v, angle)
    dt = 0.01
    t = 0

    while throw.y >= 0:
        throw.step(dt)
        t += dt
    
    return throw.xarr, throw.yarr, t

def main(rng, pos):

    velocity = 15
    diff = 9999999
    if pos == 0:
        for ang in arange(1, 89.99, 0.01):
            x,y,t = shot(velocity, ang)
            if abs(rng-x[len(x)-1]) < diff:
                diff = abs(rng-x[len(x)-1])
                optAngle = ang
                optTime = t
                optx = x
                opty = y
    return optAngle, optTime, optx, opty

# print (main(20))
print (main(20,0))







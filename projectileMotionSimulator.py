from math import sin, cos, radians, inf, atan
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

    def updatevx(self, dt):
        self.vx = self.vx + self.ax * dt
        return self.vx

    def updatevy(self, dt):
        self.vy = self.vy + self.ay * dt
        return self.vy

    def updatex(self, dt):
        self.x = self.x + 0.5 * (self.vx + self.updatevx(dt)) * dt
        return self.x

    def updatey(self, dt):
        self.y = self.y + 0.5 * (self.vy + self.updatevy(dt)) * dt
        return self.y

    def step(self, dt):
        self.xarr.append(self.updatex(dt))
        self.yarr.append(self.updatey(dt))
        self.time += dt


def shot(v, angle, pos, range):
    throw = Projectile(v, angle)
    dt = 0.0005
    t = 0

    if pos == 0:
        while throw.y >= 0:
            throw.step(dt)
            t += dt
    else:
        while throw.x <= range:
            throw.step(dt)
            t += dt

    return throw.xarr, throw.yarr, t

def bruteForce(start, stop, rng, pos, v, neg = 1):
    global optTime, optAngle
    diff = inf
    for ang in arange(start, stop, neg * 0.02):
        x, y, t = shot(v, ang, pos, rng)
        if pos == 0:
            newDiff = abs(rng - x[len(x) - 1])
        else:
            newDiff = abs(pos-y[len(y)-1])
        if newDiff > diff:
            if diff > 0.1:
                return ValueError
            else:
                break
        if newDiff < diff:
            diff = newDiff
            optAngle = ang
            optTime = t
        
    return optAngle, optTime, x, y

def main(velocity, rng, pos):
    try:
        if pos == 0:
            optAngle, optTime, x, y = bruteForce(0.01, 90, rng, pos, velocity)
        elif pos > 0:
            optAngle, optTime, x, y = bruteForce(round(atan(pos/rng), 2), 90, rng, pos, velocity)
        else:
            optHorizAng = round(bruteForce(0.01, 90, rng, 0, velocity)[0], 2)
            optAngle, optTime, x, y = bruteForce(optHorizAng, round(atan(pos/rng), 2), rng, pos, velocity, -1)
    except:
        return -1

    return round(optAngle, 2), round(optTime, 2), x, y


if __name__ == "__main__":
    tgts = []
    tgtnum = int(input("How many targets are there to hit?"))
    velocity = int(input("Throwing speed?"))
    smallest = inf
    optTgt = 0
    plt.xlabel('X coordinate (m)')
    plt.ylabel('Y coordinate (m)')
    for i in range(tgtnum):
        rng = int(input("Horizontal displacement from target " + str(i + 1) + ":"))
        pos = int(input("Vertical displacement from target " + str(i+1) + ":"))
        print("Please wait a moment as I calculate the optimum angle and time to hit target....")
        data = main(velocity, rng, pos)
        if data != -1:
            plt.plot([0, rng], [0, 0], "k-")
            plt.plot(data[2], data[3], label = "Target " + str(i + 1))
            if data[1] < smallest:
                smallest = data[1]
                optTgt = i+1
            print("Throw at", data[0], "degrees to the horizontal to hit target", i + 1, ". This will take", data[1], "seconds to hit.")
            print("*********************************")
        else:
            print("Target impossible to hit")
    if optTgt != 0:
        print("Target", optTgt, "is your best bet.")
        plt.legend()
        plt.show()
    else:
        print("Sorry buddy, you can't hit your target")


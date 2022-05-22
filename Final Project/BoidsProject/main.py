from p5 import setup, draw, size, background, run
import p5
import numpy as np
import random
from boid import Boid
from boid import Predator


def random_generator():
    a = random.uniform(0, 0.5)
    b = random.uniform(0, 0.5)
    c = 1 - (a + b)
    return a, b, c


# Screen Settings.
WIDTH = 1000
HEIGHT = 1000

# Creating pack of birds at random location.
FLOCK_SIZE = 20
PREDATOR_SIZE = 2

flock = [Boid(*np.random.rand(2) * 1000, WIDTH, HEIGHT,random_generator()[0],random_generator()[1],random_generator()[2]) for i in range(FLOCK_SIZE)]
predators = [Predator(*np.random.rand(2) * 1000, WIDTH, HEIGHT) for j in range(PREDATOR_SIZE)]


# Initialize animation window.
def setup():
    size(WIDTH, HEIGHT)


def draw():
    background(51)  # Background color.
    iter_boid = 0
    iter_predator = 0
    for boid in flock:
        if boid.alive == True:
            iter_boid += 1

            boid.show()
            neighbour = boid.Neighbours(flock)

            boid.combine_steers(neighbour,iter_boid)
            boid.collusion(flock)
            boid.boundary()

            # if boid.birth(flock, iter_boid):
            #     flock.append(Boid(*np.random.rand(2) * 1000, WIDTH, HEIGHT,random_generator()[0],random_generator()[1],random_generator()[2]))
            boid.update(iter_boid)
        else:
            flock.remove(boid)

    for predator in predators:
        iter_predator += 1
        predator.boundary()
        predator.show()
        predator.eat(flock)
        predator.awareness_update(flock)
        predator.update(iter_predator)


run()
from p5 import setup, draw, size, background, run
import p5
import numpy as np
from boid import Boid

# Screen Settings.
WIDTH = 1000
HEIGHT = 1000

# Creating pack of birds at random location.
FLOCK_SIZE = 20
flock = [Boid(*np.random.rand(2)*1000, WIDTH, HEIGHT) for i in range(FLOCK_SIZE)]

#Initialize animation window.
def setup():
    size(WIDTH,HEIGHT)

def draw():
    background(51) # Background color.

    for boid in flock:
        boid.boundary()
        boid.show()
        boid.update()

run()

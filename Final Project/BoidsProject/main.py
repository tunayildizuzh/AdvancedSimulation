from p5 import setup, draw, size, background, run
import p5
import numpy as np
import time
import random
from boid import Boid
from boid import Predator



def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def random_generator():
    rng = np.random.default_rng()
    rng = np.random.default_rng()
    float1 = rng.random()
    float2 = rng.random()
    float3 = rng.random()
    data = np.array([float1, float2, float1])
    rand = softmax(data)

    return rand

def age(iter):

    if iter < 15:
        return 'green'
    else:
        return 'white'


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

AGE = 0
def draw():
    background(51)  # Background color.

    iter_boid = 0
    iter_predator = 0
    iter_color = 0
    for boid in flock:
        if boid.alive == True:

            iter_boid += 1
            iter_color +=1
            boid.show()
            neighbour = boid.Neighbours(flock)


            boid.combine_steers(neighbour,iter_boid)

            boid.collusion(flock)
            boid.boundary()
            if boid.age > 10:
                boid.color = 'white'
            #print(iter_count(iter_boid, 10,AGE))
            if boid.birth(flock, iter_boid,np.random.randint(0,2)):
                new_bird = Boid(*np.random.rand(2) * 1000, WIDTH, HEIGHT,random_generator()[0],random_generator()[1],random_generator()[2])
                new_bird.color = 'green'
            # if boid.age > 10:
            #     new_bird.color = 'white'



                # if new_bird.age < 5:            # FIX AGE.
                #     new_bird.color = 'green'
                # else:
                #     new_bird.color = 'white'
                flock.append(new_bird)

            boid.update(iter_boid)
        else:
            flock.remove(boid)

    for predator in predators:  # PREDATOR COUNT INCREASE.
        iter_predator += 1
        predator.boundary()
        predator.show()
        predator.eat(flock)
        predator.awareness_update(flock)
        predator.update(iter_predator)
        if len(flock) > FLOCK_SIZE and len(flock) % 10 == 0:
            predators.append(Predator(*np.random.rand(2) * 1000, WIDTH, HEIGHT))


run()
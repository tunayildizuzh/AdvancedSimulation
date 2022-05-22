import numpy as np
from p5 import setup, draw, size, background, run, Vector, stroke, triangle, color, fill, circle
import random

K = 1
S = 1
M = 1

COEF_ADJUST = 10

class Boid():

    def __init__(self, x, y, WIDTH, HEIGHT, align_coef, separation_coef, cohesion_coef):
        self.position = Vector(x, y)
        vec = np.random.uniform(-10,10,2)
        self.velocity = Vector(*vec)
        vec2 = np.random.uniform(-0.5,0.5,2)
        self.acceleration = Vector(*vec2)


        self.max_speed = 5
        self.force = 0.5
        self.width = WIDTH
        self.height = HEIGHT

        self.alive = True

        self.align_coef = align_coef
        self.separation_coef = separation_coef
        self.cohesion_coef = cohesion_coef

    def Neighbours(self, boids):
        neighbours = []
        for bird in boids:
            if np.linalg.norm(bird.position - self.position) < 50:  # The distance between boids.
                neighbours.append(bird)
        return neighbours

    def show(self):
        # Triangular Bird's settings.
        side = 10
        tri_len = (np.sqrt(3) / 3) * side
        tri_len2 = (np.sqrt(3) / 6) * side

        fill('white')

        if self.alive == False:  # just for debugging to see which birds die
            fill("black")

        A = (self.position[0], self.position[1] + tri_len)
        B = (self.position[0] - (side / 2), self.position[1] - tri_len2)
        C = (self.position[0] + (side / 2), self.position[1] - tri_len2)
        triangle(A[0], A[1], B[0], B[1], C[0], C[1])

    def update(self,iter):

        self.position += self.velocity
        self.velocity += self.acceleration


        # To prevent velocity and acceleration to be too high.
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = (self.velocity / np.linalg.norm(self.velocity)) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))

        # if iter % 3 == 0:
        #     self.velocity += Vector(*np.random.uniform(-0.5,0.5,2)) * 7

    # Boundary Condition settings.
    def boundary(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def alignment(self, boids, iter):  # Boids tends to TURN in same direction with nearby boids.
        average_vector = Vector(*np.zeros(2))
        steering_angle = Vector(*np.zeros(2))
        total_velocity = Vector(*np.zeros(2))
        boid_count = 0

        for bird in boids:
            if np.linalg.norm(bird.position - self.position) < 50:
                total_velocity += bird.velocity
                boid_count += 1

        if boid_count > 1:
            average = total_velocity / boid_count
            average_vector = Vector(*average)
            average_vector = (average_vector / np.linalg.norm(average_vector)) * self.max_speed
        if iter % 15 == 0 :
            average_vector += Vector(*np.random.uniform(-0.5,0.5,2)) * 7
        return average_vector * (self.align_coef * COEF_ADJUST)

    def alignment_update(self, boids,iter):
        alignment = self.alignment(boids,iter)
        self.acceleration += M * alignment

    def separation(self, boids):  # Avoid collisions
        # position_difference = Vector(*np.zeros(2))
        #
        # for bird in boids:
        #     position_difference += self.position - bird.position
        #
        # return position_difference  # in Paper it is negative
        steering_angle = Vector(*np.zeros(2))
        count = 0
        difference_total = Vector(*np.zeros(2))

        for bird in boids:
            distance = np.linalg.norm(bird.position - self.position)

            if self.position != bird.position and distance < 70:

                position_diff = (self.position - bird.position) / distance
                difference_total += position_diff
                count += 1

            if count > 0:
                average_vector = Vector(*(difference_total / count))
                if np.linalg.norm(steering_angle) > 0:
                    average_vector = (average_vector / np.linalg.norm(steering_angle)) * self.max_speed
                steering_angle = average_vector - self.velocity

                if np.linalg.norm(steering_angle) > self.force:
                    steering_angle = (steering_angle / np.linalg.norm(steering_angle)) * self.force

        return steering_angle * (self.separation_coef * COEF_ADJUST)


    def separation_update(self, boids):
        separation_steer = self.separation(boids)
        self.acceleration += S * separation_steer

    def cohesion(self, boids):  # Boids MOVE towards the pack.

        steering_angle = Vector(*np.zeros(2))
        displacement_vector = Vector(*np.zeros(2))
        # average_position = Vector(*np.zeros(2))
        total_position = Vector(*np.zeros(2))
        boid_count = 0

        for bird in boids:
            if np.linalg.norm(bird.position - self.position) < 50:
                total_position += bird.position
                boid_count += 1

        if boid_count > 0:
            average_position = Vector(*(total_position / boid_count))  # average position of all neighbours
            displacement_vector = average_position - self.position
            if np.linalg.norm(displacement_vector) > 0:
                displacement_vector = (displacement_vector / np.linalg.norm(displacement_vector)) * self.max_speed
            steering_angle = displacement_vector

            if np.linalg.norm(steering_angle) > self.force:
                steering_angle = (steering_angle / np.linalg.norm(steering_angle)) * self.force

        return steering_angle * (self.cohesion_coef * COEF_ADJUST)

    def cohesion_update(self, boids):
        cohesion = self.cohesion(boids)
        self.acceleration += K * cohesion

    def combine_steers(self, boids,iter):
        separation_steer = self.separation(boids)
        cohesion = self.cohesion(boids)
        alignment = self.alignment(boids,iter)

        self.acceleration += S * separation_steer + K * cohesion + M * alignment

    def birth(self,boids,iter):
        count = 0
        for bird in boids:
            if np.linalg.norm(bird.position - self.position) < 50:
                count +=1
                #*np.random.rand(2) * 1000
            if count > 2 and iter % 5 == 0:
                pos_x = self.position.x + random.uniform(-3, 3)
                pos_y = self.position.y + random.uniform(-3, 3)

                pos = Vector(pos_x,pos_y)
                return True, pos


    def collusion(self,boids):

        for bird in boids:
            distance = distance = np.linalg.norm(bird.position - self.position)

            if self.position != bird.position and distance < 10:
                self.alive = False

            if self.alive == False:
                fill('black')







class Predator(Boid):
    def __init__(self, x, y, WIDTH, HEIGHT):
        Boid.__init__(self, x, y, WIDTH, HEIGHT,align_coef=0,separation_coef=0,cohesion_coef=0)
        self.position = Vector(x, y)
        vec = (np.random.rand(2)) * 10 + 0.2
        self.velocity = Vector(*vec)
        vec2 = (np.random.rand(2)) / 2 + 0.2
        self.acceleration = Vector(*vec2)

        self.max_speed = 6
        self.width = WIDTH
        self.height = HEIGHT

    def awareness(self,boids):
        nearby = []
        commute_vector = Vector(*np.zeros(2))
        steering_angle = Vector(*np.zeros(2))
        for bird in boids:

            if np.linalg.norm(bird.position - self.position) < 130:
                bird_count = bird.Neighbours(boids)

                if len(bird_count) == 1:

                    commute_vector = bird.position - self.position

                    if np.linalg.norm(commute_vector) > 0:
                        commute_vector = (commute_vector/np.linalg.norm(commute_vector)) * self.max_speed * 2

                    steering_angle = commute_vector

        return steering_angle

    def awareness_update(self,boids):
        awareness = self.awareness(boids)
        self.acceleration += awareness * 2


    def eat(self, boids):
        nearby = []

        for bird in boids:

            if np.linalg.norm(bird.position - self.position) < 15:
                nearby.append(bird)
                neighbours = bird.Neighbours(boids)

                if len(neighbours) < 3:  # if bird has not a certain amount of neighbours, the predator attacks it
                    bird.alive = False

    def show(self):
        # Triangular Bird's settings.
        side = 14
        tri_len = (np.sqrt(3) / 3) * side
        tri_len2 = (np.sqrt(3) / 6) * side

        fill('red')
        A = (self.position[0], self.position[1] + tri_len)
        B = (self.position[0] - (side / 2), self.position[1] - tri_len2)
        C = (self.position[0] + (side / 2), self.position[1] - tri_len2)
        triangle(A[0], A[1], B[0], B[1], C[0], C[1])
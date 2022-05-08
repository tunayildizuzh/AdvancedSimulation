import numpy as np
from p5 import setup, draw, size, background,run,Vector,stroke,triangle,color,fill

class Boid():

    def __init__(self,x,y,WIDTH,HEIGHT):
        self.position = Vector(x,y)
        vec = (np.random.rand(2)) * 10
        self.velocity = Vector(*vec)
        vec2 = (np.random.rand(2))/2
        self.acceleration = Vector(*vec2)

        self.max_speed = 5
        self.width = WIDTH
        self.height = HEIGHT



    def show(self):
        # Triangular Bird's settings.
        side = 12
        tri_len = (np.sqrt(3) /3) * side
        tri_len2 = (np.sqrt(3) /6) * side

        fill(255,204,0)
        A = (self.position[0],self.position[1]+tri_len)
        B = (self.position[0] - (side/2),self.position[1]- tri_len2)
        C = (self.position[0] + (side/2),self.position[1]- tri_len2)
        triangle(A[0],A[1],B[0],B[1],C[0],C[1])

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        # To prevent velocity and acceleration to be too high.
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))

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
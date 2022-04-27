import numpy as np
import matplotlib.pyplot as plt

# Reference https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9

def unit_vec(vec):
    return vec / np.linalg.norm(vec)


def reflected(vector, axis):
    return vector - 2 * np.dot(vector,axis) * axis


def sphere_intersection(center, radius, ray_origin, ray_direction): # Solving quadratic eq. for sphere function and ray
    b = 2 * np.dot(ray_direction, ray_origin-center)
    c = np.linalg.norm(ray_origin-center) **2 - radius**2
    delta = b ** 2 - 4*c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:  # Selecting positive points (because negative t values = -d, behind camera.)
            return min(t1, t2)  # Minimum distance is selected since we are picking the closest intersection point.
    return None


def closest_intersected_object(objects, ray_origin, ray_direction):
    distances = [sphere_intersection(obj['center'],obj['radius'], ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]

    return nearest_object, min_distance


WIDTH = 1920
HEIGHT = 1080
max_depth = 3
camera = np.array([0,0,1])

ratio = float(WIDTH)/HEIGHT
screen = (-1, 1/ratio, 1, -1/ratio)  # Sides of the screen
light = {'position': np.array([-3.5,2,5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1,1,1]), 'specular': np.array([1,1,1])}
image = np.zeros((HEIGHT,WIDTH,3))

objects = [
    {'center': np.array([-0.15, 0, -1]), 'radius': 0.8, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0.1, -0.1, 0]), 'radius': 0.07, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'center': np.array([0.25, 0.3, 0]), 'radius': 0.15, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    #{'center': np.array([0, -9000, 0]), 'radius': 9000- 0.7, 'ambient': np.array([0.05, 0.05, 0.05]), 'diffuse': np.array([0.3, 0.3, 0.3]), 'specular': np.array([0.5, 0.5, 0.5]), 'shininess': 60, 'reflection': 0}
]


for i, y in enumerate(np.linspace(screen[1], screen[3], HEIGHT)):
    for j, x in enumerate(np.linspace(screen[0],screen[2], WIDTH)):
        pixel = np.array([x, y, 0])
        origin = camera
        direction = unit_vec(pixel-origin)

        color = np.zeros((3))
        reflection = 1

        for k in range(max_depth):
            # Checking intersections
            nearest_object, min_distance = closest_intersected_object(objects, origin, direction)
            if nearest_object is None:
                break

            # Intersection point of ray and nearest object
            intersection = origin + min_distance * direction

            normal_to_surface = unit_vec(intersection - nearest_object['center'])
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = unit_vec(light['position'] - intersection)

            _, min_distance = closest_intersected_object(objects, shifted_point, intersection_to_light)
            intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                break

            illumination = np.zeros((3))
            illumination += nearest_object['ambient'] * light['ambient'] # Ambient

            illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface) # Diffuse

            intersection_to_camera = unit_vec(camera - intersection) # Specular
            H = unit_vec(intersection_to_light + intersection_to_camera)
            illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)

            # Reflection settings.
            color += reflection * illumination
            reflection *= nearest_object['reflection']

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

            image[i,j] = np.clip(illumination, 0, 1)


plt.imsave('image.png', image)





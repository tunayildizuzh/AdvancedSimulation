import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Reference https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9

data = pd.read_csv('/Users/tunayildiz/Desktop/UZH/AdvancedSim/teapot.txt', sep=" ", header=None)
data_remove = data.drop(columns = [0])
grouped = data_remove.groupby(data[0])

vertex_df = grouped.get_group('v')
faces_df = grouped.get_group('f')

vertex = vertex_df.to_numpy()
faces = faces_df.to_numpy()

print(f"vertex array shape: {vertex.shape}")
print(f"faces array shape: {faces.shape}")

row, col = faces.shape


face_vector = np.zeros((3, row, 3))
for i in range(row):
    v0 = vertex[int(faces[i,0])-1]
    v1 = vertex[int(faces[i,1])-1]
    v2 = vertex[int(faces[i,2])-1]
    face_vector[0][i] = np.array(v0)
    face_vector[1][i] = np.array(v1)
    face_vector[2][i] = np.array(v2)
# First depth second row third specific element of the vector
# print(f" V0 OF TRI INTERSECTION {face_vector[0][0]}")
# print(f" V1 OF TRI INTERSECTION {face_vector[1][0]}")
# print(f" V2 OF TRI INTERSECTION {face_vector[2][0]}")


triangle_object = []
for j in range(row-2):
    triangle_object.append({'faces': [face_vector[0, j],face_vector[1, j],face_vector[2, j]],'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5  })
print(triangle_object[0]['faces'])



a = np.array([ 1.368074,  2.435437, -0.227403])
b = np.array([ 1.381968,  2.4     , -0.229712])
c = np.array([1.4, 2.4, 0. ])


def tri_intersection(v0,v1,v2, ray_origin, ray_direction):
    # Normal Force.
    # print(f"V0: {v0.shape}")
    # print(f"V1: {v1.shape}")
    # print(f"V2: {v2.shape}")
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    N = np.cross(v0v1, v0v2)


    # P = O + tR   o origin, direction R, d from plane eq.
    parallel = np.dot(N, ray_direction)
    #print(f"ray_dire: {ray_direction}")
    #print(f"parallel: {parallel}")
    if parallel < 1e-8:   # PARALLEL CHECK. with epsilon being 1e-8
        return None

    D = np.dot(N, v0)
    t = (np.dot(N, ray_origin) + D) / np.dot(N, ray_direction)
    # print(D)
    # print(np.dot(N, ray_origin) + D)
    # print(f"ray origin {ray_origin}")
    # print(f"N,ray_dire: {np.dot(N, ray_direction)}")
    # print(t)
    if t < 0 :    # Checking if the triangle is behind the ray
        return None

    P = ray_origin + t * ray_direction  # Intersection point.

    # inside-outside test
    # Go through each edge of the triangle.
    edge0 = v1-v0
    vp0 = P - v0
    C0 = np.cross(edge0, vp0)
    # print(f"dot prod. {np.dot(N,C0)}")
    if np.dot(N, C0) < 0: # Intersection is on the right side.
        return None

    edge1 = v2-v1
    vp1 = P - v1
    C1 = np.cross(edge1, vp1)

    if np.dot(N, C1) < 0: # Intersection is on the right side.
        return None

    edge2 = v0-v2
    vp2 = P - v2
    C2 = np.cross(edge2, vp2)

    if np.dot(N, C2) < 0: # Intersection is on the right side.
        return None

    return t # Ray hits the triangle.

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

#print(triangle_object['faces'][0])
def closest_intersected_object(objects, ray_origin, ray_direction):

    distances = [tri_intersection(obj['faces'][0], obj['faces'][1], obj['faces'][2], ray_origin,ray_direction) for obj in objects]
    #print(f"DISTANCES ARE HEREEEEE: {distances}")
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = triangle_object[index]

    return nearest_object, min_distance




WIDTH = 100
HEIGHT = 60
max_depth = 3
camera = np.array([0,0,1])

ratio = float(WIDTH)/HEIGHT
screen = (-1, 1/ratio, 1, -1/ratio)  # Sides of the screen
light = {'position': np.array([-3.5,2,5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1,1,1]), 'specular': np.array([1,1,1])}
image = np.zeros((HEIGHT,WIDTH,3))


# objects = [
#     {'center': np.array([-0.15, 0, -1]), 'radius': 0.8, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
#     {'center': np.array([0.1, -0.1, 0]), 'radius': 0.07, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
#     {'center': np.array([0.25, 0.3, 0]), 'radius': 0.15, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
#     #{'center': np.array([0, -9000, 0]), 'radius': 9000- 0.7, 'ambient': np.array([0.05, 0.05, 0.05]), 'diffuse': np.array([0.3, 0.3, 0.3]), 'specular': np.array([0.5, 0.5, 0.5]), 'shininess': 60, 'reflection': 0}
# ]
#print(f"OBJECTS: {objects}")



for i, y in enumerate(np.linspace(screen[1], screen[3], HEIGHT)):
    for j, x in enumerate(np.linspace(screen[0],screen[2], WIDTH)):
        pixel = np.array([x, y, 0])
        origin = camera
        direction = unit_vec(pixel-origin)
        #print(f"DIRECTION: {direction}")
        color = np.zeros((3))
        reflection = 1

        for k in range(max_depth):
            print(f"k val is: {k}")
            # Checking intersections
            nearest_object, min_distance = closest_intersected_object(triangle_object,origin, direction)
            print(f"NEAREST OBJECT: {nearest_object}")
            #print("Nearest object and min distance values are obtained.")
            if nearest_object is None:
                break

            # Intersection point of ray and nearest object
            intersection = origin + min_distance * direction

            normal_to_surface = unit_vec(intersection - nearest_object['faces'][0])
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = unit_vec(light['position'] - intersection)

            _, min_distance = closest_intersected_object(triangle_object, shifted_point, intersection_to_light)
            intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
            is_shadowed = min_distance < intersection_to_light_distance
            #print("is_shadowed values are obtained.")

            if is_shadowed:
                break

            #print('illumination process begins.')
            illumination = np.zeros((3))
            illumination += nearest_object['ambient'] * light['ambient'] # Ambient

            illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface) # Diffuse

            intersection_to_camera = unit_vec(camera - intersection) # Specular
            H = unit_vec(intersection_to_light + intersection_to_camera)
            illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)
            #print('reflection process begins.')
            # Reflection settings.
            color += reflection * illumination
            reflection *= nearest_object['reflection']

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)
            print('image construction begins.')
            print(f"ITERATION: {i}, {j}")
            image[i,j] = np.clip(illumination, 0, 1)


plt.imsave('image.png', image)


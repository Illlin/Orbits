from typing import List
import numpy as np
G =  6.67430e-11


class Body:
    def __init__(self, radius, gm, position, velocity, name=None):
        self.name = "" if name is None else name
        self.gm = gm                # m^3/s^2
        self.mass = gm/G            # KG?
        self.radius = radius        # km
        self.position = position    # Vec3 km
        self.velocity = velocity    # Vec3 km

    def __str__(self):
        return self.name

    def step(self, t):
        self.position += self.velocity * t


class System:
    def __init__(self, bodies: List[Body]):
        self.bodies = bodies

        self.all_pos = np.array([x.position for x in self.bodies])
        self.all_vel = np.array([x.velocity for x in self.bodies])
        self.all_gm = np.array([x.gm for x in self.bodies])
        self.all_names = [x.name for x in self.bodies]

    def store_back(self):
        # Store data back into bodies
        pass

    def get_pos(self):
        return self.all_pos

    def step(self, t):
        # Compute forces
        for i, body in enumerate(self.bodies):
            sum_a = np.zeros(3)
            for j, other in enumerate(self.bodies):
                if i == j:
                    continue
                dist_vector = (other.position - body.position)
                r = np.linalg.norm(dist_vector)
                dist_norm = dist_vector / r
                f = (body.gm * other.gm)/(r*r)
                a = f/body.mass
                sum_a = dist_norm*a

            body.velocity += sum_a*t

        for body in self.bodies:
            body.step(t)



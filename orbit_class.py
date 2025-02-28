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

        self.all_pos = np.array([x.position for x in bodies])
        self.all_vel = np.array([x.velocity for x in bodies])
        self.all_gm = np.array([x.gm for x in bodies])

    def print(self):
        for body in self.bodies:
            print(f"{body.name:20}: {body.mass}")

    def store_back(self):
        # Store data back into bodies
        for i, body in enumerate(self.bodies):
            body.position = self.all_pos[i]
            body.velocity = self.all_vel[i]

    def get_pos(self):
        return self.all_pos
        return [x.position for x in self.bodies]

    def fast_step(self, t, e=1e-5):
        dr = self.all_pos[np.newaxis, :, :] - self.all_pos[:, np.newaxis, :]
        r_sq = np.sum(dr**2, axis=2) + e**2
        inv_r_cubed = 1.0 / (r_sq**1.5)
        np.fill_diagonal(inv_r_cubed, 0)

        accel_factor = self.all_gm[np.newaxis, :, np.newaxis] * inv_r_cubed[:, :, np.newaxis]
        acceleration = (accel_factor * dr).sum(axis=1)

        self.all_vel += acceleration * t
        self.all_pos += self.all_vel * t


        print("pass")

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
                # f = G*(body.mass * other.mass)/(r*r)
                # a = f/body.mass

                a = other.gm/(r*r)
                sum_a += dist_norm*a

            body.velocity += sum_a*t

        for body in self.bodies:
            body.step(t)

    def localise(self):
        # return
        centre = self.bodies[0].position * 1
        vel = self.bodies[0].velocity * 1
        # self.bodies[0].velocity -= vel

        for body in self.bodies:
            body.position -= centre
            body.velocity -= vel


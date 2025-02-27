from typing import List
import numpy as np


class Body:
    def __init__(self, radius, gm, position, velocity, name=None):
        self.name = "" if name is None else name
        self.gm = gm                # km^3/s^2
        self.radius = radius        # km
        self.position = position    # Vec3 km
        self.velocity = velocity    # Vec3 km

    def __str__(self):
        return self.name


class System:
    def __init__(self, bodies: List[Body]):
        self.bodies = bodies

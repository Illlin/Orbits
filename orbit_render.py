from orbit_class import Body, System
from horizons import get_solar_system_data, targets
import numpy as np

def get_system():
    df = get_solar_system_data(targets, 10)

    bodies = []
    for i, body in df.iterrows():
        r = body["Mean radius (km)"]
        if np.isnan(r):
            r = body["Equat. radius (1 bar)"]

        bodies.append(
            Body(
                r,
                body["GM (km^3/s^2)"],
                body["pos"],
                body["vel"],
                name=body["name"]
            )
        )

    return System(bodies)


if __name__ == "__main__":
    system = get_system()
    print("pass")
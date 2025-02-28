from orbit_class import Body, System
from horizons import get_solar_system_data, targets
import numpy as np
import pyray as pr

def get_system():
    df = get_solar_system_data(targets, 10)

    bodies = []
    for i, body in df.iterrows():
        r = body["Mean radius (km)"]
        if np.isnan(r):
            r = body["Equat. radius (1 bar)"]

        bodies.append(
            Body(
                r*1000,
                body["GM (km^3/s^2)"] * 1000000000,
                body["pos"],
                body["vel"],
                name=body["name"]
            )
        )

    return System(bodies)


if __name__ == "__main__":
    screen_w = 1200
    screen_h = 800

    system = get_system()
    # Centre on First object
    system.localise()

    system.print()

    body_pos = system.get_pos()
    system_centre = system.bodies[0].position * 1
    # Localise on Centre
    body_pos = body_pos - system_centre
    # Find dims
    system_dims = np.abs(np.max(body_pos, axis=0) - np.min(body_pos, axis=0))

    # Set scale
    zoom = (np.max(system_dims)/screen_h)*2

    pr.init_window(screen_w,screen_h, "Orbits")
    pr.set_target_fps(1)
    system.fast_step(1)
    while not pr.window_should_close():
        # Center screen

        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        pr.draw_text(f"{pr.get_fps(): 3d} fps", 0,0, 20, pr.PURPLE)
        for body in system.bodies:
            for i in range(1):
                # system.step(10)
                system.fast_step(1)
            system.store_back()
            pos = (body.position-system_centre)/zoom
            screen_pos = int(pos[0] + screen_w/2), int(pos[1] + screen_h/2)
            rad = max(5,body.radius/zoom)
            pr.draw_circle(
                screen_pos[0],
                screen_pos[1],
                rad,
                pr.VIOLET
            )
            pr.draw_text(body.name, int(screen_pos[0]+rad), int(screen_pos[1]+rad), 10, pr.BLACK)

        pr.end_drawing()



    print("pass")
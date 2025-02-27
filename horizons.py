from astroquery.jplhorizons import Horizons
import datetime
import pandas as pd
import numpy as np

au = 148587870.700

# List of major solar system objects (Sun-centered)
targets = [
    # Planets
    # {'name': 'Mercury', 'id': '199'},
    # {'name': 'Venus', 'id': '299'},
    # {'name': 'Earth', 'id': '399'},
    # {'name': 'Mars', 'id': '499'},
    # {'name': 'Saturn', 'id': '699'},
    # {'name': 'Uranus', 'id': '799'},
    # {'name': 'Neptune', 'id': '899'},
    # {'name': 'Pluto', 'id': '999'},

    # Jupiter moons (Galilean + others)
    {'name': 'Io', 'id': '501'},
    {'name': 'Europa', 'id': '502'},
    {'name': 'Ganymede', 'id': '503'},
    {'name': 'Callisto', 'id': '504'},
    {'name': 'Amalthea', 'id': '505'},
    # {'name': 'Himalia', 'id': '506'},
    {'name': 'Jupiter', 'id': '599'},
]


def get_solar_system_data(bodies, target):
    data = []

    for body in bodies:
        # Query Horizons for vectors (position) and elements (orbital characteristics)
        obj = Horizons(id=body['id'], location=target, epochs={'start': '2025-01-01', 'stop': '2025-01-02', 'step': '1h'})

        # Get position vectors (geometric coordinates)
        vec_table = obj.vectors()

        # Get orbital elements
        elements_table = obj.elements()

        obj_stats = {}
        # Get physical atributes
        lines = obj.last_response.text.split("\n")
        # [print(f"{i: 4d}:  {c}") for i, c in enumerate(lines)]
        split_lines = [i for i, c in enumerate(lines) if "********************************" in c]

        [print(f"{i: 4d}:  {c}") for i, c in enumerate(lines[split_lines[0]:split_lines[1]])]

        physcial_lines = lines[split_lines[0]+1:split_lines[1]]
        split_phys_lines = [i for i, c in enumerate(physcial_lines) if c.strip() == "" or "              " in c[:15]]
        phys_lines = physcial_lines[split_phys_lines[0]+2:split_phys_lines[1]]
        c = phys_lines[0].find("Density") - 1
        for line in phys_lines:
            def parse_val(val):
                val = val.strip()
                # Remove +-
                val = val.split("+")[0]

                if len(val) == 0:
                    return None

                if "h" in val and "m" in val and "s" in val:
                    print("TIME!!")
                    return None

                # Tiny values are reperesented as < Xx10^-Y
                val = val.strip("~< \"''")

                # Scientific notation
                val = val.replace("x10^", "e")

                # Remove units
                val = val.split(" ")[0]

                try:
                    return float(val)
                except ValueError:
                    print("Pass")
            es = [i for i, c in enumerate(line) if c == "="]

            obj_stats[line[0:es[0]].strip().replace("   ", " ")] = parse_val(line[es[0]+1:c])
            if len(es) == 2:
                obj_stats[line[c:es[1]].strip()] = parse_val(line[es[1]+1:])
        obj_stats["name"] = elements_table["targetname"][0]

        # coord
        pos_samples = np.array([
            [vec_table['x'][0], vec_table['y'][0], vec_table['z'][0]],
            [vec_table['x'][1], vec_table['y'][1], vec_table['z'][1]],
        ]) * au

        obj_stats["pos"] = np.mean(pos_samples, axis=0)
        obj_stats["vel"] = pos_samples[1] - pos_samples[0]

        data.append(obj_stats)
        print(f"Retrieved data for {body['name']}")


    return pd.DataFrame(data)

if __name__ == "__main__":
    # Get data and save to CSV
    df = get_solar_system_data(targets, 10)
    df.to_csv('solar_system_objects.csv', index=False)
    print("\nData saved to solar_system_objects.csv")
    print(df[['name', 'x (AU)', 'y (AU)', 'z (AU)', 'semi_major_axis (AU)', 'eccentricity']])
    print("pass")
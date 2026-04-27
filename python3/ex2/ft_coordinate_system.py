import math
from typing import Tuple


def get_player_pos(prompt: str) -> Tuple[float, float, float]:
    while True:
        coord = input(prompt)
        parts = coord.split(',')
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())
            return (x, y, z)
        except ValueError as e:
            for p in parts:
                p = p.strip()
                try:
                    float(p)
                except ValueError:
                    print(f"Error on parameter '{p}': {e}")
                    break


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    print("Get a first set of coordinates")
    pos1 = get_player_pos(
        "Enter new coordinates as floats in format 'x,y,z': ")
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    dist1 = math.sqrt(pos1[0]**2 + pos1[1]**2 + pos1[2]**2)
    print("Distance to center: {:.4f}".format(dist1))
    print("Get a second set of coordinates")
    pos2 = get_player_pos(
        "Enter new coordinates as floats in format 'x,y,z': ")
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    dist2 = math.sqrt(dx**2 + dy**2 + dz**2)
    print("Distance between the 2 sets of coordinates: {:.4f}".format(dist2))

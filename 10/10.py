"""10.py."""
import math


def show(program):
    for row in program:
        print(''.join(row))


def map_asteroids(program):
    # X, Y
    asteroid_pos = list()
    for y, row in enumerate(program):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroid_pos.append((x, y))
    return asteroid_pos


def find_polar_coordinates_of_asteroids(center_position, asteroid_positions):
    polar_coords = dict()
    for asteroid in asteroids:
        if center_position != asteroid:
            cx, cy = center_position
            ox, oy = asteroid
            # Find new coords with center as origo
            x = ox - cx
            y = oy - cy
            # Polar coordinates
            rho = math.sqrt(x*x + y*y)
            theta = math.atan2(y, x)*(180/math.pi)+90
            if theta < 0:
                theta += 360
            if theta not in polar_coords:
                polar_coords[theta] = {rho: asteroid}
            else:
                polar_coords[theta][rho] = asteroid
    return polar_coords


def find_asteroids_in_positions(asteroids):
    sums = dict()
    for curr_asteroid in asteroids:
        angles_d = dict()
        for other_asteroid in asteroids:
            if curr_asteroid != other_asteroid:
                cx, cy = curr_asteroid
                ox, oy = other_asteroid
                x = cx - ox
                y = cy - oy
                # Polar coordinates
                rho = math.sqrt(x*x + y*y)
                angle = math.atan2(y, x)*(180/math.pi)
                angles_d[angle] = (rho, x, y)
        sums[curr_asteroid] = len(angles_d)
    return sums


with open("input.txt") as f:
    program = [list(line.strip()) for line in f.readlines()]
    asteroids = map_asteroids(program)

    sum_positions = find_asteroids_in_positions(asteroids)
    max_val = 0
    for pos, val in sum_positions.items():
        max_val = max(val, max_val)
        if val == max_val:
            best_pos = pos
    print('Part1: {}'.format(max_val))

    polar_coords = find_polar_coordinates_of_asteroids(best_pos, asteroids)
    all_angles_sorted = sorted(polar_coords.keys())

    i = 0
    while len(polar_coords) > 0:
        for angle in all_angles_sorted:
            if angle in polar_coords.keys():
                shortest_distance = sorted(polar_coords[angle].keys())[0]
                i += 1
                x, y = polar_coords[angle][shortest_distance]
                # print(i, x, y)
                if i == 200:
                    print('Part2: {}'.format(int(x) * 100 + int(y)))
                polar_coords[angle].pop(shortest_distance)
                if len(polar_coords[angle]) == 0:
                    polar_coords.pop(angle)

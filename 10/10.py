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

def find_best_position(program, asteroids):
    height = len(program)
    width = len(program[0])
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
                theta = math.atan2(y, x)*(180/math.pi)
                angles_d[theta] = (rho, x, y)
        sums[curr_asteroid] = len(angles_d)
    return sums

with open("input.txt") as f:
    program = [list(line.strip()) for line in f.readlines()]
    asteroids = map_asteroids(program)

    sum_positions = find_best_position(program, asteroids)
    max_val = 0
    for pos, val in sum_positions.items():
        max_val = max(val, max_val)
        if val == max_val:
            best_pos = pos
    print(best_pos, max_val)

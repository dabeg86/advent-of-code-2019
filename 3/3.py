"""3.py."""


def get_min_manhattan_distance(central_port_coord, all_intersections):
    """Get intersection with min distance from central port."""
    c_x, c_y = central_port_coord
    distances = []
    for x, y in all_intersections:
        # Manhattan distance (p1, p2) and (q1, q2) = abs(p1 - q1) + abs(p2 - q2)
        distance = abs(c_x - x) + abs(c_y - y)
        distances.append(distance)
    return min(distances)


with open("input") as f:
    central_port = (0, 0)
    all_wire_coords = list()
    wire_paths = list()
    intersections = set()
    wire_coords = list()
    for line in f.read().splitlines():
        wire_paths.append(line.split(','))
    for wire in wire_paths:
        wire_coords = dict()
        x = 0
        y = 0
        total_length = 0
        for instruction in wire:
            starting_point = (x, y)
            direction = instruction[0]
            amount = int(instruction[1:])
            for i in range(amount):
                if direction == 'U':
                    y += 1
                elif direction == 'D':
                    y -= 1
                elif direction == 'R':
                    x += 1
                elif direction == 'L':
                    x -= 1
                else:
                    raise AttributeError("Unkown direction: {}".format(direction))
                total_length += 1
                if (x, y) in wire_coords:
                    wire_coords[(x, y)] = min(total_length, wire_coords[(x, y)])
                else:
                    wire_coords[(x, y)] = total_length
        all_wire_coords.append(wire_coords)

    wire1 = all_wire_coords[0]
    wire2 = all_wire_coords[1]
    intersections = set(wire1.keys()) & set(wire2.keys())
    path_sum = 99999999999999999999999999
    for intersection in intersections:
        new_path_sum = wire1[intersection] + wire2[intersection]
        path_sum = min(new_path_sum, path_sum)
        if new_path_sum == path_sum:
            smallest_coord = intersection

    print('Part 1: {}'.format(get_min_manhattan_distance(central_port, intersections)))
    print('Part 2: {}, {} steps'.format(smallest_coord, path_sum))

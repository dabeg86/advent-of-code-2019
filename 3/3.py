"""3.py."""

# Manhattan distance (p1, p2) and (q1, q2) = abs(p1 - q1) + abs(p2 - q2)


def get_new_coords(start_x, start_y, direction, amount):
    """Get list of new coordinates."""
    if direction == 'U':
        new_coords = list(zip([start_x]*amount,
                              list(range(start_y, start_y + amount))))
        start_y += amount
    elif direction == 'D':
        new_coords = list(zip([start_x]*amount,
                              list(range(start_y - amount, start_y))))
        start_y -= amount
    elif direction == 'R':
        new_coords = list(zip(range(start_x, start_x + amount),
                              list([start_y]*amount)))
        start_x += amount
    elif direction == 'L':
        new_coords = list(zip(range(start_x - amount, start_x),
                              list([start_y]*amount)))
        start_x -= amount
    else:
        raise AttributeError("Unkown direction: {}".format(direction))

    return start_x, start_y, new_coords


def get_min_manhattan_distance(central_port_coord, all_intersections):
    """Get intersection with min distance from central port."""
    c_x, c_y = central_port_coord
    distances = []
    for x, y in all_intersections:
        distance = abs(c_x - x) + abs(c_y - y)
        distances.append(distance)
    return min(distances)


with open("input") as f:
    central_port = (0, 0)
    wire_paths = list()
    intersections = set()
    all_wire_paths = set()
    for line in f.read().splitlines():
        wire_paths.append(line.split(','))
    for wire in wire_paths:
        x = 0
        y = 0
        wire_path = set()
        for instruction in wire:
            starting_point = (x, y)
            x, y, coords = get_new_coords(x, y,
                                          instruction[0],
                                          int(instruction[1:]))
            for coord in coords:
                wire_path.add(coord)
        for coord in wire_path:
            if coord in all_wire_paths:
                intersections.add(coord)
            else:
                all_wire_paths.add(coord)

    if central_port in intersections:
        intersections.remove(central_port)
    print('intersections: {}'.format(intersections))
    print(get_min_manhattan_distance(central_port, intersections))

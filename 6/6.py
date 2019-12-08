"""6.py."""

you_path = set()
santa_path = set()

with open("input.txt") as f:
    map_data = f.readlines()
    nodes = dict()
    for line in map_data:
        p, c = line.strip().split(')')
        nodes[c] = p


def get_depth(node):
    if node == 'COM':
        return 0
    else:
        n_node = nodes[node]
        return 1 + get_depth(n_node)


def get_visited_nodes(visited, node):
    visited.add(node)
    if node == 'COM':
        return visited
    else:
        n_node = nodes[node]
        return get_visited_nodes(visited, n_node)

sum = 0
for node, child in nodes.items():
    sum += get_depth(node)

print('Part1: {}'.format(sum))
you = get_visited_nodes(set(), 'YOU')
santa = get_visited_nodes(set(), 'SAN')
common = you.intersection(santa)
you = you - common
santa = santa - common
print('Part2: {}'.format(len(you) + len(santa) - 2))

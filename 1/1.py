"""1.py."""


def calc_fuel(mass):
    """Calculate the fuel for one module."""
    fuel = int(mass / 3) - 2
    if fuel >= 0:
        return fuel + calc_fuel(fuel)
    else:
        return 0


with open("inputs.txt") as f:
    content = f.readlines()

    total_fuel = 0
    for i in range(len(content)):
        total_fuel += calc_fuel(int(content[i].strip()))

    print(total_fuel)

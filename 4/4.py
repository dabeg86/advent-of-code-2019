start = 128392
stop = 643281

part1 = 0
part2 = 0

def adjacent_not_part_of_larger_group(number_set, number_str):
    for digit in number_set:
        digits_of_same = number_str.count(digit)
        if digits_of_same == 2:
            return True
    return False

for number in range(start, stop + 1):
    number_str = str(number)
    number_set = set(number_str)
    if len(number_set) != 6: # Has duplicates
        if number == int(''.join(sorted(number_str))): # Never decreases
            part1 += 1
            if adjacent_not_part_of_larger_group(number_set, number_str):
                part2 +=1

print('Part1: {}'.format(part1))
print('Part2: {}'.format(part2))
"""11.py."""

_OP_LENGTH_4 = 4
_OP_LENGTH_3 = 3
_OP_LENGTH_2 = 2

position = '0'
immediate = '1'
relative = '2'

from enum import Enum

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


def get_parameter(mode, program, function_ptr, relative_base):
    if function_ptr not in program:
        program[function_ptr] = 0

    if mode == position:
        if program[function_ptr] not in program:
            program[program[function_ptr]] = 0
        return program[program[function_ptr]]
    elif mode == immediate:
        return program[function_ptr]
    elif mode == relative:
        if program[function_ptr]+relative_base not in program:
            program[program[function_ptr]+relative_base] = 0
        return program[program[function_ptr]+relative_base]
    else:
        raise ValueError('Unknown mode: {}'.format(mode))


def set_parameter(mode, program, function_ptr, value, relative_base):
    if function_ptr not in program:
        program[function_ptr] = 0

    if mode == position:
        program[program[function_ptr]] = value
    elif mode == immediate:
        program[function_ptr] = value
    elif mode == relative:
        program[program[function_ptr]+relative_base] = value
    else:
        raise ValueError('Unknown mode: {}'.format(mode))


def intcode_machine(function_ptr_start, relative_base_start, in_val, program):
    """Intcode machine."""
    function_ptr = function_ptr_start
    output_cnt = 0
    first_output = 0
    relative_base = relative_base_start
    while(program[function_ptr] != 99):
        # Interpret the instruction
        instruction = str(program[function_ptr]).zfill(5)
        op_code = instruction[3:5]
        par1_mode = instruction[2]
        par2_mode = instruction[1]
        par3_mode = instruction[0]

        # Do the instruction
        if op_code == '01': # Addition
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            op_result = par1 + par2
            set_parameter(par3_mode, program, function_ptr+3, op_result, relative_base)
            function_ptr += _OP_LENGTH_4
        elif op_code == '02': # Multiply
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            op_result = par1 * par2
            set_parameter(par3_mode, program, function_ptr+3, op_result, relative_base)
            function_ptr += _OP_LENGTH_4
        elif op_code == '03': # Input
            input_val = in_val
            #print('in: {}'.format(in_val))
            set_parameter(par1_mode, program, function_ptr+1, input_val, relative_base)
            function_ptr += _OP_LENGTH_2
        elif op_code == '04': # Output
            output = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            #print('out: {}'.format(output))
            function_ptr += _OP_LENGTH_2
            if output_cnt == 0:
                first_output = output
                output_cnt += 1
            else:
                return function_ptr, relative_base, first_output, output, False, program
        elif op_code == '05': # Jump if true
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            if par1 != 0:
                function_ptr = par2
            else:
                function_ptr += _OP_LENGTH_3
        elif op_code == '06': # Jump if false
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            if par1 == 0:
                function_ptr = par2
            else:
                function_ptr += _OP_LENGTH_3
        elif op_code == '07': # Less than
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            if par1 < par2:
                set_parameter(par3_mode, program, function_ptr+3, 1, relative_base)
            else:
                set_parameter(par3_mode, program, function_ptr+3, 0, relative_base)
            function_ptr += _OP_LENGTH_4
        elif op_code == '08': # Equals
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            par2 = get_parameter(par2_mode, program, function_ptr+2, relative_base)
            if par1 == par2:
                set_parameter(par3_mode, program, function_ptr+3, 1, relative_base)
            else:
                set_parameter(par3_mode, program, function_ptr+3, 0, relative_base)
            function_ptr += _OP_LENGTH_4
        elif op_code == '09': # Adjust relative base
            par1 = get_parameter(par1_mode, program, function_ptr+1, relative_base)
            relative_base += par1
            function_ptr += _OP_LENGTH_2
        elif op_code == '99': # Exit
            return function_ptr, 0, 0, 0, True, program
        else:
            raise ValueError('Unknown op_code "{}".'.format(op_code))
    return function_ptr, 0, 0, 0, True, program


def new_direction(turn, current_direction):
    turn = Direction(turn)
    if turn == Direction.LEFT:
        if current_direction == Direction.UP:
            return Direction.LEFT
        elif current_direction == Direction.LEFT:
            return Direction.DOWN
        elif current_direction == Direction.DOWN:
            return Direction.RIGHT
        elif current_direction == Direction.RIGHT:
            return Direction.UP
        else:
            raise ValueError('Unkown value: {}'.format(current_direction))
    elif turn == Direction.RIGHT:
        if current_direction == Direction.UP:
            return Direction.RIGHT
        elif current_direction == Direction.LEFT:
            return Direction.UP
        elif current_direction == Direction.DOWN:
            return Direction.LEFT
        elif current_direction == Direction.RIGHT:
            return Direction.DOWN
        else:
            raise ValueError('Unkown value: {}'.format(current_direction))
    else:
        raise ValueError('Unknown turn value: {}'.format(turn))


def translate_input(panel_val):
    if panel_val == '#':
        return 1
    elif panel_val == '.':
        return 0
    else:
        raise ValueError(panel_val)


def translate_output(out_val):
    if out_val == 0:
        return '.'
    elif out_val == 1:
        return '#'
    else:
        raise ValueError(out_val)


def run_program(starting_panel, d_program):
    curr_point = 0, 0
    halted = False
    direction = Direction.UP
    visited_panels = {(0, 0): starting_panel}
    function_ptr = 0
    rel = 0

    while halted == False:
        x, y = curr_point
        #print(curr_point)
        if curr_point not in visited_panels:
            visited_panels[curr_point] = '.'
        curr_color = visited_panels[curr_point]
        color = translate_input(curr_color)
        function_ptr, rel, new_color, turn, halted, d_program = intcode_machine(function_ptr, rel, color, d_program)
        #print(curr_point, translate_output(new_color), direction, Direction(turn), halted)
        if halted == False:
            # Paint the panel currently over
            visited_panels[curr_point] = translate_output(new_color)
            # Rotate
            direction = new_direction(turn, direction)
            # Move one step
            if direction == Direction.UP:
                y -= 1
            elif direction == Direction.DOWN:
                y += 1
            elif direction == Direction.LEFT:
                x -= 1
            elif direction == Direction.RIGHT:
                x += 1
            else:
                raise ValueError(direction)
            curr_point = x, y

    return visited_panels


with open("input.txt") as f:
    program = list(map(int, f.read().split(',')))
    d_program = dict()
    for i, val in enumerate(program):
        d_program[i] = val

    visited_panels = run_program('.', d_program.copy())
    print('Part1: {}'.format(len(visited_panels)))
    visited_panels = run_program('#', d_program.copy())
    max_x = 0
    max_y = 0
    for x, y in visited_panels.keys():
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    panels = list()
    for i in range(max_y+1):
        panels.append(['.']*(max_x+1))

    for (x, y), color in visited_panels.items():
        panels[y][x] = color

    print('Part2:')
    for line in panels:
        print(''.join(line))

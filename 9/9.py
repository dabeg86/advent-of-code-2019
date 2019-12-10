"""9.py."""

_OP_LENGTH_4 = 4
_OP_LENGTH_3 = 3
_OP_LENGTH_2 = 2

position = '0'
immediate = '1'
relative = '2'


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


def intcode_machine(program):
    """Intcode machine."""
    function_ptr = 0
    relative_base = 0
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
            input_val = int(input())
            set_parameter(par1_mode, program, function_ptr+1, input_val, relative_base)
            function_ptr += _OP_LENGTH_2
        elif op_code == '04': # Output
            print('output: ' + str(get_parameter(par1_mode, program, function_ptr+1, relative_base)))
            function_ptr += _OP_LENGTH_2
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
            break
        else:
            raise ValueError('Unknown op_code "{}".'.format(op_code))


with open("input.txt") as f:
    program = list(map(int, f.read().split(',')))
    d_program = dict()
    for i, val in enumerate(program):
        d_program[i] = val
    intcode_machine(d_program)

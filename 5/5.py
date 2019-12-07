"""5.py."""

_OP_LENGTH_4 = 4
_OP_LENGTH_2 = 2

position = '0'
immediate = '1'

def get_parameter(mode, program, function_ptr):
    if mode == position:
        return program[program[function_ptr]]
    elif mode == immediate:
        return program[function_ptr]
    else:
        raise ValueError('Unknown mode: {}'.format(mode))


def set_parameter(mode, program, function_ptr, value):
    if mode == position:
        program[program[function_ptr]] = value
    elif mode == immediate:
        program[function_ptr] = value
    else:
        raise ValueError('Unknown mode: {}'.format(mode))


def intcode_machine(program):
    """Intcode machine."""
    function_ptr = 0
    while(program[function_ptr] != 99):
        # Interpret the instruction
        instruction = str(program[function_ptr]).zfill(5)
        op_code = instruction[3:5]
        par1_mode = instruction[2]
        par2_mode = instruction[1]
        par3_mode = instruction[0]

        # Do the instruction
        if op_code == '01': # Addition
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            op_result = par1 + par2
            set_parameter(par3_mode, program, function_ptr+3, op_result)
            function_ptr += _OP_LENGTH_4
        elif op_code == '02': # Multiply
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            op_result = par1 * par2
            set_parameter(par3_mode, program, function_ptr+3, op_result)
            function_ptr += _OP_LENGTH_4
        elif op_code == '03': # Input
            input_val = int(input())
            set_parameter(par1_mode, program, function_ptr+1, input_val)
            function_ptr += _OP_LENGTH_2
        elif op_code == '04': # Output
            print(get_parameter(par1_mode, program, function_ptr+1))
            function_ptr += _OP_LENGTH_2
        elif op_code == '05': # Jump if true
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            if par1 != 0:
                function_ptr = par2
            else:
                function_ptr += 3
        elif op_code == '06': # Jump if false
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            if par1 == 0:
                function_ptr = par2
            else:
                function_ptr += 3
        elif op_code == '07': # Less than
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            if par1 < par2:
                set_parameter(par3_mode, program, function_ptr+3, 1)
            else:
                set_parameter(par3_mode, program, function_ptr+3, 0)
            function_ptr += _OP_LENGTH_4
        elif op_code == '08': # Equals
            par1 = get_parameter(par1_mode, program, function_ptr+1)
            par2 = get_parameter(par2_mode, program, function_ptr+2)
            if par1 == par2:
                set_parameter(par3_mode, program, function_ptr+3, 1)
            else:
                set_parameter(par3_mode, program, function_ptr+3, 0)
            function_ptr += _OP_LENGTH_4
        elif op_code == '99': # Exit
            break
        else:
            raise ValueError('Unknown op_code "{}".'.format(op_code))


with open("input.txt") as f:
    program = list(map(int, f.read().split(',')))
    intcode_machine(program)

"""2.py."""

_OP_LENGTH = 4


def find_noun_verb(exp_result):
    """Find the noun and verb."""
    with open("inputs.txt") as f:
        program = list(map(int, f.read().split(',')))

        for noun in range(100):
            for verb in range(100):
                result = intcode_machine(program.copy(), noun, verb)
                if (result == exp_result):
                    return noun, verb
    return 0, 0


def intcode_machine(program, noun, verb):
    """Intcode machine."""
    program[1] = noun
    program[2] = verb
    function_ptr = 0
    while(function_ptr < len(program)-_OP_LENGTH):
        op_code = program[function_ptr]
        val1 = program[program[function_ptr+1]]
        val2 = program[program[function_ptr+2]]
        if op_code == 1:
            op_result = val1 + val2
        elif op_code == 2:
            op_result = val1 * val2
        elif op_code == 99:
            break
        else:
            raise ValueError('Unknown op_code "{}".'.format(op_code))
        program[program[function_ptr+3]] = op_result

        function_ptr += _OP_LENGTH

    return program[0]


noun, verb = find_noun_verb(exp_result=19690720)
print(100 * noun + verb)

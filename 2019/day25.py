from aoc.input import read_input
from incode_computer import AsciiIntcodeComputer

_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]
_computer = AsciiIntcodeComputer(_program)

# needed path:
# south, west, take asterisk,
# east, north, east, north, north, take mutex,
# north, take prime number
# south, south, east, north, take mug
# south, west, south, east, east, south, east, east, north
_computer.run()
print(_computer.str_output)
while True:
    _computer.output.clear()
    command = input()
    if command == 'exit':
        break
    if command == 'restart':
        _computer = AsciiIntcodeComputer(_program)
        _computer.run()
        print(_computer.str_output)
        continue
    _computer.run(command)
    print(_computer.str_output)

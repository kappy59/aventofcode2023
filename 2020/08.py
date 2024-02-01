import main


def execute(lines):
    visited_lines = set()
    line = 0
    accumulator = 0
    while line < len(lines) and line not in visited_lines:
        visited_lines.add(line)
        line_offset = 1
        if lines[line][0:3] == "nop":
            ...
        elif lines[line][0:3] == "acc":
            accumulator += int(lines[line][4:])
        elif lines[line][0:3] == "jmp":
            line_offset = int(lines[line][4:])
        line += line_offset
    return line < len(lines), accumulator


@main.pretty_level
def part_1(lines):
    _, accumulator = execute(lines)
    return accumulator


@main.pretty_level
def part_2(lines):
    for line in range(len(lines)):
        if lines[line][0:3] == "nop":
            lines[line] = lines[line].replace("nop", "jmp")
        elif lines[line][0:3] == "jmp":
            lines[line] = lines[line].replace("jmp", "nop")
        else:
            continue

        infinite_loop, accumulator = execute(lines)
        if not infinite_loop:
            return accumulator

        if lines[line][0:3] == "nop":
            lines[line] = lines[line].replace("nop", "jmp")
        elif lines[line][0:3] == "jmp":
            lines[line] = lines[line].replace("jmp", "nop")

    return 0

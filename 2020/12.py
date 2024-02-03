import main

directions = ["E", "S", "W", "N"]
moves = [1, -1j, -1, 1j]


@main.pretty_level
def part_1(lines):
    dir_idx = 0
    pos = 0
    for line in lines:
        if line[0] == "F":
            line = directions[dir_idx] + line[1:]

        if line[0] in directions:
            pos += int(line[1:]) * moves[directions.index(line[0])]

        elif line[0] == "R":
            dir_idx = (dir_idx + int(line[1:]) // 90) % 4
        elif line[0] == "L":
            dir_idx = (dir_idx - int(line[1:]) // 90) % 4
    return int(abs(pos.real) + abs(pos.imag))


@main.pretty_level
def part_2(lines):
    waypoint = 10 + 1j
    pos = 0

    for line in lines:
        if line[0] == "F":
            pos += int(line[1:]) * waypoint

        if line[0] in directions:
            waypoint += int(line[1:]) * moves[directions.index(line[0])]

        elif line[0] == "R":
            waypoint *= pow(-1j, int(line[1:]) // 90)
        elif line[0] == "L":
            waypoint *= pow(1j, int(line[1:]) // 90)

    return int(abs(pos.real) + abs(pos.imag))

import main


def count_energized_cells(lines, starting_beam):
    beams = [starting_beam]
    cells = [[[] for _ in range(len(lines))] for _ in range(len(lines[0]))]

    while beams:
        beam = beams[0]
        while True:
            # break if out of range
            if (
                beam[0] < 0
                or beam[0] >= len(cells)
                or beam[1] < 0
                or beam[1] >= len(cells[0])
            ):
                break

            # break if loop detected : loop is same cell and same direction !!!
            if beam[2] in cells[beam[0]][beam[1]]:
                break

            # flag the cell with the direction (memory)
            cells[beam[0]][beam[1]].append(beam[2])

            # next move.
            # If splitter, current beam is continued as one of the two possible next beam status and a new one is created at the other next beam status
            # This is ugly
            if beam[2] == "E":
                if lines[beam[0]][beam[1]] in ".-":
                    beam[1] += 1
                elif lines[beam[0]][beam[1]] in "\\":
                    beam[0] += 1
                    beam[2] = "S"
                elif lines[beam[0]][beam[1]] in "/":
                    beam[0] -= 1
                    beam[2] = "N"
                elif lines[beam[0]][beam[1]] in "|":
                    beams.append([beam[0] + 1, beam[1], "S"])
                    beam[0] -= 1
                    beam[2] = "N"
            elif beam[2] == "W":
                if lines[beam[0]][beam[1]] in ".-":
                    beam[1] -= 1
                elif lines[beam[0]][beam[1]] in "\\":
                    beam[0] -= 1
                    beam[2] = "N"
                elif lines[beam[0]][beam[1]] in "/":
                    beam[0] += 1
                    beam[2] = "S"
                elif lines[beam[0]][beam[1]] in "|":
                    beams.append([beam[0] + 1, beam[1], "S"])
                    beam[0] -= 1
                    beam[2] = "N"
            elif beam[2] == "N":
                if lines[beam[0]][beam[1]] in ".|":
                    beam[0] -= 1
                elif lines[beam[0]][beam[1]] in "\\":
                    beam[1] -= 1
                    beam[2] = "W"
                elif lines[beam[0]][beam[1]] in "/":
                    beam[1] += 1
                    beam[2] = "E"
                elif lines[beam[0]][beam[1]] in "-":
                    beams.append([beam[0], beam[1] + 1, "E"])
                    beam[1] -= 1
                    beam[2] = "W"
            elif beam[2] == "S":
                if lines[beam[0]][beam[1]] in ".|":
                    beam[0] += 1
                elif lines[beam[0]][beam[1]] in "\\":
                    beam[1] += 1
                    beam[2] = "E"
                elif lines[beam[0]][beam[1]] in "/":
                    beam[1] -= 1
                    beam[2] = "W"
                elif lines[beam[0]][beam[1]] in "-":
                    beams.append([beam[0], beam[1] + 1, "E"])
                    beam[1] -= 1
                    beam[2] = "W"

        # Looped ? Out of bounds ? In any case dismiss beam a continue to next one
        beams.pop(0)

    # cell is energize if at least one "beamdirection" has been flags in it
    return sum(
        [
            sum([1 for c in range(len(cells[0])) if len(cells[r][c]) > 0])
            for r in range(len(cells))
        ]
    )


@main.pretty_level
def part_1(lines):
    return count_energized_cells(lines, [0, 0, "E"])


@main.pretty_level
def part_2(lines):
    best_total = 0
    for r in range(len(lines)):
        beam = [r, 0, "E"]
        best_total = max(best_total, count_energized_cells(lines, beam))
        beam = [r, len(lines[0]) - 1, "W"]
        best_total = max(best_total, count_energized_cells(lines, beam))

    for c in range(len(lines[0])):
        beam = [0, c, "S"]
        best_total = max(best_total, count_energized_cells(lines, beam))
        beam = [len(lines) - 1, c, "N"]
        best_total = max(best_total, count_energized_cells(lines, beam))

    return best_total

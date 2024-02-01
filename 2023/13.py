import main


def find_symmetry(pattern, ignore_row=None, ignore_col=None):
    """Find the symmetry.
    The ignore_row, ignore_cols are for part 2 only.
    Attention to the +1 offset between indexes and rows/cols numbers"""
    row = None
    col = None

    # horizontal sym
    for i in range(0, len(pattern) - 1):
        if ignore_row and i + 1 == ignore_row:
            continue
        size = min(i + 1, len(pattern) - i - 1, len(pattern) // 2)
        tmp = None if i - size < 0 else i - size
        if pattern[i:tmp:-1] == pattern[i + 1 : i + size + 1]:
            row = i + 1

    # vertical sym
    pattern_T = [list(sublist) for sublist in zip(*pattern)]
    for i in range(0, len(pattern_T) - 1):
        if ignore_col and i + 1 == ignore_col:
            continue
        size = min(i + 1, len(pattern_T) - i - 1, len(pattern_T) // 2)
        tmp = None if i - size < 0 else i - size
        if pattern_T[i:tmp:-1] == pattern_T[i + 1 : i + size + 1]:
            col = i + 1

    return row, col


def patterns(lines):
    pattern = []
    for l in lines:
        if not l:
            yield pattern
            pattern = []
        else:
            pattern.append(list(l))
    yield pattern


@main.pretty_level
def part_1(lines):
    total = 0
    for pattern in patterns(lines):
        row, col = find_symmetry(pattern)
        total += 100 * (row if row else 0) + (col if col else 0)

    return total


@main.pretty_level
def part_2(lines):
    total = 0
    for pattern in patterns(lines):
        row, col = find_symmetry(pattern)
        new_row = new_col = None

        # Brute force the smudge positions

        for r in range(len(pattern)):
            # Stop if something new found
            if new_row or new_col:
                break
            for c in range(len(pattern[0])):
                if pattern[r][c] == ".":
                    # Try with smudge at [r][c]
                    pattern[r][c] = "#"
                    new_row, new_col = find_symmetry(pattern, row, col)
                    # Stop if something new found
                    if new_row or new_col:
                        break
                    # Reset pattern
                    pattern[r][c] = "."

                else:
                    # Try with smudge at [r][c]
                    pattern[r][c] = "."
                    new_row, new_col = find_symmetry(pattern, row, col)
                    # Stop if something new found
                    if new_row or new_col:
                        break
                    # Reset pattern
                    pattern[r][c] = "#"

        total += 100 * (new_row if new_row else 0) + (new_col if new_col else 0)
    return total

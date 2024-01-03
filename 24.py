import main


def stone(line):
    # a stone defines a line in 3D space with a known point and a vector
    # Equation of the line is
    #  * X = P[x] + t . V[x]
    #  * Y = P[y] + t . V[y]
    #  * Z = P[z] + t . V[z]
    position, velocity = line.split("@")
    p = dict(zip("xyz", list(map(int, position.split(",")))))
    v = dict(zip("xyz", list(map(int, velocity.split(",")))))
    return p, v


@main.pretty_level
def part_1(lines):
    total = 0

    # LOW = 7
    # HIGH = 27
    LOW = 200000000000000
    HIGH = 400000000000000

    for stone_1 in range(len(lines) - 1):
        for stone_2 in range(stone_1 + 1, len(lines)):
            p1, v1 = stone(lines[stone_1])
            p2, v2 = stone(lines[stone_2])

            # We consider 2D lines with equations:
            # * line_1
            #   * X = P1[x] + t1 . V1[x]
            #   * Y = P1[y] + t1 . V1[y]
            # * line_2
            #   * X = P2[x] + t2 . V2[x]
            #   * Y = P2[y] + t2 . V2[y]

            # if lines do not intersect or equals (cross product == 0): continue
            if v1["x"] * v2["y"] - v1["y"] * v2["x"] == 0:
                continue

            # Two lines intersect at the position where
            # * X = P1[x] + t1 . V1[x] = P2[x] + t2 . V2[x]
            # * Y = P1[y] + t1 . V1[y] = P2[y] + t2 . V2[y]

            # From there we can compute t1
            #      V2[x] . (P1[y] - P2[y]) - V2[y] . (P1[x] - P2[x])
            # t1 = -------------------------------------------------
            #              (V1[x] . V2[y]) - (V1[y] . V2[x])
            #
            # and then deduce X, Y of the intersection
            # and then deduce t2
            t1 = (v2["x"] * (p1["y"] - p2["y"]) - v2["y"] * (p1["x"] - p2["x"])) / (
                v1["x"] * v2["y"] - v1["y"] * v2["x"]
            )
            x = p1["x"] + t1 * v1["x"]
            y = p1["y"] + t1 * v1["y"]
            t2 = (x - p2["x"]) / v2["x"] if v2["x"] else (y - p2["y"]) / v2["y"]

            if LOW <= x <= HIGH and LOW <= y <= HIGH and t1 > 0 and t2 > 0:
                total += 1

    return total


def jordan_gauss_reduction(matrix, eps=1.0 / (10**10)):
    for r in range(len(matrix)):
        if abs(matrix[r][r]) <= eps:
            for i in range(r + 1, len(matrix)):
                if matrix[i][r] > eps:
                    matrix[i], matrix[r] = matrix[r], matrix[i]
                    break
        if abs(matrix[r][r]) <= eps:
            raise ZeroDivisionError("Cannot solve this stuff")

        # normalize row (make the 1st non 0 to become a 1)
        for c in range(len(matrix[0]) - 1, r - 1, -1):
            matrix[r][c] /= matrix[r][r]

        # eliminate coefficient in other equations
        for r2 in range(len(matrix)):
            if r2 != r:
                for c in range(len(matrix[0]) - 1, r - 1, -1):
                    matrix[r2][c] -= matrix[r][c] * matrix[r2][r]

    return 0


import z3


@main.pretty_level
def part_2(lines):
    P = {}
    V = {}
    for axis in "xyz":
        P[axis] = z3.Int(f"P{axis}")
        V[axis] = z3.Int(f"V{axis}")

    solver = z3.Solver()
    for i in range(3):
        p, v = stone(lines[i])
        t = z3.Int(f"t{i}")
        for axis in "xyz":
            solver.add(p[axis] + t * v[axis] == P[axis] + t * V[axis])

    assert solver.check() == z3.sat
    for axis in "xyz":
        print(f"p{axis} == {solver.model().eval(P[axis])}")
    for axis in "xyz":
        print(f"v{axis} == {solver.model().eval(V[axis])}")

    return solver.model().eval(P["x"] + P["y"] + P["z"])

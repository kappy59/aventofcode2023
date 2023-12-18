import main

# from PIL import Image


# def bmp_visualize(grid, size_r, size_c, name):
#     for l in grid:
#         print("".join(l))

#     img = Image.new(mode="L", size=(size_c, size_r))
#     for r in range(size_r):
#         for c in range(size_c):
#             if grid[r][c] == "#":
#                 img.putpixel((c, r), 255)
#             if grid[r][c] == ".":
#                 img.putpixel((c, r), 80)
#             if grid[r][c] == "@":
#                 img.putpixel((c, r), 160)
#             if grid[r][c] == " ":
#                 img.putpixel((c, r), 0)

#     img.save(name)


def compute2(input):
    # the input describes the perimeter of a polygon
    # Each of the vertices of the polygon are lattices (they lie on the grid)
    # We can use the shoelace theorem to compute the area of the polygon
    #    A = 1/2 * (x0y1 - x1y0 + x1y2 - x2y1 + ... )
    # https://www.theoremoftheday.org/GeometryAndTrigonometry/Shoelace/TotDShoelace.pdf
    # Pick's theorem also compute the area of the polygon
    #    A = I + B/2 - 1   (where I is the nb of lattices inside the polygon, B the nb of lattices in the boundary)
    # In our case, the entire perimeter is composed of lattices, thus B == the perimeter of the polygon (i.e. the sum of the sizes of each move from the input)
    #
    # Attention: the area calculated by the shoelace theorem does not take into account the thickness of our contour (digging is 1 meter wide)
    # In our case, that means the shoelace theorem computes the nb of lattices within the polygon - i.e the 'I' of the Pick's theorem
    # We want I + B
    #   from Pick  => I = A(shoelace) - B/2 + 1
    #              => I + B = A(shoelace) + B/2 + 1

    vertices = [(0, 0)]
    contour = 0
    for line in input:
        match (line[0]):
            case "R":
                vertices.append((vertices[-1][0], vertices[-1][1] + line[1]))
            case "D":
                vertices.append((vertices[-1][0] + line[1], vertices[-1][1]))
            case "U":
                vertices.append((vertices[-1][0] - line[1], vertices[-1][1]))
            case "L":
                vertices.append((vertices[-1][0], vertices[-1][1] - line[1]))
        contour += line[1]

    area = 0
    for i in range(len(vertices) - 1):
        area += (vertices[i][1] * vertices[i + 1][0]) - vertices[i][0] * vertices[
            i + 1
        ][1]

    area //= 2

    return area + contour // 2 + 1


@main.pretty_level
def part_1(lines):
    input = [(line[0], int(line.split(" ")[1])) for line in lines]
    return compute2(input)


@main.pretty_level
def part_2(lines):
    directions = "RDLU"
    input = [(directions[int(line[-2])], int(line[-7:-2], 16)) for line in lines]
    return compute2(input)

import main


@main.pretty_level
def part_1(lines):
    tree = {}
    # Construct a tree of contenanship of the bags (ignore the numbers)
    for line in lines:
        bag, subbags = line.strip(".").split(" bags contain ")
        tree[bag] = set()

        if subbags == "no other bags":
            continue

        subbags = subbags.split(", ")
        for subbag in subbags:
            subbag = subbag.split(" ")
            # ignore 1st split (the nb) and the last (bags or bag)
            tree[bag].add(" ".join(subbag[1:-1]))

    # Reduce the tree
    keep_going = True
    while keep_going:
        # While the previous loop produced something => keep going
        keep_going = False
        for bag, subbags in tree.items():
            # if the shiny gold is in the list of subbags => we skip the bag because we already have our answer : it can contain shiny gold
            if "shiny gold" in subbags:
                continue

            # if not we will use a new subbag list created by replacing all the subbags by their own subbags (subsubbag)
            new_subbags = set()
            for subbag in subbags:
                if len(tree[subbag]) > 0:
                    keep_going = True
                    for subsubbag in tree[subbag]:
                        new_subbags.add(subsubbag)
            tree[bag] = new_subbags

    # After the reduction, all bags that still have a non empty set of subbags WILL HAVE shiny gold in this set
    return sum([len(x) != 0 for x in tree.values()])


@main.pretty_level
def part_2(lines):
    tree = {}
    # Construct a tree of contenanship of the bags. This time a list of subbags (not a set) and we add as many as needed
    for line in lines:
        bag, subbags = line.strip(".").split(" bags contain ")
        tree[bag] = []

        if subbags == "no other bags":
            continue

        subbags = subbags.split(", ")
        for subbag in subbags:
            subbag = subbag.split(" ")
            for _ in range(int(subbag[0])):
                tree[bag].append(" ".join(subbag[1:-1]))

    # Compute the schbims
    # Here we have a counter of bags and within the loop we will increase the counter by the nb of subbags in shiny gold and then replace each of the subbags by their own subsubbags
    nb_bags = 0
    while len(tree["shiny gold"]):
        nb_bags += len(tree["shiny gold"])
        new_content = []
        for subbag in tree["shiny gold"]:
            new_content += tree[subbag]
        tree["shiny gold"] = new_content
    return nb_bags

from math import lcm, prod
import main

LOW = 0
HIGH = 1


def push_button(modules):
    signals = [{"src": "button", "type": LOW, "dest": "broadcaster"}]
    signals_history = []
    while signals:
        s = signals.pop(0)
        signals_history.append(s)

        match modules[s["dest"]]["type"]:
            case "%":
                if s["type"] == LOW:
                    modules[s["dest"]]["pos"] = (1 + modules[s["dest"]]["pos"]) % 2
                    for dest in modules[s["dest"]]["dests"]:
                        signals.append(
                            {
                                "src": s["dest"],
                                "type": modules[s["dest"]]["pos"],
                                "dest": dest,
                            }
                        )
            case "&":
                modules[s["dest"]]["inputs_memory"][s["src"]] = s["type"]
                for dest in modules[s["dest"]]["dests"]:
                    signals.append(
                        {
                            "src": s["dest"],
                            "type": LOW
                            if all(
                                [
                                    mem == HIGH
                                    for mem in modules[s["dest"]][
                                        "inputs_memory"
                                    ].values()
                                ]
                            )
                            else HIGH,
                            "dest": dest,
                        }
                    )
            case _:
                for dest in modules[s["dest"]]["dests"]:
                    signals.append({"src": s["dest"], "type": LOW, "dest": dest})

    return modules, signals_history


def parse_input(lines):
    modules = {"button": {"type": "button", "dests": ["broadcaster"]}}

    for line in lines:
        module_type_name, dest_modules = line.split(" -> ")
        module_name = module_type_name[1:]
        module_type = module_type_name[0]
        if module_type not in "%&":
            module_name = module_type = module_type_name
        dest_modules = [x.strip() for x in dest_modules.split(",") if x]

        # add a new module
        modules[module_name] = {"pos": LOW, "type": module_type, "dests": dest_modules}

    # Fix the missing modules:  i.e modules that do not send signals (like output in sample #2)
    loose_ends = []
    for module_name, module in modules.items():
        for dest in module["dests"]:
            if not dest in modules:
                loose_ends.append(dest)
    for loose_end in loose_ends:
        modules[loose_end] = {"type": "loose end", "dests": []}

    # Complete the input connections
    for module_name, module in modules.items():
        for dest in module["dests"]:
            if not dest in modules:
                modules[dest] = {"type": "loose end", "dests": []}
            if modules[dest]["type"] == "&":
                if not "inputs_memory" in modules[dest]:
                    modules[dest]["inputs_memory"] = {}
                modules[dest]["inputs_memory"][module_name] = LOW

    return modules


@main.pretty_level
def part_1(lines):
    # parse modules
    modules = parse_input(lines)

    signals = []
    for _ in range(1000):
        modules, signals_iter = push_button(modules)
        signals += signals_iter
    return sum([s["type"] == LOW for s in signals]) * sum(
        [s["type"] == HIGH for s in signals]
    )


@main.pretty_level
def part_2(lines):
    # parse modules
    all_modules = parse_input(lines)

    # First I tried to brute force the solution. After 10 minutes it was clear it would not converge
    #
    # When looking closely at the all_modules chain, it appears that:
    #  - the "rx" module is a loose-end. It has exactly one conjunction node as input (in my case "cs"). Let's call it before_rx
    #  - This conjunction node has exactly 4 conjunction nodes as input (in my case "hn", "kh", "lz" and "tg"). Let's call them before_before_rx
    #  - Each of these for conjunctions has exactly 1 conjunction node as input (in my case "pl", "sd", "sk" and "zv"). Let's call them end_of_loops
    #  - "broadcaster" has exactly 4 destination nodes. Lets call them head_of_loops
    #  - each of the dests of broadcaster is the beginning of a loop ending with a different end_of_loops node
    #  - these loops are independant (meaning no node is common here)
    #
    # If I can make these assumptions, then the problem is reduced to finding a repetition of pattern in the statuses of [toggle_in_loop and end_of_loops] with hopefully the end_of_loops receiving HIGH at this step. In this case, they will send LOW to the before_before_rx, that will cause the before_before_rx to send a HIGH signal to the before_rx that will in turn send a LOW signal to rx
    #
    # Now, in each loop of modules, we have a signals policy describing the behaviour of all the toggles
    # Empirically it seems that the number of button pushes to reach the initial status of all flipflops and the number of button pushes to send LOW signal to the before_rx for each loop are equals.
    # Either I missed something or it is a happy coincidence and it can be assumed (just like the former assumptions)

    before_rx = []
    for module_name, module in all_modules.items():
        if "rx" in module["dests"]:
            before_rx.append(module_name)

    assert len(before_rx) == 1
    before_rx = before_rx[0]

    before_before_rx = []
    for module_name, module in all_modules.items():
        if before_rx in module["dests"]:
            before_before_rx.append(module_name)

    assert len(before_before_rx) == 4
    end_of_loops = []
    for before_before in before_before_rx:
        tmp = []
        for module_name, module in all_modules.items():
            if before_before in module["dests"]:
                tmp.append(module_name)
        assert len(tmp) == 1
        end_of_loops.append(tmp[0])

    start_of_loops = all_modules["broadcaster"]["dests"]

    loops = {}
    for origin in start_of_loops:
        loop = set([origin])
        while True:
            updated_loop = set([])
            for l in loop:
                updated_loop.update(all_modules[l]["dests"])
            if len(updated_loop) == len(loop):
                break
            loop.update(updated_loop)

        # assert that from each of the start_of_loop we got to rx
        assert "rx" in loop
        loop.remove("rx")

        # assert that from each of the start_of_loop we got to rx through before_rx
        assert before_rx in loop
        loop.remove(before_rx)

        # assert that from each of the start_of_loop we got to rx through only one of the end_of_loops
        assert len(loop & set(end_of_loops)) == 1

        loops[origin] = loop

    # assert that no loops have common nodes
    for i in range(len(start_of_loops) - 1):
        for j in range(i + 1, len(start_of_loops)):
            assert len(loops[start_of_loops[i]] & loops[start_of_loops[j]]) == 0

    print("assertions true")

    # prepare submodules dicts that contains each only one loop
    loop_modules = {
        start_of_loop: {
            "button": {"type": "button", "dests": ["broadcaster"]},
            "broadcaster": {"type": "button", "dests": [start_of_loop]},
            before_rx: {"type": "loose end", "dests": []},
            **(dict(zip(loop, [all_modules[l] for l in loop]))),
        }
        for start_of_loop, loop in loops.items()
    }

    # We now know there are for module loops in the total model
    cnt = 1
    loops_sizes = {}
    triggers = {}
    while True:
        for start_of_loop, modules in loop_modules.items():
            modules, signals_history = push_button(modules)
            if (
                len(
                    [
                        signal
                        for signal in signals_history
                        if signal["dest"] == before_rx and signal["type"] == HIGH
                    ]
                )
                == 1
            ):
                if start_of_loop not in triggers:
                    triggers[start_of_loop] = cnt
            if sum([m["pos"] for m in modules.values() if m["type"] == "%"]) == 0:
                if start_of_loop not in loops_sizes:
                    loops_sizes[start_of_loop] = cnt

        cnt += 1
        if len(loops_sizes) == len(start_of_loops) == len(triggers):
            break

    assert triggers == loops_sizes

    return prod(list(loops_sizes.values()))

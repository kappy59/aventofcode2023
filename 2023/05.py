import functools
import main


def get_seeds_to_location_mapping(lines):
    parsed_inputs = {}

    current_map = ""
    for line in lines:
        if not line:
            current_map = ""
        elif line.endswith("map:"):
            current_map = line.split(" ")[0]
            parsed_inputs[current_map] = []
        else:
            tmp = [int(x) for x in line.split(" ")]
            parsed_inputs[current_map].append(
                {
                    "src start": tmp[1],
                    "src end": tmp[1] + tmp[2],
                    "dst start": tmp[0],
                    "dst end": tmp[0] + tmp[2],
                    "offset": tmp[0] - tmp[1],
                }
            )
    for k, v in parsed_inputs.items():
        parsed_inputs[k] = sorted(v, key=lambda x: x["src start"])
        if parsed_inputs[k][0]["src start"] != 0:
            tmp = [
                {
                    "src start": 0,
                    "src end": parsed_inputs[k][0]["src start"],
                    "dst start": 0,
                    "dst end": parsed_inputs[k][0]["src start"],
                    "offset": 0,
                },
            ]
            tmp.extend(parsed_inputs[k])
            parsed_inputs[k] = tmp

    def iterate(intervals, mapping):
        new_intervals = []

        for interval in intervals:
            idx = 0

            while idx <= len(mapping):
                if idx == len(mapping):
                    new_intervals.append(interval)
                    break

                # if the mapping interval is too low for current interval => ignore
                if mapping[idx]["src end"] <= interval["dst start"]:
                    idx += 1
                    continue  # go to next interval in the mapping

                # if the mapping interval is too high for the current interval => dumb mapping A=>A and go to next interval
                elif mapping[idx]["src start"] >= interval["dst end"]:
                    new_intervals.append(interval)
                    break  # current interval done => out of the while loop

                # if the mapping interval starts inside the current interval but not at start => split up the current interval in 2 parts: first is dumb mapping then loop
                elif interval["dst start"] < mapping[idx]["src start"]:
                    size = mapping[idx]["src start"] - interval["dst start"]
                    new_intervals.append(
                        {
                            "src start": interval["src start"],
                            "src end": interval["src start"] + size,
                            "dst start": interval["dst start"],
                            "dst end": interval["dst start"] + size,
                        }
                    )
                    interval["src start"] = interval["src start"] + size
                    interval["dst start"] = interval["dst start"] + size
                    continue

                # if the mapping interval starts before the current interval (including start of the current interval) => this is good
                elif mapping[idx]["src start"] <= interval["dst start"]:
                    # if it ends after the end of the current interval => current interval is fully mapped here
                    if interval["dst end"] <= mapping[idx]["src end"]:
                        new_intervals.append(
                            {
                                "src start": interval["src start"],
                                "src end": interval["src end"],
                                "dst start": interval["dst start"]
                                + mapping[idx]["offset"],
                                "dst end": interval["dst end"] + mapping[idx]["offset"],
                            }
                        )
                        break

                    else:
                        overlap = interval["dst end"] - mapping[idx]["src end"]
                        new_intervals.append(  # TODO: This is not finished in parsing here !!!
                            {
                                "src start": interval["src start"],
                                "src end": interval["src end"] - overlap,
                                "dst start": interval["dst start"]
                                + mapping[idx]["offset"],
                                "dst end": interval["dst end"]
                                + mapping[idx]["offset"]
                                - overlap,
                            }
                        )
                        interval["src start"] = interval["src end"] - overlap
                        interval["dst start"] = interval["dst end"] - overlap
                        continue

        return sorted(new_intervals, key=lambda x: x["src start"])

    global_map = parsed_inputs["seed-to-soil"]
    global_map = iterate(global_map, parsed_inputs["soil-to-fertilizer"])
    global_map = iterate(global_map, parsed_inputs["fertilizer-to-water"])
    global_map = iterate(global_map, parsed_inputs["water-to-light"])
    global_map = iterate(global_map, parsed_inputs["light-to-temperature"])
    global_map = iterate(global_map, parsed_inputs["temperature-to-humidity"])
    global_map = iterate(global_map, parsed_inputs["humidity-to-location"])
    return global_map


def seed_location(seed, mapping):
    for interval in mapping:
        if interval["src start"] <= seed < interval["src end"]:
            return interval["dst start"] + seed - interval["src start"]
    return 0


@main.pretty_level
def part_1(lines):
    seeds = [int(s) for s in lines[0].split(":")[1].split(" ") if s]
    mapping = get_seeds_to_location_mapping(lines[1:])
    print(seeds)
    print([seed_location(s, mapping) for s in seeds])
    return min([seed_location(s, mapping) for s in seeds])


@main.pretty_level
def part_2(lines):
    seeds_intervals = []
    tmp = [int(s) for s in lines[0].split(":")[1].split(" ") if s]
    for i in range(0, len(tmp), 2):
        seeds_intervals.append({"start": tmp[i], "end": tmp[i] + tmp[i + 1]})

    mapping = get_seeds_to_location_mapping(lines[1:])
    best_location = seed_location(seeds_intervals[0]["start"], mapping)

    for seed_interval in seeds_intervals:
        best_location = min(
            best_location, seed_location(seed_interval["start"], mapping)
        )
        for interval in mapping:
            if seed_interval["start"] <= interval["src start"] < seed_interval["end"]:
                # print(
                #     f"{seed_interval}  => {interval['src start']} - {interval['src end']} => {interval['dst start']}"
                # )
                best_location = min(best_location, interval["dst start"])
    return best_location

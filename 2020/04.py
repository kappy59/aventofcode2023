import itertools
import regex as re

import main


@main.pretty_level
def part_1(lines):
    nb_valid = 0
    passports = [
        list(group) for k, group in itertools.groupby(lines, lambda x: not x) if not k
    ]
    passports = [" ".join(passport) for passport in passports]
    for passport in passports:
        params = {x.split(":")[0]: x.split(":")[1] for x in passport.split(" ")}
        params["cid"] = "ignore"
        if all(
            [
                k in params
                for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
            ]
        ):
            nb_valid += 1
    return nb_valid


@main.pretty_level
def part_2(lines):
    nb_valid = 0
    passports = [
        list(group) for k, group in itertools.groupby(lines, lambda x: not x) if not k
    ]
    passports = [" ".join(passport) for passport in passports]
    for passport in passports:
        params = {x.split(":")[0]: x.split(":")[1] for x in passport.split(" ")}
        params["cid"] = "ignore"

        if not all(
            [
                k in params
                for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
            ]
        ):
            continue

        if (
            len(re.findall(r"^(\d{4})$", params["byr"])) != 1
            or int(params["byr"]) < 1920
            or int(params["byr"]) > 2002
        ):
            continue

        if (
            len(re.findall(r"^(\d{4})$", params["iyr"])) != 1
            or int(params["iyr"]) < 2010
            or int(params["iyr"]) > 2020
        ):
            continue

        if (
            len(re.findall(r"^(\d{4})$", params["eyr"])) != 1
            or int(params["eyr"]) < 2020
            or int(params["eyr"]) > 2030
        ):
            continue

        if params["hgt"][-2:] == "cm":
            hgt = int(params["hgt"][:-2])
            if str(hgt) != params["hgt"][:-2] or hgt < 150 or hgt > 193:
                continue
        elif params["hgt"][-2:] == "in":
            hgt = int(params["hgt"][:-2])
            if str(hgt) != params["hgt"][:-2] or hgt < 59 or hgt > 76:
                continue
        else:
            continue

        if len(re.findall(r"^(#[0-9a-f]{6})$", params["hcl"])) != 1:
            continue

        if not params["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            continue

        if len(re.findall(r"^(\d{9})$", params["pid"])) != 1:
            continue

        nb_valid += 1

    return nb_valid

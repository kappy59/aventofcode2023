import argparse
import importlib
import os
import re
import requests

from config import config


def main():
    parser = argparse.ArgumentParser(prog="Avent of code")
    parser.add_argument("-l", "--level", required=False, default=None)
    parser.add_argument("-f", "--use_fixtures", required=False, action="store_true")
    parser.add_argument("-1", "--part_1", required=False, action="store_true")
    parser.add_argument("-2", "--part_2", required=False, action="store_true")
    args = parser.parse_args()

    if args.level:
        config.level_to_run = args.level
    else:
        levels_available = [f for f in os.listdir(".") if re.search(r"^\d{2}\.py$", f)]
        print(f"levels_available : {levels_available}")
        config.level_to_run = max(
            [int(l.removesuffix(".py")) for l in levels_available]
        )

    config.level_to_run_str = f"{int(config.level_to_run):02d}"

    print(f"Loading {config.level_to_run_str}.py\n")
    level = importlib.import_module(config.level_to_run_str)

    config.use_fixtures = args.use_fixtures

    if not args.part_2 or args.part_1 and args.part_2:
        level.part_1()

    if not args.part_1 or args.part_1 and args.part_2:
        level.part_2()


def send_answer(level: int, answer: str) -> str:
    url = f"{config.url}/{str(config.level_to_run)}/answer"
    data = {"level": level, "answer": answer}

    print(f"Sending response {data} to {url}")

    response = requests.post(url=url, cookies=config.cookies, data=data)

    print(response.status_code)
    assert response.text.find("That's not the right answer") == -1
    # print(response.text)
    print("That was right!")


def load_data() -> str:
    url = f"{config.url}/{str(config.level_to_run)}/input"
    print(f"Loading {url}")

    response = requests.get(url=url, cookies=config.cookies)
    return response.content.decode("utf-8")


def load_fixtures(name: str) -> str:
    print(f"fixtures/level_{config.level_to_run_str}_{name}.txt")
    try:
        with open(f"fixtures/level_{config.level_to_run_str}_{name}.txt") as fixture:
            return fixture.read()
    except FileExistsError as e:
        print("Fixture file not found")
        return ""


def pretty_level(func):
    def wrapper():
        global config

        print(f"Entering {func.__name__}")
        input = load_fixtures(func.__name__) if config.use_fixtures else load_data()
        input = input.splitlines()
        res = func(input)
        print(f"Found result {res}")
        if not config.use_fixtures:
            send_answer(int(func.__name__.split("_")[1]), res)
        print(f"Leaving {func.__name__}\n")

    return wrapper


if __name__ == "__main__":
    main()

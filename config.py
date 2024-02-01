import os


class Config:
    base_url = "https://adventofcode.com/{year}/day/{day}"
    cookies = {}

    def __init__(self):
        self.cookies["session"] = os.getenv("AVANT_OF_CODE_SESSION_COOKIE")


config = Config()

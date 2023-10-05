import json
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)


class Server:
    def __init__(self) -> None:
        self.HOST: str = getenv("HOST")  # type: ignore

    def get_root(self) -> dict:
        res: requests.Response = requests.get(self.HOST)
        return res.json()

    def make_move(self, turn, move, timestamp) -> None:
        params = {
            "turn": turn,
            "from": move["from"],
            "to": move["to"],
            "time": timestamp,
        }

        requests.patch(self.HOST + "game", params=params)

    def reset(self) -> dict:
        # used to reset to a new game
        res: requests.Response = requests.put(self.HOST + "game")
        return json.loads(res.text)

    def get_game(self) -> dict:
        res: requests.Response = requests.get(self.HOST + "game")
        return json.loads(res.text)

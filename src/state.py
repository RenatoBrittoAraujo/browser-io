from src.util import *


class State:
    state = {}

    def __init__(self):
        self.state = {}

    def to_json(self):
        return json.dumps(
            self.state, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

    def save(self):
        save_file("app_state.json", self.to_json())

    def load(self):
        if not is_file("app_state.json"):
            return
        self.state = load_json("app_state.json")

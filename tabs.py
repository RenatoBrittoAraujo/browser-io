from src.util import *


def get_mozilla_folder():
    _, o, _ = cmd("find / -name '*.mozilla' -type d")
    print(o)
    _, user_folder, _ = cmd("echo ~")
    user_folder = user_folder.strip()
    resp = None
    for candidate in o.splitlines():
        candidate = candidate.strip()
        if candidate.startswith(user_folder):
            resp = candidate
            break
    if resp is None:
        raise Exception("the '.mozilla' folder was not found")
    return resp


def get_session_file(mozilla_folder):
    _, o, _ = cmd(f"find {mozilla_folder} -name '*recovery.jsonlz4'", debug=True)
    o = o.strip()
    return o


def get_session_recovery_data(mozilla_folder):
    # lz4jsoncat $profile/sessionstore-backups/recovery.jsonlz4 \
    # | jq -r '.windows[] | .tabs[] | (.index - 1) as $i | .entries[$i] | .title, .url, ""'

    recovery_file = get_session_file(mozilla_folder)
    print(f"recovery_file = {recovery_file}")
    _, o, _ = cmd(
        f"lz4jsoncat {recovery_file} | jq -r '.windows[] | .tabs[] | (.index - 1) as $i | .entries[$i] | .title, .url, "
        "'"
    )
    return o


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


if __name__ == "__main__":
    s = State()
    s.load()
    print(s.state)
    if "jose" in s.state:
        del s.state["jose"]
    else:
        s.state["jose"] = 1
    s.state["maria"] = 2
    s.save()
    # mozilla_path = get_mozilla_folder()
    # print(f"MOZZILA_PATH = {mozilla_path}")

    # o = get_session_recovery_data(mozilla_path)
    # print("sess = ", o)
    # save_file("sess.json", o)

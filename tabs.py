from src.util import *
from src.state import State


def get_mozilla_folder():
    _, o, _ = cmd("find / -name '*.mozilla' -type d")
    print(o)
    _, user_folder, _ = cmd("echo ~")
    user_folder = user_folder.strip()
    resps = []
    for candidate in o.splitlines():
        candidate = candidate.strip()
        if candidate.startswith(user_folder):
            resps.append(candidate)
    if len(resps) == 0:
        raise Exception("the '.mozilla' folder was not found")
    if len(resps) > 1:
        raise Exception(
            f"more than one ({len(resps)}) possible candidate for '.mozilla' folder, please specify it manually in the state file. the candidates are: \n ---> "
            + "\n ---> ".join(resps)
        )
    return resps[0]


def get_recovery_file(mozilla_folder):
    _, o, _ = cmd(
        f"find {mozilla_folder} -name '*recovery.jsonlz4'",
    )
    o = o.strip()
    return o


def get_recovery_recovery_data(recovery_file):
    # lz4jsoncat $profile/sessionstore-backups/recovery.jsonlz4 \
    # | jq -r '.windows[] | .tabs[] | (.index - 1) as $i | .entries[$i] | .title, .url, ""'

    _, o, _ = cmd(
        f"lz4jsoncat {recovery_file} | jq -r '[.windows[] | .tabs[] | (.index - 1) as $i | .entries[$i]]'",
    )
    return o


if __name__ == "__main__":
    s = State()
    s.load()

    if "MOZZILA_PATH" not in s.state:
        s.state["MOZZILA_PATH"] = ""
        s.save()

    mozilla_path = s.state.get("MOZZILA_PATH")
    if mozilla_path is None or len(mozilla_path) == 0:
        s.state["MOZZILA_PATH"] = get_mozilla_folder()
    print(f"MOZZILA_PATH = {mozilla_path}")

    s.save()

    recovery_file = s.state.get("RECOVERY_FILE")
    if recovery_file is None or len(recovery_file) == 0:
        s.state["RECOVERY_FILE"] = get_recovery_file(mozilla_path)
    print(f"RECOVERY_FILE = {recovery_file}")
    s.save()

    o = get_recovery_recovery_data(recovery_file)

    filename = f"sess-{get_timestamp()}.json"
    save_file(filename, o)

    print(f"saved tabs to '{filename}'")

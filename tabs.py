from src.util import *
from src.state import State

DEBUG = 1


def get_brave_folder():
    _, o, _ = cmd("find ~ -name BraveSoftware -type d")
    _, user_folder, _ = cmd("echo ~")
    user_folder = user_folder.strip()
    resps = []
    for candidate in o.splitlines():
        candidate = candidate.strip()
        if candidate.startswith(user_folder):
            if "cache" in resps:
                continue
            resps.append(candidate)
    for r in resps:
        if "config" in r:
            return r
    if len(resps) == 0:
        raise Exception("the 'BraveSoftware' folder was not found")
    if len(resps) > 1:
        print(
            f"more than one ({len(resps)}) possible candidate for 'BraveSoftware' folder, please specify it manually in the state file. the candidates are: \n ---> "
            + "\n ---> ".join(resps)
        )


def get_brave_tabs(s: State):
    brave_folder = get_brave_folder()
    brave_sess_path = brave_folder + "/Brave-Browser/Default/Sessions"
    # SELECIONA POR MOTIVOS ALEATÓRIOS O MAIOR RESULTADO
    brave_sess_file = sorted(cmd("ls " + brave_sess_path)[1].split("\n"))
    brave_sess_file = brave_sess_file[len(brave_sess_file) - 1]
    brave_sess_file = brave_sess_path + "/" + brave_sess_file

    print("brave_sess_file=" + brave_sess_file)

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-f", "--filename")
    # args = parser.parse_args()
    # filename = args.filename

    tmpfile = "tmpfile"
    cmd(f"strings -n1 {brave_sess_file} > {tmpfile}")
    content = load_file(tmpfile)
    cmd(f"rm {tmpfile}")

    content = content.split("\n")
    urls = {}
    last_url = ""
    for txt in content:
        if "http" in txt and "://" in txt and "---" not in txt:
            if not txt in urls:
                urls[txt] = {"title": []}
            last_url = txt
        elif len(last_url) > 0:
            urls[last_url]["title"].append(txt)

    file = []
    for url in urls:
        urls[url]["source"] = "brave"
        urls[url]["url"] = url

        text = "".join(urls[url]["title"])
        text = text.split("https://")[0]
        text = text.split("http://")[0]

        if "- YouTube" in text:
            text = text.split("- YouTube")[0]
            text += "- YouTube"

        urls[url]["title"] = text
        file.append(urls[url])

    return file


def get_mozilla_folder():
    _, o, _ = cmd("find ~ -name '*.mozilla' -type d")
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


def get_firefox_tabs(s: State):
    if "MOZZILA_PATH" not in s.state:
        s.state["MOZZILA_PATH"] = ""
        s.save()

    mozilla_path = s.state.get("MOZZILA_PATH")
    if mozilla_path is None or len(mozilla_path) == 0:
        s.state["MOZZILA_PATH"] = get_mozilla_folder()
    print(f"MOZZILA_PATH = {mozilla_path}")

    s.save()

    recovery_file = s.state.get("MOZILLA_RECOVERY_FILE")
    if recovery_file is None or len(recovery_file) == 0:
        s.state["MOZILLA_RECOVERY_FILE"] = get_recovery_file(mozilla_path)
    print(f"MOZILLA_RECOVERY_FILE = {recovery_file}")
    s.save()

    o = get_recovery_recovery_data(recovery_file)

    tabs = json.loads(o)

    firefox_tabs = []

    for tab in tabs:
        firefox_tabs.append(
            {
                "url": tab["url"],
                "title": tab["title"],
                "source": "firefox",
            }
        )

    return firefox_tabs


if __name__ == "__main__":
    s = State()
    s.load()

    print(f"getting firefox tabs...")
    firefox = get_firefox_tabs(s)
    print(f"getting brave tabs...")
    brave = get_brave_tabs(s)

    all_tabs = firefox + brave

    filename = f"sess-{get_timestamp()}.json"

    save_json(filename, all_tabs)

    print(f"saved all tabs to '{filename}'")

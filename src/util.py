import subprocess
import copy
import json
import math
import threading
import hashlib
import json
import time
import os
import json
import datetime


def cmd(command: str, debug=False):
    if debug:
        print(f"executing command: {command}")
    completed_process = subprocess.run(
        command,  # command.split(" "),
        shell=True,
        # cwd="env",
        # input=bytes(command, encoding="utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = completed_process.stdout.decode("utf-8")
    err = completed_process.stderr.decode("utf-8")
    return completed_process, out, err


def copy_file(source, target):
    subprocess.run("cp " + source + " " + target, shell=True)


def save_file(name, val):
    with open(name, "w") as f:
        f.write(val)


def append_file(name, val):
    with open(name, "a") as f:
        f.write(val)


def save_json(name, val):
    with open(name, "w") as f:
        f.write(json.dumps(val, indent=4))


def load_json(name):
    with open(name, "r") as f:
        return json.loads(f.read())


def delete_file(target):
    try:
        subprocess.call(["rm", "-f", target])
    except Exception as e:
        # print("ERROR! tried to delete file", target, "but failed because", e)
        pass


def load_file(name):
    with open(name, "r") as f:
        return f.read()


def is_file(name):
    return os.path.isfile(name)


def get_files_inside_folder(folder):
    return os.listdir(folder)


def flatten_html_bs4(content):
    words = []
    for p in content.find_all():
        words.append(p.getText())
    return " ".join(words)


def get_time_string():
    return datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S")


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S")


def sort_list_by_key(list, key):
    return sorted(list, key=lambda k: k[key], reverse=True)

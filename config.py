import os
import json
import sys

CONFIG_FILE_NAME = "config.json"

conf = {}


def init_config():
    global conf
    touch_file()
    load_json_file()
    if "version" not in conf:
        print("config.json is empty or malformed. Initializing new config.")
        conf = {"version": 1,
                  "wallets": {},
                  "selected_wallet": "",
                  "rpc_address": "http://localhost:1761"}
        save_json_file()


def touch_file():
    if not os.path.exists(CONFIG_FILE_NAME):
        touch = open(CONFIG_FILE_NAME, 'w+')
        touch.close()


def load_json_file():
    global conf
    with open(CONFIG_FILE_NAME, 'r') as f:
        try:
            conf = json.load(f)
        except json.JSONDecodeError:
            print("Failed to load config.")


def save_json_file():
    global conf
    with open(CONFIG_FILE_NAME, "w") as f:
        json.dump(conf, f, indent=4)


def get(key):
    if key not in conf:
        print("Could not locate key: \"" + key + "\" in config.")
        sys.exit(1)
    return conf[key]

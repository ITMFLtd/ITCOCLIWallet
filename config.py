import os
import json


def touch_file(file_name):
    if not os.path.exists(file_name):
        touch = open(file_name, 'w+')
        touch.close()


def load_json_file(file_name):
    with open(file_name, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None

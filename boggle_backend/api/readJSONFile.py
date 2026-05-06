import re
import sys
import json

def read_json_to_list(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    string_list = []
    for value in data.values():
        if isinstance(value, list):
            string_list.extend(value)
        else:
            string_list.append(str(value))
    return string_list

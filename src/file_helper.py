import json

def read_file(file_path):
    return open(file_path, "r")


def read_file_to_json(file_path):
    file = read_file(file_path)
    return json.load(file)


def write_json_to_file(filepath, j_data):
    f_file = open(filepath, "r+")
    f_file.seek(0)
    json.dump(j_data, f_file, indent=4)
    f_file.close()


def print_json_pretty(j_data):
    print(json.dumps(j_data, indent=4, sort_keys=False))
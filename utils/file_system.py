import json
from functools import lru_cache


@lru_cache(maxsize=None)
def load_file(file_name, file_format="txt", convert_to_set=False):
    if file_format == "txt":
        with open(file_name, "r") as f:
            return f.read().split("\n")
    elif file_format == "json":
        with open(file_name, "r") as f:
            if convert_to_set:
                return set(json.load(f))
            return json.load(f)
    raise ValueError(f"Unknown format {file_format}")


def save_to_file(file_name, data, file_format="txt", open_format="a"):
    if type(data) == set:
        data = list(data)
    if file_format == "txt":
        with open(file_name, open_format) as f:
            f.write(f"{data}\n")
    elif file_format == "json":
        with open(file_name, open_format) as f:
            json.dump(data, f)
    else:
        raise ValueError(f"Unknown format {file_format}")

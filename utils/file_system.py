import json
from functools import lru_cache


@lru_cache(maxsize=None)
def load_file(file_name, file_format="txt", convert_to_set=False, convert_to_hashable=False):
    if file_format == "txt":
        with open(file_name, "r") as f:
            return f.read().split("\n")
    elif file_format == "json":
        with open(file_name, "r") as f:
            if convert_to_set:
                if convert_to_hashable:
                    return {dict_to_hashable(item) if isinstance(item, dict) else item for item in json.load(f)}
                return set(json.load(f))
            return json.load(f)
    elif file_format == "bytes":
        with open(file_name, "rb") as f:
            return f.read()
    raise ValueError(f"Unknown format {file_format}")


def save_to_file(file_name, data, file_format="txt", open_format="a", tuples_to_dict=False):
    if type(data) == set:
        data = list(data)
    if tuples_to_dict:
        data = [dict(item) if isinstance(item, tuple) else item for item in data]
    if file_format == "txt":
        with open(file_name, open_format) as f:
            f.write(f"{data}\n")
    elif file_format == "json":
        with open(file_name, open_format) as f:
            json.dump(data, f)
    else:
        raise ValueError(f"Unknown format {file_format}")


def get_blob_from_image_file(file_name):
    with open(file_name, "rb") as f:
        return f.read()
    

def dict_to_hashable(d):
    return tuple(d.items())
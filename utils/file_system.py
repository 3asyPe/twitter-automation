def load_file(file_name):
    with open(file_name, "r") as f:
        return f.read().split("\n")


def save_to_file(file_name, data):
    with open(file_name, "a") as f:
        f.write(f"{data}\n")

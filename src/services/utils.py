import os


def join_strings(strings: list[str]) -> str:
    """Joins an array of strings into a single space-separated string"""
    return " ".join(strings)


def save_to_file(filename: str, content: str, path: str):
    full_path = f"{path}/{filename}"
    os.makedirs(path, exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

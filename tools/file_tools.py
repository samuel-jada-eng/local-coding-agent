from pathlib import Path


def read_file(filepath):
    path = Path(filepath)

    if not path.exists():
        return "File does not exist."

    return path.read_text()


def write_file(filepath, content):
    path = Path(filepath)

    path.write_text(content)

    return f"File written successfully: {filepath}"


def list_files(directory="."):
    path = Path(directory)

    files = [str(file) for file in path.iterdir()]

    return "\n".join(files)

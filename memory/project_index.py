from pathlib import Path
from memory.vector_store import add_memory

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".html",
    ".css",
    ".php",
    ".sql"
]


def scan_project(directory="."):

    project_data = []

    path = Path(directory)

    for file in path.rglob("*"):

        if file.suffix in SUPPORTED_EXTENSIONS:

            try:

                content = file.read_text(encoding="utf-8")

                project_data.append({
                    "filepath": str(file),
                    "content": content[:3000]
                })

                add_memory(
                    content,
                    metadata=str(file)
                )

            except:
                pass

    return project_data

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """
    Create directory if it doesn't exist.
    """

    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_directories(*paths: Path) -> None:
    """
    Create multiple directories.
    """

    for path in paths:
        ensure_directory(path)


def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def directory_exists(path: Path) -> bool:
    return path.exists() and path.is_dir()

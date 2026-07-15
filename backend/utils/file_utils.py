from pathlib import Path
import shutil


def get_file_size(path: Path) -> float:
    """
    Returns size in MB.
    """

    return path.stat().st_size / (1024 * 1024)


def copy_file(source: Path, destination: Path) -> Path:
    """
    Copy a file and create the destination directory if needed.
    Returns the destination path.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(source, destination)

    return destination


def move_file(source: Path, destination: Path) -> None:
    shutil.move(str(source), str(destination))


def delete_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def clear_directory(directory: Path) -> None:

    if not directory.exists():
        return

    for item in directory.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)

"""Input/output utilities for puzzle solutions."""

import sys
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import List, Tuple, Union


class InputMode(Enum):
    """Mode for reading input files."""

    LINES = "lines"
    TEXT = "text"


def with_calling_file_context(func):
    """Decorator that passes the calling file's path to the wrapped function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = sys._getframe(1)
        filepath = frame.f_code.co_filename
        return func(filepath, *args, **kwargs)

    return wrapper


def puzzle_info(
    filepath: Path, pad_day: bool = False
) -> Union[Tuple[int, int, int], Tuple[int, str, int]]:
    """
    Extract year and day information from the calling file's path.

    Expects file structure like:
    - /path/to/y2024/d01_1.py -> (2024, 1) or (2024, "01")
    - /path/to/2024/d01.py -> (2024, 1) or (2024, "01")

    Args:
        filepath: Path to the calling file (automatically injected by decorator).
        pad_day: If True, return day as zero-padded string. If False, return as int.

    Returns:
        Tuple of (year, day) where day is int or str depending on pad_day.

    Example:
        >>> # In file y2024/d01_1.py
        >>> year, day = puzzle_info()
        >>> print(year, day)
        2024 1
        >>> year, day = puzzle_info(pad_day=True)
        >>> print(year, day)
        2024 01
    """
    # Extract year from parent directory (e.g., "y2024" or "2024")
    parent_dir = filepath.parts[-2]
    if parent_dir.startswith("y"):
        year = int(parent_dir[1:])
    else:
        year = int(parent_dir)

    # Extract day from filename (e.g., "d01_1.py" or "d01.py")
    filename = filepath.stem  # Gets filename without extension
    day_part = filename.split("_")[0]  # Gets "d01" from "d01_1"
    day = int(day_part.replace("d", ""))
    day = f"{day:02d}" if pad_day else day

    # part 1, part 2, etc.
    # e.g., d01_2.py for part 2 of day 1
    part = int(filename.split("_")[1]) if "_" in filename else None

    return year, day, part


@with_calling_file_context
def read_input(
    filepath: str,
    test: bool = False,
    strip: bool = True,
    data_dir: str = "../../data",
    mode: InputMode = InputMode.LINES,
) -> Union[str, List[str]]:
    """
    Read puzzle input file based on the calling file's location.

    Args:
        filepath: Path to the calling file (automatically injected by decorator).
        test: If True, read from testXX.txt. If False, read from inputXX.txt.
        strip: If True, strip whitespace from the content (or each line in LINES mode).
        data_dir: Relative path from calling file to data directory.
        mode: InputMode.LINES (default) returns list of lines, InputMode.TEXT returns string.

    Returns:
        Content of the input file as a list of strings (LINES mode) or single string (TEXT mode).

    Example:
        >>> # In file y2024/day01_1.py
        >>> lines = read_input()  # Reads ../../data/2024/input01.txt as list of lines
        >>> text = read_input(mode=InputMode.TEXT)  # Reads as single string
        >>> test_lines = read_input(test=True)  # Reads ../../data/2024/test01.txt as lines
    """
    calling_file = Path(filepath)
    year, day, part = puzzle_info(calling_file, pad_day=True)

    filetype = "test" if test else "input"

    if part is None:
        input_path = calling_file.parent / data_dir / str(year) / f"{filetype}{day}.txt"
    else:
        input_path = (
            calling_file.parent / data_dir / str(year) / f"{filetype}{day}_{part}.txt"
        )

    with open(input_path) as f:
        if mode == InputMode.LINES:
            content = f.readlines()
            if strip:
                content = [line.rstrip("\n") for line in content]
            return content
        else:  # InputMode.TEXT
            content = f.read()
            return content.strip() if strip else content

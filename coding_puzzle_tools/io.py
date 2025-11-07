"""Input/output utilities for puzzle solutions."""

import sys
from functools import wraps
from pathlib import Path
from typing import Literal, Tuple, Union


def with_calling_file_context(func):
    """Decorator that passes the calling file's path to the wrapped function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = sys._getframe(1)
        filepath = frame.f_code.co_filename
        return func(filepath, *args, **kwargs)
    return wrapper


@with_calling_file_context
def puzzle_info(
    filepath: str,
    pad_day: bool = False
) -> Union[Tuple[int, int], Tuple[int, str]]:
    """
    Extract year and day information from the calling file's path.

    Expects file structure like:
    - /path/to/y2024/day01_1.py -> (2024, 1) or (2024, "01")
    - /path/to/2024/day01.py -> (2024, 1) or (2024, "01")

    Args:
        pad_day: If True, return day as zero-padded string. If False, return as int.

    Returns:
        Tuple of (year, day) where day is int or str depending on pad_day.

    Example:
        >>> # In file y2024/day01_1.py
        >>> year, day = puzzle_info()
        >>> print(year, day)
        2024 1
        >>> year, day = puzzle_info(pad_day=True)
        >>> print(year, day)
        2024 01
    """
    p = Path(filepath)

    # Extract year from parent directory (e.g., "y2024" or "2024")
    parent_dir = p.parts[-2]
    if parent_dir.startswith('y'):
        year = int(parent_dir[1:])
    else:
        year = int(parent_dir)

    # Extract day from filename (e.g., "day01_1.py" or "day01.py")
    filename = p.stem  # Gets filename without extension
    day_part = filename.split('_')[0]  # Gets "day01" from "day01_1"
    day = int(day_part.replace('day', ''))

    if pad_day:
        return year, f"{day:02d}"
    return year, day


@with_calling_file_context
def read_input(
    filepath: str,
    test: bool = False,
    strip: bool = True,
    data_dir: str = "../../data"
) -> str:
    """
    Read puzzle input file based on the calling file's location.

    Args:
        test: If True, read from testXX.txt. If False, read from inputXX.txt.
        strip: If True, strip whitespace from the content.
        data_dir: Relative path from calling file to data directory.

    Returns:
        Content of the input file as a string.

    Example:
        >>> # In file y2024/day01_1.py
        >>> text = read_input()  # Reads ../../data/2024/input01.txt
        >>> test_text = read_input(test=True)  # Reads ../../data/2024/test01.txt
    """
    calling_file = Path(filepath)
    year, day = puzzle_info(calling_file, pad_day=True)

    filetype = "test" if test else "input"
    input_path = calling_file.parent / data_dir / str(year) / f"{filetype}{day}.txt"

    with open(input_path) as f:
        content = f.read()

    return content.strip() if strip else content
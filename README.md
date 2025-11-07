# coding-puzzle-tools

Utilities for coding puzzle competitions like Advent of Code, Everybody Codes, and similar challenges.

## Installation

### From GitHub (recommended for use)

```bash
pip install git+https://github.com/shalgrim/coding-puzzle-tools.git
```

### Local editable install (recommended for development)

```bash
# Clone the repository
git clone https://github.com/shalgrim/coding-puzzle-tools.git
cd coding-puzzle-tools

# Install in editable mode
pip install -e .
```

### In requirements.txt

```
# From GitHub
coding-puzzle-tools @ git+https://github.com/shalgrim/coding-puzzle-tools.git

# Or local editable (for development)
-e /path/to/coding-puzzle-tools
```

## Usage

### Basic example

```python
from coding_puzzle_tools import puzzle_info, read_input

# Automatically extract year and day from your file path
# If your file is y2024/day01_1.py, this returns (2024, 1)
year, day = puzzle_info()

# Or get zero-padded day string
year, day = puzzle_info(pad_day=True)  # Returns (2024, "01")

# Read input file automatically
text = read_input()  # Reads ../../data/2024/input01.txt
test_text = read_input(test=True)  # Reads ../../data/2024/test01.txt
```

### Complete solution example

```python
# File: y2024/day01_1.py
from coding_puzzle_tools import read_input

def main(lines):
    # Your solution here
    return answer

if __name__ == "__main__":
    text = read_input()  # Automatically finds correct input file
    print(main(text))
```

## Expected Directory Structure

The tools assume a directory structure like:

```
your-project/
  ├── data/
  │   └── 2024/
  │       ├── input01.txt
  │       ├── test01.txt
  │       ├── input02.txt
  │       └── test02.txt
  └── y2024/
      ├── day01_1.py
      ├── day01_2.py
      ├── day02_1.py
      └── day02_2.py
```

Or alternatively:

```
your-project/
  ├── data/
  │   └── 2024/
  │       └── input01.txt
  └── 2024/
      └── day01.py
```

## API Reference

### `puzzle_info(pad_day=False)`

Extracts year and day from the calling file's path.

**Parameters:**
- `pad_day` (bool): If True, return day as zero-padded string (e.g., "01"). Default False.

**Returns:**
- Tuple[int, int] or Tuple[int, str]: (year, day)

**Example:**
```python
# In file y2024/day05_2.py
year, day = puzzle_info()  # Returns (2024, 5)
year, day = puzzle_info(pad_day=True)  # Returns (2024, "05")
```

### `read_input(test=False, strip=True, data_dir="../../data")`

Reads puzzle input file based on the calling file's location.

**Parameters:**
- `test` (bool): If True, read test input. If False, read real input. Default False.
- `strip` (bool): If True, strip whitespace. Default True.
- `data_dir` (str): Relative path to data directory. Default "../../data".

**Returns:**
- str: Content of the input file

**Example:**
```python
# In file y2024/day01_1.py
text = read_input()  # Reads ../../data/2024/input01.txt
test = read_input(test=True)  # Reads ../../data/2024/test01.txt
raw = read_input(strip=False)  # Preserves whitespace
```

## License

MIT License

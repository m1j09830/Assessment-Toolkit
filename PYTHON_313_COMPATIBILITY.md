# Python 3.13 Compatibility Update

## Changes Made

This project has been updated for Python 3.13 compatibility with the following improvements:

### 1. Dependencies Updated
- Updated `pyproject.toml` to support Python 3.9 through 3.13
- Updated dependencies to their latest Python 3.13 compatible versions:
  - `rich` from ^12.5.1 to ^13.9.0
  - `typer` from ^0.6.1 to ^0.15.0
  - `click` explicitly set to ^8.1.7 (fixes Python 3.13 compatibility)
  - `pylint` from ^2.13 to ^3.0
  - `pytest` from ^7.1.2 to ^8.0
  - Added `black` and `mypy` for better code quality

### Known Issues Fixed
- **TypeError: Parameter.make_metavar() missing 1 required positional argument**: Fixed by updating Typer to 0.15.0+ and Click to 8.1.7+

### 2. Security Improvements
- Replaced all `os.system()` calls with safer `subprocess.run()` 
- Added proper shell command escaping using `shlex.quote()`
- Improved error handling throughout all functions
- Added type hints for better code safety

### 3. Code Quality Improvements
- Added proper return type annotations
- Improved error handling and return values
- Used `pathlib.Path` for safer file operations
- Removed code duplication
- Better string formatting consistency

### 4. Functional Changes
- All scan functions now return boolean success/failure status
- Better error reporting and logging
- Safer directory creation using `Path.mkdir()`
- Environment variable handling improved for API keys

## Common Issues and Solutions

### TypeError: Parameter.make_metavar() missing 1 required positional argument: 'ctx'

This error occurs when using older versions of Typer with Python 3.13. **Fixed by:**

1. Updated `typer` from ^0.6.1 to ^0.12.0 in `pyproject.toml`
2. Updated `click` dependency to ^8.1.0 for full Python 3.13 compatibility
3. Updated function signatures in `__main__.py` for better compatibility

**Solution:** Install the updated dependencies:
```bash
pip install typer>=0.12.0 click>=8.1.0 rich>=13.7.0
```

To install and test with Python 3.13:

### Option 1: Using Poetry (Recommended)
```bash
poetry install
poetry update
poetry run Assessment-Toolkit --help
```

### Option 2: Using pip in virtual environment
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
Assessment-Toolkit --help
```

### Option 3: Direct pip install
```bash
pip install rich>=13.9.0 typer>=0.15.0 click>=8.1.7
pip install -e .
```

To run tests:
```bash
poetry run pytest  # or just pytest if using pip
```

To check with linting:
```bash
poetry run pylint assessment_toolkit/  # or pylint if using pip
```

## Breaking Changes

- All scan functions now return `bool` instead of `None`
- Some functions may behave slightly differently due to improved error handling
- Command execution is now more secure but may require updated shell commands

## Migration Guide

If you have custom code calling these functions:

```python
# Before
discovery(rv_num, target_list)

# After - check return value
if discovery(rv_num, target_list):
    print("Discovery scan completed successfully")
else:
    print("Discovery scan failed")
```

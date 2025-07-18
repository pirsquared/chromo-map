# Scripts

This directory contains utility scripts for project maintenance and automation.

## Files

### `remove_duplicate_color.py`
**Purpose**: Code maintenance utility  
**Description**: Script used to remove duplicate Color class definitions from the main color.py file during refactoring. Contains logic to safely identify and remove redundant code blocks while preserving the correct implementation.

**Run with**: `python remove_duplicate_color.py`

## Usage

These scripts are utilities for:
- **Code maintenance**: Cleaning up duplicate or redundant code
- **Refactoring assistance**: Automating repetitive cleanup tasks
- **Project organization**: Maintaining clean codebase structure

## Note

Scripts in this directory:
- May modify source code files
- Should be run with caution
- Are designed for specific maintenance tasks
- May become obsolete after their purpose is fulfilled

Always backup your code before running maintenance scripts.

## Requirements

Scripts may require:
```bash
pip install -e .
```

And may need to be run from the project root directory.

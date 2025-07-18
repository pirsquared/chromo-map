# Development Scripts

This directory contains scripts used during development for testing, debugging, and experimentation.

## Files

### `final_test.py`
**Purpose**: Complete integration test for contrast optimization methods  
**Description**: Comprehensive test demonstrating all the new contrast optimization methods across Color, Gradient, and Swatch classes. Used for validating implementations and debugging.

**Run with**: `python final_test.py`

### `find_viridis.py`
**Purpose**: Debug script for catalog system issues  
**Description**: Diagnostic script used to troubleshoot issues with finding specific gradients (like 'viridis') in the catalog system. Helps debug import and registration problems.

**Run with**: `python find_viridis.py`

### `sensitivity_test.py`
**Purpose**: Algorithm sensitivity analysis  
**Description**: Tests how contrast optimization algorithms perform with different base colors and backgrounds. Used for validating algorithm robustness and consistency.

**Run with**: `python sensitivity_test.py`

## Usage

These scripts are primarily for:
- **Development testing**: Validating new features and implementations
- **Debugging**: Diagnosing issues with specific functionality
- **Algorithm analysis**: Understanding performance characteristics
- **Regression testing**: Ensuring changes don't break existing functionality

## Note

These scripts are development tools and may contain:
- Hard-coded test values
- Debug print statements
- Experimental code
- Temporary workarounds

They are preserved for:
- Historical reference
- Debugging similar issues
- Understanding implementation decisions
- Regression testing

## Requirements

All scripts require the chromo-map library in development mode:
```bash
pip install -e .
```

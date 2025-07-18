# Examples

This directory contains demonstration scripts and practical examples for using the chromo-map library.

## Files

### `contrast_approaches_summary.py`
**Purpose**: Comprehensive demonstration of the three contrast optimization approaches  
**Description**: Shows the differences between simple iterative, enhanced iterative, binary search, and mathematical optimization methods for finding maximal color contrast. Includes performance benchmarking and use case recommendations.

**Run with**: `python contrast_approaches_summary.py`

### `demo.py`
**Purpose**: Basic demonstration of the get_gradient function  
**Description**: Shows how to search for gradients using exact names, regex patterns, case sensitivity options, and priority ordering.

**Run with**: `python demo.py`

### `practical_example.py`
**Purpose**: Real-world accessibility example  
**Description**: Demonstrates how to make a brand color accessible for web use by finding variants that meet WCAG contrast requirements against different backgrounds.

**Run with**: `python practical_example.py`

## Usage

These examples are designed to help users understand:
- How to use different contrast optimization methods
- When to choose each approach
- Performance characteristics of different methods
- Practical accessibility applications
- Basic gradient search functionality

## Requirements

All examples require the chromo-map library to be installed:
```bash
pip install chromo-map
```

Or for development:
```bash
pip install -e .
```

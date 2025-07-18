# MyPy Type Checking Fixes

## Current Issues Analysis

### 1. chromo_map/core/color.py:977
```python
# Issue: Returning Any from function declared to return "float"
# Fix: Add proper return type annotation
```

### 2. chromo_map/core/gradient.py:76,133
```python
# Issue: Cannot determine type of "colors" and _segmentdata attribute
# Fix: Add type annotations and handle matplotlib attributes
```

### 3. chromo_map/core/swatch.py:600
```python
# Issue: Returning Any from function declared to return "str"
# Fix: Add proper return type annotation
```

### 4. chromo_map/catalog/builders.py
```python
# Issue: Multiple type annotation issues
# Fix: Add proper type annotations for dictionaries and variables
```

### 5. chromo_map/analysis/palette.py:278
```python
# Issue: Returning Any from function declared to return "Optional[Gradient]"
# Fix: Already fixed with type: ignore
```

## Implementation Priority
1. Fix gradient.py issues (most critical)
2. Fix builders.py issues (catalog system)
3. Fix color.py and swatch.py issues
4. Update mypy.ini for better configuration

# Python Packaging Configuration

## Current Setup ✅

The chromo-map project uses **modern Python packaging standards** with backward compatibility:

### **Primary Configuration: `pyproject.toml`**
- **Standard**: PEP 518/621 compliant
- **Contains**: All project metadata, dependencies, build configuration
- **Benefits**: Modern, standardized, tool-agnostic

### **Compatibility Layer: `setup.py`**
- **Purpose**: Minimal file for editable installs (`pip install -e .`)
- **Contains**: Only a basic `setup()` call
- **Configuration**: All moved to `pyproject.toml`

### **Supporting Files**
- **`MANIFEST.in`**: Data file inclusion (still needed)
- **`setup.cfg`**: Minimal legacy metadata (kept for compatibility)

## Recommended Approach ✅

**You should use BOTH `setup.py` and `pyproject.toml`** because:

1. **`pyproject.toml`** is the future and should contain all configuration
2. **`setup.py`** provides compatibility for editable installs and legacy tools
3. **This approach** follows Python packaging best practices for 2025

## File Organization

```
├── pyproject.toml     # Primary configuration (PEP 621)
├── setup.py          # Minimal compatibility layer  
├── setup.cfg         # Legacy metadata (minimal)
├── MANIFEST.in       # Data file inclusion
└── requirements.txt  # Optional for deployment
```

## Key Benefits

### ✅ **Modern Standards**
- PEP 518/621 compliant
- Tool-agnostic configuration
- Future-proof approach

### ✅ **Backward Compatibility**  
- Works with older pip versions
- Compatible with editable installs
- Supports legacy tooling

### ✅ **Single Source of Truth**
- All configuration in `pyproject.toml`
- No duplicate dependency lists
- Easy maintenance

## Migration Complete ✅

### **Changes Made:**
1. **Fixed** incorrect homepage URL in `pyproject.toml`
2. **Simplified** `setup.py` to minimal compatibility layer
3. **Removed** duplicate dependencies from `setup.py`
4. **Added** proper project URLs (homepage, docs, bug tracker)
5. **Cleaned up** `setup.cfg` to minimal content

### **Testing Verified:**
- ✅ Package imports correctly
- ✅ Configuration is valid
- ✅ All tests still pass (244/244)
- ✅ Build system works

## Best Practices Going Forward

1. **Update versions** in `pyproject.toml` only
2. **Add dependencies** to `pyproject.toml` only  
3. **Keep `setup.py`** minimal (don't add configuration there)
4. **Use `pyproject.toml`** for all tool configuration (black, mypy, etc.)

## Why Not Remove `setup.py`?

While some projects are moving to `pyproject.toml`-only, keeping a minimal `setup.py` ensures:
- **Editable installs** work reliably across all environments
- **Legacy tool compatibility** (CI/CD systems, deployment tools)
- **Developer experience** remains smooth
- **Zero maintenance burden** (it's just one line: `setup()`)

This is the **recommended approach** for production Python packages in 2025.

#!/usr/bin/env python3
"""Simple test for Phase 3 - Swatch class extraction."""

print("=== Phase 3: Basic Swatch Extraction Test ===")

# Test 1: Import all classes
try:
    from chromo_map.core.color import Color
    from chromo_map.core.gradient import Gradient
    from chromo_map.core.swatch import Swatch
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 2: Create basic instances
try:
    color = Color("#ff0000")
    gradient = Gradient(['#ff0000', '#00ff00'], name='RedGreen')
    swatch = Swatch([gradient])
    print(f"✓ Basic creation successful: {len(swatch)} gradients")
except Exception as e:
    print(f"✗ Basic creation failed: {e}")
    exit(1)

# Test 3: Test swatch basic methods
try:
    swatch_dict = swatch.to_dict()
    gradient_names = [g.name for g in swatch]
    print(f"✓ Basic methods work: {gradient_names}")
except Exception as e:
    print(f"✗ Basic methods failed: {e}")
    exit(1)

# Test 4: Test swatch adjustment methods (without accessibility for now)
try:
    adjusted = swatch.adjust_hue(90)
    print(f"✓ Swatch adjustments work: {len(adjusted)} gradients")
except Exception as e:
    print(f"✗ Swatch adjustments failed: {e}")
    exit(1)

print("\n🎉 Phase 3 Basic Test: ALL TESTS PASSED!")
print("✓ Swatch class successfully extracted to chromo_map.core.swatch")
print("✓ All basic swatch functionality working")

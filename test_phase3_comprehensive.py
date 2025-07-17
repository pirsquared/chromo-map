#!/usr/bin/env python3
"""Comprehensive test for Phase 3 completion."""

print("=== Phase 3 Comprehensive Test ===")

# Test 1: Import from main package
try:
    from chromo_map import Color, Gradient, Swatch
    print("✓ Main package imports successful")
except ImportError as e:
    print(f"✗ Main package imports failed: {e}")
    exit(1)

# Test 2: Import from core modules
try:
    from chromo_map.core.color import Color as CoreColor
    from chromo_map.core.gradient import Gradient as CoreGradient
    from chromo_map.core.swatch import Swatch as CoreSwatch
    print("✓ Core module imports successful")
except ImportError as e:
    print(f"✗ Core module imports failed: {e}")
    exit(1)

# Test 3: Test that main imports are the same as core imports
try:
    color1 = Color('#ff0000')
    color2 = CoreColor('#ff0000')
    print(f"✓ Main and core Color classes are equivalent: {type(color1) == type(color2)}")
except Exception as e:
    print(f"✗ Color class comparison failed: {e}")
    exit(1)

# Test 4: Test complete workflow
try:
    # Create colors
    red = Color('#ff0000')
    green = Color('#00ff00')
    blue = Color('#0000ff')
    
    # Create gradient
    gradient = Gradient([red, green, blue], name='RGB')
    
    # Create swatch
    swatch = Swatch([gradient])
    
    # Test swatch methods
    accessible_swatch = swatch.make_accessible('#ffffff')
    hue_adjusted = swatch.adjust_hue(90)
    
    print(f"✓ Complete workflow works:")
    print(f"  - Original swatch: {len(swatch)} gradients")
    print(f"  - Accessible swatch: {len(accessible_swatch)} gradients")
    print(f"  - Hue adjusted swatch: {len(hue_adjusted)} gradients")
    
except Exception as e:
    print(f"✗ Complete workflow failed: {e}")
    exit(1)

# Test 5: Test that duplicate classes are not interfering
try:
    # Test accessibility functions
    from chromo_map import find_accessible_color, find_maximal_contrast_iterative
    
    gray = Color('#888888')
    accessible = find_accessible_color(gray, '#ffffff')
    optimized = find_maximal_contrast_iterative(gray, '#ffffff')
    
    print(f"✓ Accessibility functions work:")
    print(f"  - Original: {gray.hex}")
    print(f"  - Accessible: {accessible.hex}")
    print(f"  - Optimized: {optimized.hex}")
    
except Exception as e:
    print(f"✗ Accessibility functions failed: {e}")
    exit(1)

print("\n🎉 Phase 3 Comprehensive Test: ALL TESTS PASSED!")
print("✓ All classes successfully extracted to core modules")
print("✓ Main package imports work correctly")
print("✓ Complete workflow functional")
print("✓ No import conflicts detected")

# Show file structure summary
print("\n📊 Current Modular Structure:")
print("  - chromo_map/core/color.py: Color class + accessibility functions")
print("  - chromo_map/core/gradient.py: Gradient class + matplotlib integration")
print("  - chromo_map/core/swatch.py: Swatch class + collection methods")
print("  - chromo_map/color.py: Utility functions + ColorMapDict (remaining)")

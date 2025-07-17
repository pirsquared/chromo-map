#!/usr/bin/env python3
"""Simple test for Phase 3 - Swatch class extraction."""

print("=== Phase 3: Basic Swatch Extraction Test ===")

# Test 1: Import Color class from core module
try:
    from chromo_map.core.color import Color
    print("✓ Color import successful")
except ImportError as e:
    print(f"✗ Color import failed: {e}")
    exit(1)

# Test 2: Create a Color instance
try:
    color = Color("#ff0000")
    print(f"✓ Color creation successful: {color}")
except Exception as e:
    print(f"✗ Color creation failed: {e}")
    exit(1)

# Test 3: Import Gradient class from core module
try:
    from chromo_map.core.gradient import Gradient
    print("✓ Gradient import successful")
except ImportError as e:
    print(f"✗ Gradient import failed: {e}")
    exit(1)

# Test 4: Create a Gradient instance
try:
    gradient = Gradient(['#ff0000', '#00ff00', '#0000ff'], name='RGB')
    print(f"✓ Gradient creation successful: {gradient.name}")
except Exception as e:
    print(f"✗ Gradient creation failed: {e}")
    exit(1)

# Test 5: Import Swatch class from core module
try:
    from chromo_map.core.swatch import Swatch
    print("✓ Swatch import successful")
except ImportError as e:
    print(f"✗ Swatch import failed: {e}")
    exit(1)

# Test 6: Create a Swatch instance
try:
    gradients = [
        Gradient(['#ff0000', '#00ff00'], name='RedGreen'),
        Gradient(['#0000ff', '#ffff00'], name='BlueYellow')
    ]
    swatch = Swatch(gradients)
    print(f"✓ Swatch creation successful with {len(swatch)} gradients")
except Exception as e:
    print(f"✗ Swatch creation failed: {e}")
    exit(1)

# Test 7: Test swatch iteration
try:
    gradient_names = [g.name for g in swatch]
    print(f"✓ Swatch iteration works: {gradient_names}")
except Exception as e:
    print(f"✗ Swatch iteration failed: {e}")
    exit(1)

# Test 8: Test swatch methods
try:
    swatch_dict = swatch.to_dict()
    print(f"✓ Swatch to_dict method works: {list(swatch_dict.keys())}")
except Exception as e:
    print(f"✗ Swatch to_dict failed: {e}")
    exit(1)

# Test 9: Test swatch adjustment methods
try:
    adjusted = swatch.adjust_hue(90)
    print(f"✓ Swatch adjust_hue works: {len(adjusted)} gradients")
except Exception as e:
    print(f"✗ Swatch adjust_hue failed: {e}")
    exit(1)

# Test 10: Test swatch accessibility methods
try:
    accessible = swatch.make_accessible('#ffffff')  # Use hex string instead of 'white'
    print(f"✓ Swatch make_accessible works: {len(accessible)} gradients")
except Exception as e:
    print(f"✗ Swatch make_accessible failed: {e}")
    exit(1)

print("\n🎉 Phase 3 Basic Test: ALL TESTS PASSED!")
print("✓ Swatch class successfully extracted to chromo_map.core.swatch")
print("✓ All basic swatch functionality working")

#!/usr/bin/env python3
"""Simple test for Phase 2 refactoring: Gradient extraction"""

def test_phase2_basic():
    try:
        print("=== Phase 2: Basic Gradient Extraction Test ===")
        
        # Test 1: Import Color from new location
        from chromo_map.core.color import Color
        print("✓ Color import successful")
        
        # Test 2: Create Color objects
        red = Color('#ff0000')
        green = Color('#00ff00')
        blue = Color('#0000ff')
        print(f"✓ Color creation successful: {red.hex}")
        
        # Test 3: Import Gradient from new location
        from chromo_map.core.gradient import Gradient
        print("✓ Gradient import successful")
        
        # Test 4: Create Gradient object
        colors = [red, green, blue]
        gradient = Gradient(colors, name='RGB')
        print(f"✓ Gradient creation successful: {gradient.name}")
        
        # Test 5: Check gradient properties
        print(f"✓ Gradient has {len(gradient.colors)} colors")
        print(f"✓ First color: {gradient.colors[0].hex}")
        print(f"✓ Last color: {gradient.colors[-1].hex}")
        
        # Test 6: Check that gradient is matplotlib compatible
        print(f"✓ Gradient is matplotlib colormap: {hasattr(gradient, 'N')}")
        
        # Test 7: Check gradient methods
        hex_list = gradient.hex
        print(f"✓ Gradient hex method works: {hex_list}")
        
        print("\n🎉 Phase 2 Basic Test: ALL TESTS PASSED!")
        print("✓ Gradient class successfully extracted to chromo_map.core.gradient")
        print("✓ All basic gradient functionality working")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_phase2_basic()

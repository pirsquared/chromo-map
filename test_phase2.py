#!/usr/bin/env python3

"""Test script to check if the basic imports work after Phase 2 refactoring."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test basic Color import
    from chromo_map.core.color import Color
    print("✓ Color import successful")
    
    # Test basic Color functionality
    red = Color('red')
    print(f"✓ Color creation successful: {red.hex}")
    
    # Test Color accessibility methods
    white = Color('white')
    contrast = red.contrast_ratio(white)
    print(f"✓ Color contrast calculation successful: {contrast}")
    
    # Test Gradient import
    from chromo_map.core.gradient import Gradient
    print("✓ Gradient import successful")
    
    # Test basic Gradient functionality
    colors = ['#ff0000', '#00ff00', '#0000ff']
    gradient = Gradient(colors, name='RGB')
    print(f"✓ Gradient creation successful: {gradient.name}")
    
    # Test Gradient accessibility methods
    accessible_gradient = gradient.make_accessible('white')
    print(f"✓ Gradient accessibility methods successful: {accessible_gradient.name}")
    
    # Test main package import
    from chromo_map import Color as MainColor, Gradient as MainGradient
    print("✓ Main package imports successful")
    
    # Test that they are the same classes
    assert Color is MainColor
    assert Gradient is MainGradient
    print("✓ Import consistency verified")
    
    print("\n🎉 All Phase 2 tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

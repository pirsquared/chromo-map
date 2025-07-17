#!/usr/bin/env python3
import chromo_map as cm
from chromo_map import Swatch

print("=== Testing ColorMapDict functionality ===")

# Test 1: Check that catalog structure is correct
print("\n1. Testing catalog structure...")
print("Available catalogs:", list(cm.cmaps.keys()))
print("Matplotlib categories:", list(cm.cmaps.matplotlib.keys()))

# Test 2: Check that ColorMapDict _repr_html_ works
print("\n2. Testing ColorMapDict._repr_html_()...")
miscellaneous = cm.cmaps.matplotlib.miscellaneous
print("Type of miscellaneous:", type(miscellaneous))
print("Is it a ColorMapDict?", type(miscellaneous).__name__ == 'ColorMapDict')

# Test 3: Test the _repr_html_ method
print("\n3. Testing _repr_html_ method...")
html_result = miscellaneous._repr_html_()
print("HTML result type:", type(html_result))
print("HTML result is string?", isinstance(html_result, str))
print("HTML result length:", len(html_result) if html_result else 0)
print("HTML starts with expected format?", html_result.startswith('<div') if html_result else False)

# Test 4: Test that we can create a Swatch manually
print("\n4. Testing manual Swatch creation...")
gradients = [cm.cmaps.all.viridis, cm.cmaps.all.plasma, cm.cmaps.all.inferno]
swatch = Swatch(gradients)
print("Swatch created successfully:", type(swatch))
print("Swatch length:", len(swatch))

# Test 5: Test the unified access pattern
print("\n5. Testing unified access patterns...")
print("Total items in cm.cmaps.all:", len(cm.cmaps.all))
print("Has viridis?", 'viridis' in cm.cmaps.all)
print("Has plasma?", 'plasma' in cm.cmaps.all)
print("Has inferno?", 'inferno' in cm.cmaps.all)

print("\n=== All tests completed successfully! ===")

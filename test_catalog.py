#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from chromo_map.color import cmaps, ColorMapDict

print("=== Testing New Catalog System ===")

# Test ColorMapDict
print("\n1. Testing ColorMapDict:")
test_dict = ColorMapDict()
print(f"   ColorMapDict created: {type(test_dict)}")

# Test the catalog structure
print("\n2. Testing catalog structure:")
print(f"   cmaps type: {type(cmaps)}")
print(f"   Available attributes: {[attr for attr in dir(cmaps) if not attr.startswith('_')]}")

# Test basic access
print("\n3. Testing basic access:")
try:
    print(f"   cmaps.all length: {len(cmaps.all)}")
    print(f"   cmaps.all type: {type(cmaps.all)}")
    if len(cmaps.all) > 0:
        first_key = list(cmaps.all.keys())[0]
        print(f"   First colormap: {first_key}")
        print(f"   First colormap type: {type(cmaps.all[first_key])}")
except Exception as e:
    print(f"   Error accessing cmaps.all: {e}")

# Test matplotlib structure
print("\n4. Testing matplotlib structure:")
try:
    print(f"   matplotlib type: {type(cmaps.matplotlib)}")
    print(f"   matplotlib length: {len(cmaps.matplotlib)}")
    if len(cmaps.matplotlib) > 0:
        for cat in list(cmaps.matplotlib.keys())[:3]:  # First 3 categories
            print(f"   {cat}: {len(cmaps.matplotlib[cat])} items")
except Exception as e:
    print(f"   Error accessing matplotlib: {e}")

print("\n=== Test Complete ===")

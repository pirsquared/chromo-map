#!/usr/bin/env python3

import chromo_map as cm
from chromo_map import get_gradient

print("=== Testing get_gradient function ===")

# Test basic search
print("\n1. Testing basic search:")
grad = get_gradient('viridis')
if grad:
    print(f"✓ Found: {grad.name} (length: {len(grad.colors)})")
else:
    print("✗ viridis not found")

# Test regex search
print("\n2. Testing regex search:")
grad = get_gradient('vir.*')
if grad:
    print(f"✓ Found: {grad.name} (length: {len(grad.colors)})")
else:
    print("✗ vir.* not found")

# Test case sensitivity
print("\n3. Testing case sensitivity:")
grad = get_gradient('VIRIDIS')
if grad:
    print(f"✓ Case insensitive: {grad.name}")
else:
    print("✗ VIRIDIS not found (case insensitive)")

grad = get_gradient('VIRIDIS', case_sensitive=True)
if grad:
    print(f"✓ Case sensitive: {grad.name}")
else:
    print("✗ VIRIDIS not found (case sensitive)")

# Test priority ordering
print("\n4. Testing priority ordering:")
grad = get_gradient('blues')
if grad:
    print(f"✓ Found blues: {grad.name} (length: {len(grad.colors)})")
else:
    print("✗ blues not found")

# Test non-existent gradient
print("\n5. Testing non-existent gradient:")
grad = get_gradient('nonexistent')
if grad:
    print(f"✗ Unexpectedly found: {grad.name}")
else:
    print("✓ Correctly returned None for non-existent gradient")

print("\n=== All tests completed ===")

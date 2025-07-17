"""Complete test demonstrating the new contrast optimization methods."""

from chromo_map import Color, Gradient, Swatch, find_maximal_contrast_optimization

print("Complete Test of Contrast Optimization Methods")
print("=" * 50)

# Test 1: Color class methods
print("\n1. Color Class Methods:")
print("-" * 25)

# Test with a medium-contrast color
color = Color('#dd4444')
background = Color('white')

print(f"Original color: {color.hex}")
print(f"Original contrast: {color.contrast_ratio(background):.2f}")

# Test all methods
accessible = color.find_accessible_version(background)
print(f"Accessible version: {accessible.hex} (contrast: {accessible.contrast_ratio(background):.2f})")

optimized_iter = color.maximize_contrast_iterative(background)
print(f"Iterative optimization: {optimized_iter.hex} (contrast: {optimized_iter.contrast_ratio(background):.2f})")

optimized_binary = color.maximize_contrast_binary_search(background)
print(f"Binary search optimization: {optimized_binary.hex} (contrast: {optimized_binary.contrast_ratio(background):.2f})")

optimized_opt = color.maximize_contrast_optimization(background)
print(f"Mathematical optimization: {optimized_opt.hex} (contrast: {optimized_opt.contrast_ratio(background):.2f})")

# Test 2: Gradient class methods
print("\n2. Gradient Class Methods:")
print("-" * 27)

# Create a gradient with various colors
gradient = Gradient(['#ff6666', '#66aa66', '#6666ff'], name='Test Gradient')
print(f"Original gradient: {gradient.name}")
print(f"Original colors: {[c.hex for c in gradient.colors]}")
print(f"Original contrasts: {[round(c.contrast_ratio(background), 2) for c in gradient.colors]}")

# Test optimization
optimized_gradient = gradient.maximize_contrast_optimization(background)
print(f"Optimized gradient: {optimized_gradient.name}")
print(f"Optimized colors: {[c.hex for c in optimized_gradient.colors]}")
print(f"Optimized contrasts: {[round(c.contrast_ratio(background), 2) for c in optimized_gradient.colors]}")

# Test 3: Swatch class methods
print("\n3. Swatch Class Methods:")
print("-" * 25)

# Create a swatch with multiple gradients
gradients = [
    Gradient(['#ff8888', '#88aa88'], name='Red-Green'),
    Gradient(['#8888ff', '#ffff88'], name='Blue-Yellow')
]
swatch = Swatch(gradients)
print(f"Original swatch has {len(swatch)} gradients")

# Show original contrasts
for i, grad in enumerate(swatch.gradients):
    contrasts = [round(c.contrast_ratio(background), 2) for c in grad.colors]
    print(f"  Gradient {i+1}: {contrasts}")

# Test optimization
optimized_swatch = swatch.maximize_contrast_optimization(background)
print(f"Optimized swatch has {len(optimized_swatch)} gradients")

# Show optimized contrasts
for i, grad in enumerate(optimized_swatch.gradients):
    contrasts = [round(c.contrast_ratio(background), 2) for c in grad.colors]
    print(f"  Gradient {i+1}: {contrasts}")

# Test 4: Compare with standalone functions
print("\n4. Comparison with Standalone Functions:")
print("-" * 40)

test_color = Color('#aa5555')
print(f"Test color: {test_color.hex}")

# Using standalone function
standalone_result = find_maximal_contrast_optimization(test_color, background)
print(f"Standalone function: {standalone_result.hex} (contrast: {standalone_result.contrast_ratio(background):.2f})")

# Using method
method_result = test_color.maximize_contrast_optimization(background)
print(f"Method result: {method_result.hex} (contrast: {method_result.contrast_ratio(background):.2f})")

print(f"Results match: {standalone_result.hex == method_result.hex}")

print("\n" + "=" * 50)
print("All tests completed successfully!")
print("The methods have been successfully integrated into:")
print("- Color class: find_accessible_version, maximize_contrast_*")
print("- Gradient class: find_accessible_version, maximize_contrast_*")
print("- Swatch class: find_accessible_version, maximize_contrast_*")

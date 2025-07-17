"""Test script to verify the new contrast optimization methods."""

from chromo_map import Color, Gradient, Swatch

# Test Color methods
print("Testing Color methods:")
print("===================")

# Create a light color
light_color = Color('#ffcccc')
print(f"Original color: {light_color}")

# Test find_accessible_version
accessible = light_color.find_accessible_version('white')
print(f"Accessible version: {accessible}")

# Test maximize_contrast_iterative
optimized_iter = light_color.maximize_contrast_iterative('white')
print(f"Optimized (iterative): {optimized_iter}")

# Test maximize_contrast_binary_search
optimized_binary = light_color.maximize_contrast_binary_search('white')
print(f"Optimized (binary search): {optimized_binary}")

# Test maximize_contrast_optimization
optimized_opt = light_color.maximize_contrast_optimization('white')
print(f"Optimized (optimization): {optimized_opt}")

print("\nTesting Gradient methods:")
print("========================")

# Create a gradient with light colors
gradient = Gradient(['#ffcccc', '#ccffcc', '#ccccff'], name='Light Colors')
print(f"Original gradient: {gradient.name}")

# Test find_accessible_version
accessible_gradient = gradient.find_accessible_version('white')
print(f"Accessible gradient: {accessible_gradient.name}")

# Test maximize_contrast_iterative
optimized_gradient_iter = gradient.maximize_contrast_iterative('white')
print(f"Optimized gradient (iterative): {optimized_gradient_iter.name}")

# Test maximize_contrast_binary_search
optimized_gradient_binary = gradient.maximize_contrast_binary_search('white')
print(f"Optimized gradient (binary search): {optimized_gradient_binary.name}")

# Test maximize_contrast_optimization
optimized_gradient_opt = gradient.maximize_contrast_optimization('white')
print(f"Optimized gradient (optimization): {optimized_gradient_opt.name}")

print("\nTesting Swatch methods:")
print("======================")

# Create a swatch with light gradients
gradients = [
    Gradient(['#ffcccc', '#ccffcc'], name='Light Red-Green'),
    Gradient(['#ccccff', '#ffffcc'], name='Light Blue-Yellow')
]
swatch = Swatch(gradients)
print(f"Original swatch has {len(swatch)} gradients")

# Test find_accessible_version
accessible_swatch = swatch.find_accessible_version('white')
print(f"Accessible swatch has {len(accessible_swatch)} gradients")

# Test maximize_contrast_iterative
optimized_swatch_iter = swatch.maximize_contrast_iterative('white')
print(f"Optimized swatch (iterative) has {len(optimized_swatch_iter)} gradients")

# Test maximize_contrast_binary_search
optimized_swatch_binary = swatch.maximize_contrast_binary_search('white')
print(f"Optimized swatch (binary search) has {len(optimized_swatch_binary)} gradients")

# Test maximize_contrast_optimization
optimized_swatch_opt = swatch.maximize_contrast_optimization('white')
print(f"Optimized swatch (optimization) has {len(optimized_swatch_opt)} gradients")

print("\nAll tests completed successfully!")

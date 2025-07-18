from chromo_map import (
    find_accessible_color,
    find_maximal_contrast_iterative,
    find_maximal_contrast_binary_search,
    find_maximal_contrast_optimization,
    Color,
)

# Practical example: Making a website color accessible
brand_color = "#ff6b6b"  # Light red brand color
background = "white"

print("PRACTICAL EXAMPLE: Brand Color Accessibility")
print("=" * 50)
print(f"Brand Color: {brand_color}")
print(f"Background: {background}")

base = Color(brand_color)
target = Color(background)
original_contrast = base.contrast_ratio(target)
print(f"Original contrast: {original_contrast:.2f} (needs 4.5+ for AA)")

print("\nApproach Results:")
print("=" * 50)

# Method 1
result1 = find_accessible_color(brand_color, background)
print(f"1. Simple: {result1.hex} (contrast: {result1.contrast_ratio(target):.2f})")

# Method 2
result2 = find_maximal_contrast_iterative(brand_color, background)
print(f"2. Enhanced: {result2.hex} (contrast: {result2.contrast_ratio(target):.2f})")

# Method 3
result3 = find_maximal_contrast_binary_search(brand_color, background)
print(f"3. Binary: {result3.hex} (contrast: {result3.contrast_ratio(target):.2f})")

# Method 4
result4 = find_maximal_contrast_optimization(brand_color, background)
print(
    f"4. Optimization: {result4.hex} (contrast: {result4.contrast_ratio(target):.2f})"
)

print("\nChoice depends on your needs:")
print("- Simple: Quick fix, meets requirements")
print("- Enhanced: Best visual contrast")
print("- Binary: Precise, consistent results")
print("- Optimization: Maximum theoretical contrast")

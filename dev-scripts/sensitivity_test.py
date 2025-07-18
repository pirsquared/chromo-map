from chromo_map import find_maximal_contrast_binary_search, Color

# Test sensitivity to different base colors
target = Color("white")
base_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]

print("SENSITIVITY TEST: Different base colors vs white background")
print("=" * 60)
for base in base_colors:
    result = find_maximal_contrast_binary_search(base, target)
    base_obj = Color(base)
    print(
        f"{base} ({base_obj.hsv[0]:3.0f}°) → {result.hex} (contrast: {result.contrast_ratio(target):.2f})"
    )

print("\nDifferent targets with same base:")
print("=" * 60)
base = "#888888"
targets = ["white", "black", "#ff0000", "#0000ff"]
for target_str in targets:
    target = Color(target_str)
    result = find_maximal_contrast_binary_search(base, target)
    print(
        f"{base} vs {target_str} → {result.hex} (contrast: {result.contrast_ratio(target):.2f})"
    )

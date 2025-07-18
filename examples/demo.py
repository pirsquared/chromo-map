from chromo_map.color import get_gradient

# Test basic search
grad = get_gradient("viridis")
if grad:
    print(f'Basic search "viridis": {grad.name} (length: {len(grad.colors)})')

# Test regex pattern matching
grad = get_gradient("plasma.*")
name = grad.name if grad else "Not found"
length = len(grad.colors) if grad else 0
print(f'Regex pattern "plasma.*": {name} (length: {length})')

# Test priority ordering with longer gradients
grad = get_gradient("blue", case_sensitive=False)
name = grad.name if grad else "Not found"
length = len(grad.colors) if grad else 0
print(f"Blue (longest): {name} (length: {length})")

# Test with set pattern
grad = get_gradient("Set[0-9]+")
name = grad.name if grad else "Not found"
length = len(grad.colors) if grad else 0
print(f"Set pattern: {name} (length: {length})")

# Test case sensitivity
grad = get_gradient("VIRIDIS", case_sensitive=True)
print(f'Case sensitive "VIRIDIS": {grad.name if grad else "Not found"}')

grad = get_gradient("VIRIDIS", case_sensitive=False)
print(f'Case insensitive "VIRIDIS": {grad.name if grad else "Not found"}')

#!/usr/bin/env python3
"""Test script to demonstrate the three approaches for finding maximal contrast."""

from chromo_map.color import (
    Color, 
    find_accessible_color,
    find_maximal_contrast_iterative,
    find_maximal_contrast_binary_search,
    find_maximal_contrast_optimization
)

def test_all_approaches():
    """Test all three approaches for finding maximal contrast."""
    print("=== Testing Three Approaches for Finding Maximal Contrast ===\n")
    
    # Test colors
    test_cases = [
        ('#888888', 'white', 'Gray vs White'),
        ('#ffcccc', 'white', 'Light Pink vs White'),
        ('#333333', 'black', 'Dark Gray vs Black'),
        ('#ff6666', '#000080', 'Light Red vs Navy'),
        ('#ccccff', '#800080', 'Light Blue vs Purple')
    ]
    
    for base_color, target_color, description in test_cases:
        print(f"Test Case: {description}")
        print(f"Base: {base_color}, Target: {target_color}")
        
        base = Color(base_color)
        target = Color(target_color)
        original_contrast = base.contrast_ratio(target)
        
        print(f"Original contrast ratio: {original_contrast:.2f}")
        
        # Method 1: Simple iterative approach (current implementation)
        result1 = find_accessible_color(base_color, target_color)
        contrast1 = result1.contrast_ratio(target)
        print(f"1. Simple iterative: {result1.hex} (contrast: {contrast1:.2f})")
        
        # Method 2: Enhanced iterative approach
        result2 = find_maximal_contrast_iterative(base_color, target_color)
        contrast2 = result2.contrast_ratio(target)
        print(f"2. Enhanced iterative: {result2.hex} (contrast: {contrast2:.2f})")
        
        # Method 3: Binary search approach
        result3 = find_maximal_contrast_binary_search(base_color, target_color)
        contrast3 = result3.contrast_ratio(target)
        print(f"3. Binary search: {result3.hex} (contrast: {contrast3:.2f})")
        
        # Method 4: Optimization approach
        result4 = find_maximal_contrast_optimization(base_color, target_color)
        contrast4 = result4.contrast_ratio(target)
        print(f"4. Mathematical optimization: {result4.hex} (contrast: {contrast4:.2f})")
        
        # Find the best result
        results = [
            (contrast1, result1, "Simple iterative"),
            (contrast2, result2, "Enhanced iterative"),
            (contrast3, result3, "Binary search"),
            (contrast4, result4, "Mathematical optimization")
        ]
        
        best_contrast, best_color, best_method = max(results, key=lambda x: x[0])
        print(f"Best result: {best_method} with contrast {best_contrast:.2f}")
        print(f"Improvement: {best_contrast - original_contrast:.2f}")
        print("-" * 60)

def test_performance_comparison():
    """Test performance of different approaches."""
    print("\n=== Performance Comparison ===\n")
    
    import time
    
    test_color = '#888888'
    target_color = 'white'
    
    # Test each method multiple times for average performance
    methods = [
        ("Simple iterative", lambda: find_accessible_color(test_color, target_color)),
        ("Enhanced iterative", lambda: find_maximal_contrast_iterative(test_color, target_color)),
        ("Binary search", lambda: find_maximal_contrast_binary_search(test_color, target_color)),
        ("Mathematical optimization", lambda: find_maximal_contrast_optimization(test_color, target_color))
    ]
    
    iterations = 100
    
    for method_name, method_func in methods:
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            result = method_func()
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        contrast = result.contrast_ratio(Color(target_color))
        
        print(f"{method_name}:")
        print(f"  Average time: {avg_time*1000:.3f}ms")
        print(f"  Result: {result.hex}")
        print(f"  Contrast: {contrast:.2f}")
        print()

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n=== Edge Cases Testing ===\n")
    
    edge_cases = [
        ('white', 'white', 'Same color'),
        ('black', 'black', 'Same color (black)'),
        ('#ffffff', '#000000', 'Maximum contrast'),
        ('#000000', '#ffffff', 'Maximum contrast (reversed)'),
        ('#808080', '#808080', 'Same medium gray'),
        ('#ff0000', '#00ff00', 'Red vs Green'),
        ('#ffff00', '#0000ff', 'Yellow vs Blue')
    ]
    
    for base_color, target_color, description in edge_cases:
        print(f"Edge Case: {description}")
        
        base = Color(base_color)
        target = Color(target_color)
        original_contrast = base.contrast_ratio(target)
        
        print(f"Original contrast: {original_contrast:.2f}")
        
        try:
            # Test all methods
            result_simple = find_accessible_color(base_color, target_color)
            result_iterative = find_maximal_contrast_iterative(base_color, target_color)
            result_binary = find_maximal_contrast_binary_search(base_color, target_color)
            result_optimization = find_maximal_contrast_optimization(base_color, target_color)
            
            contrasts = [
                result_simple.contrast_ratio(target),
                result_iterative.contrast_ratio(target),
                result_binary.contrast_ratio(target),
                result_optimization.contrast_ratio(target)
            ]
            
            print(f"Results: {[f'{c:.2f}' for c in contrasts]}")
            print(f"All methods converged: {len(set(f'{c:.2f}' for c in contrasts)) == 1}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_all_approaches()
    test_performance_comparison()
    test_edge_cases()

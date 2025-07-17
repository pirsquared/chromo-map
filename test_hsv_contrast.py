#!/usr/bin/env python3
"""Test script for HSV manipulation and contrast calculation features."""

from chromo_map.color import Color, contrast_ratio, is_accessible, find_accessible_color, generate_color_palette, analyze_color_harmony

def test_hsv_properties():
    """Test HSV and HSL properties."""
    print("=== Testing HSV/HSL Properties ===\n")
    
    # Test basic HSV conversion
    red = Color('red')
    print(f"Red RGB: {red.rgb}")
    print(f"Red HSV: {red.hsv}")
    print(f"Red HSL: {red.hsl}")
    print(f"Red Luminance: {red.luminance:.3f}")
    print()
    
    # Test other colors
    colors = [
        ('Blue', Color('blue')),
        ('Green', Color('green')),
        ('Yellow', Color('yellow')),
        ('Purple', Color('purple')),
        ('Orange', Color('orange'))
    ]
    
    for name, color in colors:
        h, s, v = color.hsv
        print(f"{name}: HSV({h:.1f}, {s:.2f}, {v:.2f}) | Luminance: {color.luminance:.3f}")
    print()

def test_hsv_adjustments():
    """Test HSV adjustment methods."""
    print("=== Testing HSV Adjustments ===\n")
    
    red = Color('red')
    print(f"Original red: {red.hex}")
    
    # Test hue adjustment
    orange = red.adjust_hue(30)
    print(f"Red + 30° hue: {orange.hex}")
    
    green = red.adjust_hue(120)
    print(f"Red + 120° hue: {green.hex}")
    
    # Test saturation adjustment
    desaturated = red.adjust_saturation(0.5)
    print(f"Red 50% saturation: {desaturated.hex}")
    
    # Test brightness adjustment
    dark_red = red.adjust_brightness(0.5)
    print(f"Red 50% brightness: {dark_red.hex}")
    
    # Test lightness adjustment
    light_red = red.adjust_lightness(1.3)
    print(f"Red 130% lightness: {light_red.hex}")
    
    # Test set_hsv
    blue = red.set_hsv(h=240)
    print(f"Red with hue=240: {blue.hex}")
    print()

def test_color_harmony():
    """Test color harmony functions."""
    print("=== Testing Color Harmony ===\n")
    
    red = Color('red')
    
    # Complementary
    comp = red.complementary()
    print(f"Red complementary: {comp.hex}")
    
    # Triadic
    triad1, triad2 = red.triadic()
    print(f"Red triadic: {triad1.hex}, {triad2.hex}")
    
    # Analogous
    analog1, analog2 = red.analogous()
    print(f"Red analogous: {analog1.hex}, {analog2.hex}")
    print()

def test_contrast_calculations():
    """Test contrast ratio calculations."""
    print("=== Testing Contrast Calculations ===\n")
    
    # Test basic contrast ratios
    black = Color('black')
    white = Color('white')
    gray = Color('#808080')
    
    print(f"Black vs White: {black.contrast_ratio(white):.1f}:1")
    print(f"Black vs Gray: {black.contrast_ratio(gray):.1f}:1")
    print(f"White vs Gray: {white.contrast_ratio(gray):.1f}:1")
    
    # Test accessibility
    print(f"Black on white accessible (AA): {black.is_accessible(white, 'AA')}")
    print(f"Gray on white accessible (AA): {gray.is_accessible(white, 'AA')}")
    print(f"Gray on white accessible (AAA): {gray.is_accessible(white, 'AAA')}")
    
    # Test standalone functions
    print(f"Contrast ratio (function): {contrast_ratio('black', 'white'):.1f}:1")
    print(f"Is accessible (function): {is_accessible('black', 'white')}")
    print()

def test_accessible_color_finding():
    """Test finding accessible colors."""
    print("=== Testing Accessible Color Finding ===\n")
    
    # Test finding accessible version of gray
    light_gray = Color('#cccccc')
    white = Color('white')
    
    print(f"Original gray: {light_gray.hex}")
    print(f"Contrast vs white: {light_gray.contrast_ratio(white):.1f}:1")
    
    accessible_gray = find_accessible_color(light_gray, white)
    print(f"Accessible gray: {accessible_gray.hex}")
    print(f"New contrast vs white: {accessible_gray.contrast_ratio(white):.1f}:1")
    print()

def test_color_palettes():
    """Test color palette generation."""
    print("=== Testing Color Palette Generation ===\n")
    
    base_color = Color('red')
    
    schemes = ['complementary', 'triadic', 'analogous', 'monochromatic', 'split_complementary']
    
    for scheme in schemes:
        palette = generate_color_palette(base_color, scheme, 5)
        hex_colors = [c.hex for c in palette]
        print(f"{scheme.capitalize()}: {hex_colors}")
    print()

def test_color_harmony_analysis():
    """Test color harmony analysis."""
    print("=== Testing Color Harmony Analysis ===\n")
    
    # Test with a good palette
    good_palette = ['#ff0000', '#00ff00', '#0000ff']  # Primary colors
    analysis = analyze_color_harmony(good_palette)
    
    print("Primary colors analysis:")
    print(f"  Average contrast: {analysis['average_contrast']:.2f}")
    print(f"  Min contrast: {analysis['min_contrast']:.2f}")
    print(f"  Max contrast: {analysis['max_contrast']:.2f}")
    print(f"  Accessibility score: {analysis['accessibility_score']:.2f}")
    print(f"  Hue distribution: {[f'{h:.1f}°' for h in analysis['hue_distribution']]}")
    print(f"  Saturation range: {analysis['saturation_range']}")
    print(f"  Brightness range: {analysis['brightness_range']}")
    print()
    
    # Test with a poor palette
    poor_palette = ['#ffcccc', '#ffdddd', '#ffeeee']  # Very similar colors
    analysis2 = analyze_color_harmony(poor_palette)
    
    print("Similar colors analysis:")
    print(f"  Average contrast: {analysis2['average_contrast']:.2f}")
    print(f"  Accessibility score: {analysis2['accessibility_score']:.2f}")
    print()

if __name__ == "__main__":
    test_hsv_properties()
    test_hsv_adjustments()
    test_color_harmony()
    test_contrast_calculations()
    test_accessible_color_finding()
    test_color_palettes()
    test_color_harmony_analysis()
    print("=== All Tests Completed ===")

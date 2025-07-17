#!/usr/bin/env python3
"""Test script for Gradient and Swatch HSV manipulation and contrast analysis."""

from chromo_map.color import Color, Gradient, Swatch

def test_gradient_hsv_manipulation():
    """Test HSV manipulation methods on Gradient objects."""
    print("=== Testing Gradient HSV Manipulation ===\n")
    
    # Create a test gradient
    colors = ['#ff0000', '#00ff00', '#0000ff']  # Red, Green, Blue
    gradient = Gradient(colors, name='RGB')
    
    print(f"Original gradient: {[c.hex for c in gradient.colors]}")
    
    # Test hue adjustment
    hue_shifted = gradient.adjust_hue(60)
    print(f"Hue +60°: {[c.hex for c in hue_shifted.colors]}")
    
    # Test saturation adjustment
    desaturated = gradient.adjust_saturation(0.5)
    print(f"50% saturation: {[c.hex for c in desaturated.colors]}")
    
    # Test brightness adjustment
    darker = gradient.adjust_brightness(0.7)
    print(f"70% brightness: {[c.hex for c in darker.colors]}")
    
    # Test lightness adjustment
    lighter = gradient.adjust_lightness(1.2)
    print(f"120% lightness: {[c.hex for c in lighter.colors]}")
    
    # Test complementary
    complement = gradient.complementary()
    print(f"Complementary: {[c.hex for c in complement.colors]}")
    print()

def test_gradient_contrast_analysis():
    """Test contrast analysis methods on Gradient objects."""
    print("=== Testing Gradient Contrast Analysis ===\n")
    
    # Create gradients with different contrast levels
    light_colors = ['#ffcccc', '#ccffcc', '#ccccff']  # Light colors
    dark_colors = ['#330000', '#003300', '#000033']   # Dark colors
    
    light_gradient = Gradient(light_colors, name='Light')
    dark_gradient = Gradient(dark_colors, name='Dark')
    
    # Analyze contrast against white background
    light_analysis = light_gradient.analyze_contrast('white')
    dark_analysis = dark_gradient.analyze_contrast('white')
    
    print("Light gradient vs white background:")
    print(f"  Average contrast: {light_analysis['average_contrast']:.2f}")
    print(f"  Min contrast: {light_analysis['min_contrast']:.2f}")
    print(f"  Max contrast: {light_analysis['max_contrast']:.2f}")
    print(f"  AA accessible: {light_analysis['accessible_aa_count']}/{len(light_colors)}")
    print(f"  AAA accessible: {light_analysis['accessible_aaa_count']}/{len(light_colors)}")
    
    print("\nDark gradient vs white background:")
    print(f"  Average contrast: {dark_analysis['average_contrast']:.2f}")
    print(f"  Min contrast: {dark_analysis['min_contrast']:.2f}")
    print(f"  Max contrast: {dark_analysis['max_contrast']:.2f}")
    print(f"  AA accessible: {dark_analysis['accessible_aa_count']}/{len(dark_colors)}")
    print(f"  AAA accessible: {dark_analysis['accessible_aaa_count']}/{len(dark_colors)}")
    print()

def test_gradient_accessibility():
    """Test accessibility adjustment methods on Gradient objects."""
    print("=== Testing Gradient Accessibility ===\n")
    
    # Create a gradient with poor contrast
    poor_colors = ['#ffcccc', '#ccffcc', '#ccccff']
    poor_gradient = Gradient(poor_colors, name='Poor_Contrast')
    
    print(f"Original colors: {[c.hex for c in poor_gradient.colors]}")
    
    # Make accessible against white
    accessible = poor_gradient.make_accessible('white', level='AA')
    print(f"AA accessible: {[c.hex for c in accessible.colors]}")
    
    # Test contrast before and after
    original_analysis = poor_gradient.analyze_contrast('white')
    accessible_analysis = accessible.analyze_contrast('white')
    
    print(f"Original AA score: {original_analysis['accessibility_aa_score']:.2f}")
    print(f"Accessible AA score: {accessible_analysis['accessibility_aa_score']:.2f}")
    print()

def test_swatch_hsv_manipulation():
    """Test HSV manipulation methods on Swatch objects."""
    print("=== Testing Swatch HSV Manipulation ===\n")
    
    # Create a swatch with multiple gradients
    gradients = [
        Gradient(['#ff0000', '#ff8000'], name='Red-Orange'),
        Gradient(['#00ff00', '#80ff00'], name='Green-YellowGreen'),
        Gradient(['#0000ff', '#8000ff'], name='Blue-Purple')
    ]
    swatch = Swatch(gradients)
    
    print("Original swatch:")
    for i, grad in enumerate(swatch.gradients):
        print(f"  {grad.name}: {[c.hex for c in grad.colors]}")
    
    # Test hue adjustment
    hue_shifted = swatch.adjust_hue(30)
    print("\nHue +30°:")
    for i, grad in enumerate(hue_shifted.gradients):
        print(f"  {grad.name}: {[c.hex for c in grad.colors]}")
    
    # Test saturation adjustment
    desaturated = swatch.adjust_saturation(0.6)
    print("\n60% saturation:")
    for i, grad in enumerate(desaturated.gradients):
        print(f"  {grad.name}: {[c.hex for c in grad.colors]}")
    print()

def test_swatch_contrast_analysis():
    """Test contrast analysis methods on Swatch objects."""
    print("=== Testing Swatch Contrast Analysis ===\n")
    
    # Create a swatch with mixed contrast levels
    gradients = [
        Gradient(['#000000', '#333333'], name='Dark'),
        Gradient(['#666666', '#999999'], name='Medium'),
        Gradient(['#cccccc', '#ffffff'], name='Light')
    ]
    swatch = Swatch(gradients)
    
    # Analyze against white background
    analysis = swatch.analyze_contrast('white')
    
    print("Swatch analysis vs white background:")
    print(f"  Total colors: {analysis['total_colors']}")
    print(f"  Overall average contrast: {analysis['overall_average_contrast']:.2f}")
    print(f"  Overall min contrast: {analysis['overall_min_contrast']:.2f}")
    print(f"  Overall max contrast: {analysis['overall_max_contrast']:.2f}")
    print(f"  Overall AA accessible: {analysis['overall_accessible_aa_count']}/{analysis['total_colors']}")
    print(f"  Overall AA score: {analysis['overall_accessibility_aa_score']:.2f}")
    
    print("\nPer-gradient analysis:")
    for grad_analysis in analysis['gradients']:
        grad_data = grad_analysis['analysis']
        print(f"  {grad_analysis['name']}: avg={grad_data['average_contrast']:.2f}, "
              f"AA={grad_data['accessible_aa_count']}/{len(grad_data['contrasts'])}")
    print()

def test_swatch_accessibility():
    """Test accessibility adjustment methods on Swatch objects."""
    print("=== Testing Swatch Accessibility ===\n")
    
    # Create a swatch with poor contrast
    gradients = [
        Gradient(['#ffcccc', '#ffdddd'], name='Light_Reds'),
        Gradient(['#ccffcc', '#ddffdd'], name='Light_Greens')
    ]
    swatch = Swatch(gradients)
    
    print("Original swatch contrast:")
    original_analysis = swatch.analyze_contrast('white')
    print(f"  Overall AA score: {original_analysis['overall_accessibility_aa_score']:.2f}")
    
    # Make accessible
    accessible_swatch = swatch.make_accessible('white', level='AA')
    accessible_analysis = accessible_swatch.analyze_contrast('white')
    
    print("Accessible swatch contrast:")
    print(f"  Overall AA score: {accessible_analysis['overall_accessibility_aa_score']:.2f}")
    
    print("\nColor changes:")
    for i, (orig, acc) in enumerate(zip(swatch.gradients, accessible_swatch.gradients)):
        print(f"  {orig.name}:")
        for j, (orig_color, acc_color) in enumerate(zip(orig.colors, acc.colors)):
            print(f"    {orig_color.hex} -> {acc_color.hex}")
    print()

if __name__ == "__main__":
    test_gradient_hsv_manipulation()
    test_gradient_contrast_analysis()
    test_gradient_accessibility()
    test_swatch_hsv_manipulation()
    test_swatch_contrast_analysis()
    test_swatch_accessibility()
    print("=== All Gradient and Swatch Tests Completed ===")

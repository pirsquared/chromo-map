Accessibility Guide
===================

This guide covers creating accessible color combinations that meet WCAG (Web Content Accessibility Guidelines) standards.

Understanding Color Accessibility
----------------------------------

Color accessibility ensures that content is usable by people with various visual impairments, including:

- **Color blindness** (affecting ~8% of men and ~0.5% of women)
- **Low vision** conditions
- **Age-related vision changes**
- **Different viewing conditions** (bright sunlight, low-quality displays)

WCAG Guidelines
---------------

The Web Content Accessibility Guidelines define contrast requirements:

**Contrast Ratios**
   - **AA Level**: 4.5:1 for normal text, 3:1 for large text
   - **AAA Level**: 7:1 for normal text, 4.5:1 for large text

**Text Size Classifications**
   - **Normal text**: Under 18pt regular or 14pt bold
   - **Large text**: 18pt+ regular or 14pt+ bold

Quick Accessibility Check
--------------------------

Use the built-in functions to check if color combinations are accessible:

.. code-block:: python

   from chromo_map import Color, contrast_ratio, is_accessible
   
   # Check contrast ratio
   text_color = Color('#333333')
   background = Color('#ffffff')
   
   ratio = contrast_ratio(text_color, background)
   print(f"Contrast ratio: {ratio:.2f}")  # 12.63
   
   # Check WCAG compliance
   aa_compliant = is_accessible(text_color, background, level='AA')
   aaa_compliant = is_accessible(text_color, background, level='AAA')
   
   print(f"AA compliant: {aa_compliant}")   # True
   print(f"AAA compliant: {aaa_compliant}") # True

Making Colors Accessible
-------------------------

When you have a color that doesn't meet accessibility requirements, use the optimization functions:

**Basic Accessibility**

.. code-block:: python

   from chromo_map import find_accessible_color
   
   # Start with a brand color that might not be accessible
   brand_color = '#ff6b6b'  # Light red
   background = 'white'
   
   # Make it accessible
   accessible_color = find_accessible_color(brand_color, background, level='AA')
   
   print(f"Original: {brand_color}")
   print(f"Accessible: {accessible_color.hex}")
   print(f"Contrast: {accessible_color.contrast_ratio(Color(background)):.2f}")

**Maximum Contrast Optimization**

For the best possible contrast while maintaining color character:

.. code-block:: python

   from chromo_map import find_maximal_contrast_binary_search
   
   # Find maximum contrast version
   optimized = find_maximal_contrast_binary_search('#ff6b6b', 'white')
   
   print(f"Optimized color: {optimized.hex}")
   print(f"Contrast ratio: {optimized.contrast_ratio(Color('white')):.2f}")

Practical Examples
------------------

**Website Color Palette**

.. code-block:: python

   from chromo_map import Color, find_accessible_color
   
   # Brand colors
   primary = '#3498db'      # Blue
   secondary = '#e74c3c'    # Red
   accent = '#f39c12'       # Orange
   
   # Background colors
   light_bg = '#ffffff'     # White
   dark_bg = '#2c3e50'      # Dark blue
   
   # Ensure all combinations are accessible
   primary_on_light = find_accessible_color(primary, light_bg)
   secondary_on_light = find_accessible_color(secondary, light_bg)
   accent_on_light = find_accessible_color(accent, light_bg)
   
   # For dark backgrounds, often we need lighter text
   primary_on_dark = find_accessible_color(primary, dark_bg)
   
   print("Accessible color palette:")
   print(f"Primary on light: {primary_on_light.hex}")
   print(f"Secondary on light: {secondary_on_light.hex}")
   print(f"Accent on light: {accent_on_light.hex}")
   print(f"Primary on dark: {primary_on_dark.hex}")

**Form Validation Colors**

.. code-block:: python

   from chromo_map import find_accessible_color
   
   # Common form validation colors
   success_base = '#28a745'   # Green
   warning_base = '#ffc107'   # Yellow  
   error_base = '#dc3545'     # Red
   info_base = '#17a2b8'      # Cyan
   
   background = '#ffffff'
   
   # Make all accessible for text on white background
   success_text = find_accessible_color(success_base, background)
   warning_text = find_accessible_color(warning_base, background) 
   error_text = find_accessible_color(error_base, background)
   info_text = find_accessible_color(info_base, background)
   
   validation_colors = {
       'success': success_text.hex,
       'warning': warning_text.hex,
       'error': error_text.hex,
       'info': info_text.hex
   }
   
   print("Accessible validation colors:", validation_colors)

Color Blindness Considerations
------------------------------

Beyond contrast, consider color blindness when choosing colors:

**Problematic Combinations**
   - Red/green (most common color blindness)
   - Blue/purple
   - Green/brown

**Safe Strategies**

.. code-block:: python

   from chromo_map import Color
   
   # Use colors that are distinguishable across color blindness types
   safe_colors = [
       Color('#d73027'),  # Red (safe red)
       Color('#1a9850'),  # Green (safe green)  
       Color('#313695'),  # Blue
       Color('#f46d43'),  # Orange
       Color('#a50026'),  # Dark red
       Color('#74add1')   # Light blue
   ]
   
   # Test: These colors have good separation in HSV space
   for i, color in enumerate(safe_colors):
       print(f"Color {i+1}: {color.hex} (H:{color.hue:.0f}°)")

**Use Additional Visual Cues**
   Don't rely on color alone. Combine with:
   - Icons or symbols
   - Patterns or textures  
   - Typography (bold, italic)
   - Positioning

Testing Your Colors
--------------------

**Automated Testing**

.. code-block:: python

   from chromo_map import Color, is_accessible
   
   def test_color_accessibility(colors, backgrounds):
       """Test all color/background combinations."""
       results = []
       
       for color in colors:
           for bg in backgrounds:
               color_obj = Color(color)
               bg_obj = Color(bg)
               ratio = color_obj.contrast_ratio(bg_obj)
               aa = is_accessible(color, bg, level='AA')
               aaa = is_accessible(color, bg, level='AAA')
               
               results.append({
                   'color': color,
                   'background': bg,
                   'ratio': ratio,
                   'aa': aa,
                   'aaa': aaa
               })
       
       return results
   
   # Test your palette
   text_colors = ['#333333', '#666666', '#999999']
   backgrounds = ['#ffffff', '#f8f9fa', '#e9ecef']
   
   test_results = test_color_accessibility(text_colors, backgrounds)
   
   for result in test_results:
       if result['aa']:
           print(f"✅ {result['color']} on {result['background']}: {result['ratio']:.2f}")
       else:
           print(f"❌ {result['color']} on {result['background']}: {result['ratio']:.2f}")

**Manual Testing Tools**
   - Browser developer tools (accessibility audits)
   - Color blindness simulators
   - Real testing with users who have visual impairments

Advanced Accessibility Features
-------------------------------

**Progressive Enhancement**

.. code-block:: python

   from chromo_map import Color, find_accessible_color
   
   def create_accessible_theme(base_color, backgrounds):
       """Create progressively accessible color variations."""
       base = Color(base_color)
       
       theme = {}
       for bg_name, bg_color in backgrounds.items():
           # Different accessibility levels
           theme[f'{bg_name}_aa'] = find_accessible_color(
               base_color, bg_color, level='AA'
           ).hex
           
           theme[f'{bg_name}_aaa'] = find_accessible_color(
               base_color, bg_color, level='AAA'  
           ).hex
       
       return theme
   
   # Create adaptive theme
   backgrounds = {
       'light': '#ffffff',
       'medium': '#f5f5f5', 
       'dark': '#333333'
   }
   
   brand_theme = create_accessible_theme('#3498db', backgrounds)
   print(brand_theme)

**Dynamic Contrast Adjustment**

.. code-block:: python

   from chromo_map import Color, find_maximal_contrast_optimization
   
   def get_optimal_text_color(background_color):
       """Get the best text color for any background."""
       bg = Color(background_color)
       
       # Test both black and white text
       black_contrast = Color('#000000').contrast_ratio(bg)
       white_contrast = Color('#ffffff').contrast_ratio(bg)
       
       if black_contrast > white_contrast:
           # Optimize black text
           return find_maximal_contrast_optimization('#000000', background_color)
       else:
           # Optimize white text  
           return find_maximal_contrast_optimization('#ffffff', background_color)
   
   # Example usage
   backgrounds = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71']
   
   for bg in backgrounds:
       optimal_text = get_optimal_text_color(bg)
       print(f"Background: {bg} → Text: {optimal_text.hex}")

Best Practices Summary
----------------------

1. **Always test contrast ratios** before finalizing color choices
2. **Aim for AAA compliance** when possible, especially for body text
3. **Use multiple visual cues** beyond color alone
4. **Test with actual users** who have visual impairments
5. **Consider viewing conditions** (mobile devices, bright sunlight)
6. **Maintain brand identity** while ensuring accessibility
7. **Document your accessible color palette** for consistent use

Tools and Resources
-------------------

**chromo-map Functions**
   - ``contrast_ratio()`` - Calculate WCAG contrast ratios
   - ``is_accessible()`` - Check WCAG compliance
   - ``find_accessible_color()`` - Make colors accessible
   - ``find_maximal_contrast_*()`` - Optimize for maximum contrast

**External Tools**
   - WebAIM Contrast Checker
   - Colour Contrast Analyser (CCA)
   - axe DevTools browser extension

**Testing**
   - Lighthouse accessibility audits
   - WAVE (Web Accessibility Evaluation Tool)
   - Color blindness simulators

Remember: Accessibility benefits everyone, not just users with disabilities. High-contrast, well-chosen colors improve readability and user experience for all users.

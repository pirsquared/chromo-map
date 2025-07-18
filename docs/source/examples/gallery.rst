Example Gallery
===============

This gallery showcases practical examples of using chromo-map for various applications.

Jupyter Integration
-------------------

**Interactive Visual Exploration**

chromo-map provides exceptional Jupyter notebook integration with rich visual displays. See our comprehensive interactive demo:

:doc:`jupyter_integration`

This notebook demonstrates:
- Rich color and gradient visualization
- Interactive color manipulation with real-time feedback  
- Professional palette exploration
- matplotlib compatibility examples

Basic Color Operations
----------------------

**Creating and Manipulating Colors**

.. code-block:: python

   from chromo_map import Color
   
   # Create a base color
   sunset_orange = Color('#ff6b35')
   
   # Explore properties
   print(f"Hex: {sunset_orange.hex}")
   print(f"RGB: {sunset_orange.rgb}")
   print(f"HSV: {sunset_orange.hsv}")
   print(f"HSL: {sunset_orange.hsl}")
   
   # Create variations
   lighter = sunset_orange.adjust_lightness(0.2)
   darker = sunset_orange.adjust_lightness(-0.2)
   more_saturated = sunset_orange.adjust_saturation(0.3)
   complementary = sunset_orange.complementary()
   
   variations = {
       'original': sunset_orange.hex,
       'lighter': lighter.hex,
       'darker': darker.hex,
       'more_saturated': more_saturated.hex,
       'complementary': complementary.hex
   }

Web Design Color Schemes
------------------------

**Creating a Website Color Palette**

.. code-block:: python

   from chromo_map import Color, generate_color_palette, find_accessible_color
   
   # Brand primary color
   brand_blue = Color('#2c5aa0')
   
   # Generate harmonious colors
   palette = generate_color_palette(brand_blue, 'analogous', 5)
   
   # Ensure accessibility for web use
   white_bg = '#ffffff'
   accessible_palette = []
   
   for color in palette:
       accessible = find_accessible_color(color, white_bg, level='AA')
       accessible_palette.append(accessible.hex)
   
   # Create semantic colors
   success_green = find_accessible_color('#28a745', white_bg)
   warning_yellow = find_accessible_color('#ffc107', white_bg)
   error_red = find_accessible_color('#dc3545', white_bg)
   
   web_colors = {
       'primary': accessible_palette[2],  # Main brand color
       'secondary': accessible_palette[0], # Supporting color
       'accent': accessible_palette[4],    # Highlight color
       'success': success_green.hex,
       'warning': warning_yellow.hex,
       'error': error_red.hex
   }

Data Visualization
------------------

**Scientific Color Maps**

.. code-block:: python

   from chromo_map import get_gradient, Gradient
   import matplotlib.pyplot as plt
   import numpy as np
   
   # Get a perceptually uniform colormap
   viridis = get_gradient('viridis')
   
   # Create sample data
   data = np.random.rand(10, 10)
   
   # Plot with chromo-map gradient
   plt.figure(figsize=(10, 4))
   
   plt.subplot(1, 2, 1)
   plt.imshow(data, cmap=viridis.to_mpl())
   plt.title('Viridis (Perceptually Uniform)')
   plt.colorbar()
   
   # Custom gradient for comparison
   custom = Gradient(['#440154', '#31688e', '#35b779', '#fde725'], 256)
   
   plt.subplot(1, 2, 2)
   plt.imshow(data, cmap=custom.to_mpl())
   plt.title('Custom Gradient')
   plt.colorbar()
   
   plt.tight_layout()
   plt.show()

**Categorical Data Visualization**

.. code-block:: python

   from chromo_map import generate_color_palette, Color
   import matplotlib.pyplot as plt
   
   # Generate colors for 6 categories
   base_color = '#e74c3c'
   categories = 6
   
   # Create evenly distributed hues
   colors = []
   base = Color(base_color)
   for i in range(categories):
       hue_shift = (360 / categories) * i
       color = base.adjust_hue(hue_shift)
       colors.append(color.hex)
   
   # Sample data
   data = [23, 45, 56, 78, 32, 67]
   labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E', 'Category F']
   
   # Create pie chart
   plt.figure(figsize=(8, 8))
   plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%')
   plt.title('Categorical Data with Harmonious Colors')
   plt.show()

Brand Identity System
---------------------

**Complete Brand Color System**

.. code-block:: python

   from chromo_map import Color, find_accessible_color
   
   def create_brand_identity(primary_hex):
       """Create a complete brand identity color system."""
       primary = Color(primary_hex)
       
       # Core brand colors
       secondary = primary.adjust_hue(30)
       accent = primary.complementary()
       
       # Monochromatic variations
       primary_light = primary.adjust_lightness(0.3).adjust_saturation(-0.2)
       primary_dark = primary.adjust_lightness(-0.3)
       
       # Neutral palette
       neutral_lightest = Color('#f8f9fa')
       neutral_light = Color('#e9ecef')
       neutral_medium = Color('#6c757d')
       neutral_dark = Color('#495057')
       neutral_darkest = Color('#212529')
       
       # Ensure accessibility for text on white
       white = '#ffffff'
       text_primary = find_accessible_color(primary, white, level='AA')
       text_secondary = find_accessible_color(secondary, white, level='AA')
       text_neutral = find_accessible_color(neutral_medium, white, level='AAA')
       
       return {
           'brand': {
               'primary': primary.hex,
               'secondary': secondary.hex,
               'accent': accent.hex,
               'primary_light': primary_light.hex,
               'primary_dark': primary_dark.hex
           },
           'text': {
               'primary': text_primary.hex,
               'secondary': text_secondary.hex,
               'neutral': text_neutral.hex,
               'inverse': neutral_lightest.hex  # For dark backgrounds
           },
           'neutrals': {
               'lightest': neutral_lightest.hex,
               'light': neutral_light.hex,
               'medium': neutral_medium.hex,
               'dark': neutral_dark.hex,
               'darkest': neutral_darkest.hex
           }
       }
   
   # Example: Tech startup brand
   tech_brand = create_brand_identity('#667eea')  # Modern purple-blue
   
   print("Tech Startup Brand Colors:")
   for category, colors in tech_brand.items():
       print(f"\\n{category.upper()}:")
       for name, hex_color in colors.items():
           print(f"  {name}: {hex_color}")

Accessibility Examples
----------------------

**WCAG Compliant Color Palette**

.. code-block:: python

   from chromo_map import find_accessible_color, contrast_ratio, is_accessible
   
   def create_accessible_palette(colors, background='#ffffff'):
       """Ensure all colors meet WCAG AA standards."""
       accessible_colors = {}
       bg = background
       
       for name, color in colors.items():
           # Make accessible
           accessible = find_accessible_color(color, bg, level='AA')
           ratio = contrast_ratio(accessible, bg)
           
           accessible_colors[name] = {
               'original': color,
               'accessible': accessible.hex,
               'contrast_ratio': round(ratio, 2),
               'wcag_aa': is_accessible(accessible, bg, level='AA'),
               'wcag_aaa': is_accessible(accessible, bg, level='AAA')
           }
       
       return accessible_colors
   
   # Original palette (might not be accessible)
   original_palette = {
       'primary': '#3498db',
       'secondary': '#e74c3c', 
       'success': '#2ecc71',
       'warning': '#f39c12',
       'info': '#9b59b6'
   }
   
   # Make it accessible
   accessible_results = create_accessible_palette(original_palette)
   
   print("Accessibility Analysis:")
   for name, data in accessible_results.items():
       print(f"\\n{name.upper()}:")
       print(f"  Original: {data['original']}")
       print(f"  Accessible: {data['accessible']}")
       print(f"  Contrast: {data['contrast_ratio']}:1")
       print(f"  WCAG AA: {'✅' if data['wcag_aa'] else '❌'}")
       print(f"  WCAG AAA: {'✅' if data['wcag_aaa'] else '❌'}")

Seasonal Color Schemes
----------------------

**Creating Seasonal Palettes**

.. code-block:: python

   from chromo_map import Color, Gradient, Swatch
   
   def create_seasonal_palettes():
       """Create color palettes inspired by seasons."""
       
       # Spring - fresh greens and soft pastels
       spring_colors = [
           Color('#8fbc8f'),  # Dark sea green
           Color('#98fb98'),  # Pale green
           Color('#f0fff0'),  # Honeydew
           Color('#ffc0cb'),  # Pink
           Color('#ffb6c1')   # Light pink
       ]
       spring_gradient = Gradient(spring_colors, 20)
       
       # Summer - warm, vibrant colors
       summer_colors = [
           Color('#ff6347'),  # Tomato
           Color('#ffa500'),  # Orange
           Color('#ffd700'),  # Gold
           Color('#ff1493'),  # Deep pink
           Color('#00bfff')   # Deep sky blue
       ]
       summer_gradient = Gradient(summer_colors, 20)
       
       # Autumn - warm, muted earth tones
       autumn_colors = [
           Color('#d2691e'),  # Chocolate
           Color('#cd853f'),  # Peru
           Color('#daa520'),  # Goldenrod
           Color('#b22222'),  # Fire brick
           Color('#a0522d')   # Sienna
       ]
       autumn_gradient = Gradient(autumn_colors, 20)
       
       # Winter - cool blues and whites
       winter_colors = [
           Color('#4682b4'),  # Steel blue
           Color('#b0c4de'),  # Light steel blue
           Color('#f0f8ff'),  # Alice blue
           Color('#e6e6fa'),  # Lavender
           Color('#483d8b')   # Dark slate blue
       ]
       winter_gradient = Gradient(winter_colors, 20)
       
       # Create swatch for comparison
       seasonal_swatch = Swatch([
           spring_gradient,
           summer_gradient, 
           autumn_gradient,
           winter_gradient
       ], ncols=2)
       
       return {
           'spring': spring_gradient,
           'summer': summer_gradient,
           'autumn': autumn_gradient,
           'winter': winter_gradient,
           'swatch': seasonal_swatch
       }
   
   seasonal_palettes = create_seasonal_palettes()

Interactive Jupyter Examples
----------------------------

**Rich Display in Notebooks**

.. code-block:: python

   from chromo_map import Color, Gradient, Swatch
   
   # Colors display as colored squares with hover information
   sunset = Color('#ff6b35')
   ocean = Color('#006994')
   forest = Color('#2d5016')
   
   # Display individual colors
   print("Individual Colors:")
   display(sunset)  # Shows as colored square
   display(ocean)
   display(forest)
   
   # Gradients display as horizontal color bars
   sunset_gradient = Gradient(['#ff6b35', '#ff8e53', '#ffad6a'], 15)
   ocean_gradient = Gradient(['#006994', '#4da6c7', '#8dc3e3'], 15)
   
   print("Gradients:")
   display(sunset_gradient)  # Shows as color bar
   display(ocean_gradient)
   
   # Swatches display as organized grids
   nature_swatch = Swatch([
       Gradient(['#ff6b35', '#ffad6a'], 10),  # Sunset
       Gradient(['#006994', '#8dc3e3'], 10),  # Ocean
       Gradient(['#2d5016', '#7cb342'], 10),  # Forest
       Gradient(['#8e24aa', '#ba68c8'], 10)   # Lavender
   ], ncols=2)
   
   print("Swatch Grid:")
   display(nature_swatch)  # Shows as 2x2 grid

Advanced Contrast Optimization
------------------------------

**Finding Maximum Contrast**

.. code-block:: python

   from chromo_map import (
       find_accessible_color,
       find_maximal_contrast_iterative,
       find_maximal_contrast_binary_search,
       find_maximal_contrast_optimization
   )
   
   def compare_contrast_methods(base_color, background):
       """Compare different contrast optimization methods."""
       methods = {
           'Basic Accessible': find_accessible_color,
           'Enhanced Iterative': find_maximal_contrast_iterative,
           'Binary Search': find_maximal_contrast_binary_search,
           'Mathematical Optimization': find_maximal_contrast_optimization
       }
       
       results = {}
       for name, method in methods.items():
           try:
               optimized = method(base_color, background)
               ratio = optimized.contrast_ratio(Color(background))
               results[name] = {
                   'color': optimized.hex,
                   'contrast': round(ratio, 2)
               }
           except Exception as e:
               results[name] = {'error': str(e)}
       
       return results
   
   # Test with a challenging color
   test_results = compare_contrast_methods('#ff6b6b', 'white')
   
   print("Contrast Optimization Comparison:")
   print(f"Original: #ff6b6b vs white")
   print(f"Original contrast: {Color('#ff6b6b').contrast_ratio(Color('white')):.2f}")
   print("\\nOptimized Results:")
   
   for method, result in test_results.items():
       if 'error' in result:
           print(f"  {method}: Error - {result['error']}")
       else:
           print(f"  {method}: {result['color']} (contrast: {result['contrast']})")

Custom Color Space Operations
-----------------------------

**Working with Different Color Spaces**

.. code-block:: python

   from chromo_map import Color
   import colorsys
   
   def analyze_color_properties(hex_color):
       """Analyze a color across different properties."""
       color = Color(hex_color)
       
       analysis = {
           'input': hex_color,
           'rgb': color.rgb,
           'hsv': color.hsv,
           'hsl': color.hsl,
           'properties': {
               'hue_name': get_hue_name(color.hue),
               'saturation_level': get_saturation_level(color.saturation),
               'brightness_level': get_brightness_level(color.value),
               'warmth': 'warm' if is_warm_color(color.hue) else 'cool'
           }
       }
       
       return analysis
   
   def get_hue_name(hue):
       """Convert hue degrees to color name."""
       hue = hue % 360
       if hue < 15 or hue >= 345: return 'red'
       elif hue < 45: return 'orange'
       elif hue < 75: return 'yellow'
       elif hue < 105: return 'yellow-green'
       elif hue < 135: return 'green'
       elif hue < 165: return 'green-cyan'
       elif hue < 195: return 'cyan'
       elif hue < 225: return 'blue'
       elif hue < 255: return 'blue-purple'
       elif hue < 285: return 'purple'
       elif hue < 315: return 'purple-magenta'
       else: return 'magenta'
   
   def get_saturation_level(saturation):
       """Categorize saturation level."""
       if saturation < 0.2: return 'very low'
       elif saturation < 0.4: return 'low'
       elif saturation < 0.6: return 'medium'
       elif saturation < 0.8: return 'high'
       else: return 'very high'
   
   def get_brightness_level(brightness):
       """Categorize brightness level."""
       if brightness < 0.2: return 'very dark'
       elif brightness < 0.4: return 'dark'
       elif brightness < 0.6: return 'medium'
       elif brightness < 0.8: return 'bright'
       else: return 'very bright'
   
   def is_warm_color(hue):
       """Determine if color is warm or cool."""
       return (hue >= 315 or hue <= 45) or (45 < hue <= 135)
   
   # Analyze some colors
   test_colors = ['#ff6b35', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']
   
   for hex_color in test_colors:
       analysis = analyze_color_properties(hex_color)
       props = analysis['properties']
       print(f"\\n{hex_color}:")
       print(f"  Hue: {props['hue_name']}")
       print(f"  Saturation: {props['saturation_level']}")
       print(f"  Brightness: {props['brightness_level']}")
       print(f"  Temperature: {props['warmth']}")

These examples demonstrate the versatility and power of chromo-map for various color-related tasks. Whether you're designing websites, creating data visualizations, or building brand identities, chromo-map provides the tools to work with colors professionally and accessibly.

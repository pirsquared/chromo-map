Color Theory Guide
==================

This guide covers the color theory principles implemented in chromo-map and how to use them for creating harmonious color schemes.

Understanding Color Theory
---------------------------

Color theory is the science and art of using color. It explains how humans perceive color, how colors mix, match, or clash, and how colors convey meaning.

**Key Concepts**
   - **Hue**: The pure color (red, blue, yellow, etc.)
   - **Saturation**: The intensity or purity of the color
   - **Value/Brightness**: How light or dark the color is
   - **Lightness**: Perceptual brightness in HSL space

The Color Wheel
---------------

The color wheel is the foundation of color theory:

.. code-block:: python

   from chromo_map import Color
   
   # Primary colors (120° apart)
   red = Color('#ff0000')      # 0°
   green = Color('#00ff00')    # 120°
   blue = Color('#0000ff')     # 240°
   
   print(f"Red hue: {red.hue:.0f}°")
   print(f"Green hue: {green.hue:.0f}°")
   print(f"Blue hue: {blue.hue:.0f}°")

Color Harmonies
---------------

chromo-map provides built-in color harmony generation:

**Complementary Colors**

Colors opposite on the color wheel (180° apart):

.. code-block:: python

   from chromo_map import Color, generate_color_palette
   
   base = Color('#ff6b35')  # Orange
   
   # Get complementary color
   complement = base.complementary()
   print(f"Base: {base.hex}")
   print(f"Complement: {complement.hex}")
   
   # Generate complementary palette
   comp_palette = generate_color_palette(
       base_color=base,
       scheme='complementary',
       count=5
   )

**Analogous Colors**

Colors adjacent on the color wheel (within 30° typically):

.. code-block:: python

   # Analogous colors create harmonious, peaceful schemes
   analogous_palette = generate_color_palette(
       base_color='#3498db',  # Blue
       scheme='analogous', 
       count=5
   )
   
   # Manual analogous colors
   base = Color('#3498db')
   analogous_manual = [
       base.adjust_hue(-30),  # Blue-green
       base.adjust_hue(-15),  # Slightly blue-green
       base,                  # Base blue
       base.adjust_hue(15),   # Slightly blue-purple
       base.adjust_hue(30)    # Blue-purple
   ]

**Triadic Colors**

Three colors evenly spaced around the color wheel (120° apart):

.. code-block:: python

   # Triadic schemes are vibrant but balanced
   triadic_palette = generate_color_palette(
       base_color='#e74c3c',  # Red
       scheme='triadic',
       count=3
   )
   
   # Manual triadic
   base = Color('#e74c3c')  # Red (~0°)
   triadic_manual = [
       base,                    # Red
       base.adjust_hue(120),    # Green
       base.adjust_hue(240)     # Blue
   ]

**Split-Complementary**

Base color plus two colors adjacent to its complement:

.. code-block:: python

   # More nuanced than pure complementary
   split_comp_palette = generate_color_palette(
       base_color='#f39c12',  # Orange
       scheme='split_complementary',
       count=4
   )

**Tetradic (Rectangle)**

Four colors forming a rectangle on the color wheel:

.. code-block:: python

   # Rich, diverse palettes
   tetradic_palette = generate_color_palette(
       base_color='#9b59b6',  # Purple
       scheme='tetradic',
       count=4
   )

**Square**

Four colors evenly spaced (90° apart):

.. code-block:: python

   # Bold, dynamic palettes
   square_palette = generate_color_palette(
       base_color='#2ecc71',  # Green
       scheme='square',
       count=4
   )

Monochromatic Schemes
---------------------

Variations of a single hue using different saturation and brightness levels:

.. code-block:: python

   from chromo_map import Color, Gradient
   
   base = Color('#3498db')  # Blue
   
   # Create monochromatic variations
   monochromatic = [
       base.adjust_saturation(-0.6).adjust_lightness(0.3),  # Very light, desaturated
       base.adjust_saturation(-0.3).adjust_lightness(0.15), # Light, slightly desaturated  
       base,                                                # Base color
       base.adjust_saturation(0.2).adjust_lightness(-0.15), # Darker, more saturated
       base.adjust_saturation(0.4).adjust_lightness(-0.3)   # Very dark, highly saturated
   ]
   
   # Or use the built-in function
   mono_palette = generate_color_palette(
       base_color=base,
       scheme='monochromatic',
       count=5,
       saturation_range=(0.3, 1.0),
       brightness_range=(0.4, 1.0)
   )

Advanced Color Relationships
----------------------------

**Color Temperature**

Warm vs. cool colors affect emotional response:

.. code-block:: python

   # Warm colors (reds, oranges, yellows)
   warm_colors = [
       Color('#ff4757'),  # Red
       Color('#ff6348'),  # Orange-red
       Color('#ff7675'),  # Pink-red
       Color('#fdcb6e'),  # Yellow-orange
       Color('#e17055')   # Brown-orange
   ]
   
   # Cool colors (blues, greens, purples)
   cool_colors = [
       Color('#0984e3'),  # Blue
       Color('#74b9ff'),  # Light blue
       Color('#00b894'),  # Green
       Color('#00cec9'),  # Teal
       Color('#6c5ce7')   # Purple
   ]

**Color Intensity and Mood**

.. code-block:: python

   base = Color('#e74c3c')  # Vibrant red
   
   # Create mood variations
   energetic = base.adjust_saturation(0.3).adjust_brightness(0.1)  # More vibrant
   calming = base.adjust_saturation(-0.5).adjust_lightness(0.2)    # Muted, lighter
   dramatic = base.adjust_saturation(0.2).adjust_brightness(-0.3)  # Dark, intense
   
   moods = {
       'energetic': energetic.hex,
       'calming': calming.hex, 
       'dramatic': dramatic.hex
   }

Practical Applications
----------------------

**Brand Color Systems**

.. code-block:: python

   def create_brand_system(primary_color):
       """Create a complete brand color system."""
       primary = Color(primary_color)
       
       return {
           # Core brand colors
           'primary': primary.hex,
           'secondary': primary.complementary().hex,
           'accent': primary.adjust_hue(60).hex,
           
           # Monochromatic variations
           'primary_light': primary.adjust_lightness(0.3).hex,
           'primary_dark': primary.adjust_lightness(-0.3).hex,
           
           # Neutral colors
           'neutral_light': Color('#f8f9fa').hex,
           'neutral_medium': Color('#6c757d').hex,
           'neutral_dark': Color('#343a40').hex,
           
           # Semantic colors (maintaining brand harmony)
           'success': primary.adjust_hue(120).adjust_saturation(-0.2).hex,
           'warning': primary.adjust_hue(45).hex,
           'error': primary.adjust_hue(180).adjust_saturation(0.1).hex
       }
   
   # Example brand system
   brand_colors = create_brand_system('#3498db')
   for role, color in brand_colors.items():
       print(f"{role}: {color}")

**Data Visualization Palettes**

.. code-block:: python

   def create_data_palette(base_color, n_categories):
       """Create palette for categorical data visualization."""
       if n_categories <= 3:
           # Use triadic for small numbers
           return generate_color_palette(base_color, 'triadic', n_categories)
       elif n_categories <= 4:
           # Use square for medium numbers
           return generate_color_palette(base_color, 'square', n_categories)
       else:
           # Use evenly spaced hues for larger numbers
           base = Color(base_color)
           hue_step = 360 / n_categories
           return [base.adjust_hue(i * hue_step) for i in range(n_categories)]
   
   # Create palette for 6 categories
   data_colors = create_data_palette('#e74c3c', 6)
   print([color.hex for color in data_colors])

**Seasonal Color Schemes**

.. code-block:: python

   # Spring palette - fresh, light, analogous greens and yellows
   spring = generate_color_palette('#2ecc71', 'analogous', 5)
   spring_adjusted = [color.adjust_lightness(0.2) for color in spring]
   
   # Summer palette - warm, vibrant
   summer_base = Color('#f39c12')  # Orange
   summer = [
       summer_base.adjust_hue(-30),  # Yellow-orange
       summer_base,                  # Orange
       summer_base.adjust_hue(30),   # Red-orange
       summer_base.adjust_hue(60),   # Red
       summer_base.adjust_hue(90)    # Pink-red
   ]
   
   # Autumn palette - warm, muted
   autumn_base = Color('#d35400')  # Dark orange
   autumn = [color.adjust_saturation(-0.3) for color in 
            generate_color_palette(autumn_base, 'analogous', 5)]
   
   # Winter palette - cool, high contrast
   winter_base = Color('#2980b9')  # Dark blue
   winter = generate_color_palette(winter_base, 'complementary', 4)

Color Psychology
----------------

Different colors evoke different emotional responses:

.. code-block:: python

   # Psychological color associations
   psychology_colors = {
       'trust': Color('#3498db').hex,        # Blue - trust, stability
       'energy': Color('#e74c3c').hex,       # Red - energy, passion
       'growth': Color('#2ecc71').hex,       # Green - growth, nature
       'creativity': Color('#9b59b6').hex,   # Purple - creativity, luxury
       'optimism': Color('#f1c40f').hex,     # Yellow - optimism, happiness
       'sophistication': Color('#34495e').hex, # Dark gray - sophistication
       'purity': Color('#ecf0f1').hex,       # Light gray - purity, cleanliness
   }

Analyzing Existing Palettes
---------------------------

Use chromo-map to analyze the harmony of existing color schemes:

.. code-block:: python

   from chromo_map import analyze_color_harmony
   
   # Analyze a existing palette
   existing_palette = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
   colors = [Color(hex_color) for hex_color in existing_palette]
   
   harmony_analysis = analyze_color_harmony(colors)
   print(f"Harmony type: {harmony_analysis.get('type', 'Unknown')}")
   print(f"Overall score: {harmony_analysis.get('score', 'N/A')}")

Color Blindness Considerations
------------------------------

When applying color theory, consider color blindness:

.. code-block:: python

   # Colors that work well for color blind users
   colorblind_safe = {
       'red': Color('#d73027'),      # Safe red
       'orange': Color('#fc8d62'),   # Orange (distinct from red)
       'yellow': Color('#fee08b'),   # Yellow
       'green': Color('#1a9850'),    # Safe green  
       'blue': Color('#313695'),     # Blue
       'purple': Color('#5e3c99'),   # Purple
       'brown': Color('#8c510a'),    # Brown
       'pink': Color('#fbb4b9')      # Pink
   }
   
   # Test color separation
   for name, color in colorblind_safe.items():
       print(f"{name}: {color.hex} (H: {color.hue:.0f}°, S: {color.saturation:.2f})")

Best Practices
--------------

1. **Start with Purpose**: Choose colors based on the emotional response you want
2. **Use the 60-30-10 Rule**: 60% dominant color, 30% secondary, 10% accent
3. **Test Harmony**: Use chromo-map's harmony functions to validate your choices
4. **Consider Context**: Colors look different depending on surrounding colors
5. **Maintain Accessibility**: Ensure adequate contrast ratios
6. **Be Consistent**: Establish a color system and stick to it
7. **Test with Users**: Real feedback is invaluable

Advanced Techniques
-------------------

**Color Interpolation**

.. code-block:: python

   # Create smooth transitions between colors
   start = Color('#e74c3c')  # Red
   end = Color('#3498db')    # Blue
   
   # Create gradient with specific number of steps
   transition = Gradient([start, end], 10)
   
   # Extract colors at specific points
   quarter_point = transition[2]    # 25% of the way
   midpoint = transition[5]         # 50% of the way
   three_quarter = transition[7]    # 75% of the way

**Dynamic Color Adjustment**

.. code-block:: python

   def adjust_for_accessibility(color, background, maintain_hue=True):
       """Adjust color for accessibility while maintaining character."""
       from chromo_map import find_accessible_color, is_accessible
       
       if is_accessible(color, background):
           return Color(color)
       
       if maintain_hue:
           # Try adjusting saturation and brightness first
           base = Color(color)
           for sat_adj in [-0.2, -0.4, 0.2, 0.4]:
               for bright_adj in [-0.2, -0.4, 0.2, 0.4]:
                   adjusted = base.adjust_saturation(sat_adj).adjust_brightness(bright_adj)
                   if is_accessible(adjusted, background):
                       return adjusted
       
       # Fall back to automatic accessibility adjustment
       return find_accessible_color(color, background)

This guide provides the foundation for understanding and applying color theory with chromo-map. The library's functions implement these principles programmatically, making it easy to create beautiful, harmonious, and accessible color schemes.

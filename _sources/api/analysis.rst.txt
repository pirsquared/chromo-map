Analysis Module
===============

The analysis module provides advanced color analysis, palette generation, and color harmony functions.

Palette Generation
------------------

.. autofunction:: chromo_map.generate_color_palette

Generate color palettes based on color theory principles:

.. code-block:: python

   from chromo_map import generate_color_palette
   
   # Generate complementary palette
   palette = generate_color_palette(
       base_color='#3498db',
       scheme='complementary',
       count=5
   )
   
   # Generate triadic palette
   triadic = generate_color_palette(
       base_color='#e74c3c',
       scheme='triadic',
       count=3
   )

Color Harmony Analysis
----------------------

.. autofunction:: chromo_map.analyze_color_harmony

Analyze the harmony relationships between colors:

.. code-block:: python

   from chromo_map import analyze_color_harmony, Color
   
   colors = [Color('#ff0000'), Color('#00ff00'), Color('#0000ff')]
   
   harmony = analyze_color_harmony(colors)
   print(f"Harmony type: {harmony['type']}")
   print(f"Harmony score: {harmony['score']}")

Gradient Search
---------------

.. autofunction:: chromo_map.get_gradient

Search for gradients in the catalog using flexible patterns:

.. code-block:: python

   from chromo_map import get_gradient
   
   # Exact name search
   viridis = get_gradient('viridis')
   
   # Regex pattern search
   plasma_variants = get_gradient('plasma.*')
   
   # Case-insensitive search
   blues = get_gradient('blues', case_sensitive=False)
   
   # Priority-based search (longest gradient wins)
   blue_gradient = get_gradient('blue', prefer_longer=True)

Available Palette Schemes
-------------------------

The following color harmony schemes are supported:

**Monochromatic**
   Variations of a single hue with different saturation and brightness levels.

**Analogous**
   Colors that are adjacent on the color wheel (within 30 degrees).

**Complementary**
   Colors that are opposite on the color wheel (180 degrees apart).

**Split-Complementary**
   Base color plus two colors adjacent to its complement.

**Triadic**
   Three colors evenly spaced around the color wheel (120 degrees apart).

**Tetradic (Rectangle)**
   Four colors forming a rectangle on the color wheel.

**Square**
   Four colors evenly spaced around the color wheel (90 degrees apart).

Example: Creating Themed Palettes
----------------------------------

.. code-block:: python

   from chromo_map import generate_color_palette, Color
   
   # Create a warm sunset palette
   sunset_base = Color('#ff6b35')  # Orange
   sunset_palette = generate_color_palette(
       base_color=sunset_base,
       scheme='analogous',
       count=5,
       saturation_range=(0.7, 1.0),
       brightness_range=(0.6, 0.9)
   )
   
   # Create a professional blue palette
   business_blue = Color('#2c5aa0')
   business_palette = generate_color_palette(
       base_color=business_blue,
       scheme='monochromatic',
       count=4,
       saturation_range=(0.4, 0.8),
       brightness_range=(0.3, 0.8)
   )

Advanced Analysis Features
--------------------------

Color Distance Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate perceptual distances between colors:

.. code-block:: python

   from chromo_map import Color
   
   color1 = Color('#ff0000')
   color2 = Color('#ff3300')
   
   # Colors have built-in distance calculation
   distance = color1.distance(color2)  # Euclidean distance in RGB
   
   # For more accurate perceptual distance, use HSL
   hsl_distance = color1.distance(color2, space='hsl')

Palette Evaluation
~~~~~~~~~~~~~~~~~~

Evaluate the quality and characteristics of color palettes:

.. code-block:: python

   from chromo_map import analyze_color_harmony
   
   # Evaluate a custom palette
   custom_colors = ['#e74c3c', '#f39c12', '#f1c40f', '#27ae60']
   colors = [Color(c) for c in custom_colors]
   
   analysis = analyze_color_harmony(colors)
   
   print(f"Harmony type: {analysis['type']}")
   print(f"Contrast score: {analysis['contrast_score']}")
   print(f"Accessibility score: {analysis['accessibility_score']}")

Integration with Catalog
-------------------------

The analysis module works seamlessly with the catalog system:

.. code-block:: python

   from chromo_map import get_gradient, analyze_color_harmony
   
   # Get a gradient and analyze its harmony
   gradient = get_gradient('viridis')
   colors = [gradient[i] for i in [0, 25, 50, 75, 99]]  # Sample 5 colors
   
   harmony = analyze_color_harmony(colors)
   print(f"Viridis harmony: {harmony}")

This integration allows you to analyze existing color schemes and create new ones based on proven color theory principles.

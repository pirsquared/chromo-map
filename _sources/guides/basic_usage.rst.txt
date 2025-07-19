Basic Usage Guide
=================

This guide covers the fundamental usage patterns for chromo-map, from basic color creation to working with gradients and swatches.

Getting Started
---------------

First, install chromo-map:

.. code-block:: bash

   pip install chromo-map

Then import the main classes:

.. code-block:: python

   from chromo_map import Color, Gradient, Swatch

Creating Colors
---------------

Colors can be created from various input formats:

**From Hex Strings**

.. code-block:: python

   # Standard 6-digit hex
   red = Color('#ff0000')
   blue = Color('#0066cc')
   
   # Short 3-digit hex (automatically expanded)
   green = Color('#0f0')  # Becomes #00ff00

**From Named Colors**

.. code-block:: python

   # CSS/HTML color names
   red = Color('red')
   blue = Color('cornflowerblue')
   green = Color('forestgreen')

**From RGB Tuples**

.. code-block:: python

   # Integer RGB (0-255)
   red = Color((255, 0, 0))
   blue = Color((0, 102, 204))
   
   # Normalized RGB (0.0-1.0)
   green = Color((0.0, 1.0, 0.0))

**From RGBA (with transparency)**

.. code-block:: python

   # With alpha channel
   semi_transparent_red = Color((255, 0, 0, 0.5))
   transparent_blue = Color('#0066cc80')  # Hex with alpha

Working with Color Properties
-----------------------------

Once you have a Color object, you can access various properties:

.. code-block:: python

   color = Color('#ff6b35')  # Orange color
   
   # Basic properties
   print(f"Hex: {color.hex}")           # #ff6b35
   print(f"RGB: {color.rgb}")           # (255, 107, 53)
   print(f"RGBA: {color.rgba}")         # (255, 107, 53, 1.0)
   
   # Color space conversions
   print(f"HSV: {color.hsv}")           # (16.83, 0.79, 1.0)
   print(f"HSL: {color.hsl}")           # (16.83, 1.0, 0.60)
   
   # Individual components
   print(f"Hue: {color.hue}")           # 16.83 degrees
   print(f"Saturation: {color.saturation}")  # 0.79
   print(f"Value: {color.value}")       # 1.0

Color Manipulation
------------------

Colors can be modified in various ways:

**Adjust Components**

.. code-block:: python

   original = Color('#ff6b35')
   
   # Adjust hue (shift around color wheel)
   shifted = original.adjust_hue(30)     # Shift 30 degrees
   
   # Adjust saturation (color intensity)
   more_saturated = original.adjust_saturation(0.2)   # +20%
   less_saturated = original.adjust_saturation(-0.3)  # -30%
   
   # Adjust brightness/value
   brighter = original.adjust_brightness(0.2)   # +20%
   darker = original.adjust_brightness(-0.2)    # -20%
   
   # Adjust lightness (HSL)
   lighter = original.adjust_lightness(0.1)     # +10%

**Color Relationships**

.. code-block:: python

   base = Color('#3498db')  # Blue
   
   # Get complementary color (opposite on color wheel)
   complement = base.complementary()
   
   # Get analogous colors (adjacent on color wheel)
   analogous = base.analogous(count=3)  # Returns list of 3 colors

Creating Gradients
------------------

Gradients represent sequences of colors with smooth transitions:

**From Color Lists**

.. code-block:: python

   # Simple two-color gradient
   red_to_blue = Gradient(['red', 'blue'], 10)
   
   # Multi-color gradient
   rainbow = Gradient(['red', 'orange', 'yellow', 'green', 'blue'], 20)
   
   # Using Color objects
   colors = [Color('#ff0000'), Color('#00ff00'), Color('#0000ff')]
   custom_gradient = Gradient(colors, 15)

**From Existing Colormaps**

.. code-block:: python

   # From matplotlib colormaps
   viridis = Gradient.from_mpl('viridis', 100)
   plasma = Gradient.from_mpl('plasma', 50)
   
   # From the catalog
   from chromo_map import get_gradient
   cool_gradient = get_gradient('cool')

Working with Gradients
----------------------

Gradients behave like sequences and support many list-like operations:

**Accessing Colors**

.. code-block:: python

   gradient = Gradient(['red', 'blue'], 10)
   
   # Get individual colors
   first_color = gradient[0]         # First color
   last_color = gradient[-1]        # Last color
   middle_color = gradient[5]       # Middle color
   
   # Get slices
   first_half = gradient[:5]        # First 5 colors
   subset = gradient[2:8]           # Colors 2-7

**Gradient Operations**

.. code-block:: python

   original = Gradient(['red', 'blue'], 10)
   
   # Reverse the gradient
   reversed_grad = original.reverse()
   
   # Resample to different length
   longer = original.resample(20)      # 20 colors instead of 10
   shorter = original.resample(5)      # 5 colors instead of 10
   
   # Adjust properties of all colors
   brighter = original.adjust_brightness(0.2)
   more_saturated = original.adjust_saturation(0.3)

Creating Swatches
-----------------

Swatches organize multiple gradients for comparison and display:

.. code-block:: python

   # Create multiple gradients
   gradients = [
       Gradient(['red', 'pink'], 10),
       Gradient(['blue', 'lightblue'], 10),
       Gradient(['green', 'lightgreen'], 10),
       Gradient(['purple', 'lavender'], 10)
   ]
   
   # Create swatch
   swatch = Swatch(gradients, ncols=2)  # Display in 2 columns

Working in Jupyter Notebooks
-----------------------------

chromo-map provides rich visual representations in Jupyter notebooks:

**Color Display**

.. code-block:: python

   # Colors show as colored squares with hover info
   color = Color('#ff6b35')
   color  # Displays as colored square

**Gradient Display**

.. code-block:: python

   # Gradients show as horizontal color bars
   gradient = Gradient(['red', 'blue'], 20)
   gradient  # Displays as smooth color transition

**Swatch Display**

.. code-block:: python

   # Swatches show as organized grids
   swatch = Swatch([
       Gradient(['red', 'white'], 10),
       Gradient(['blue', 'white'], 10)
   ])
   swatch  # Displays as grid of gradients

Common Patterns
---------------

**Creating Theme Colors**

.. code-block:: python

   # Define a base brand color
   brand_color = Color('#3498db')
   
   # Create variations for different UI elements
   primary = brand_color
   secondary = brand_color.adjust_saturation(-0.3)
   accent = brand_color.complementary()
   light = brand_color.adjust_lightness(0.3)
   dark = brand_color.adjust_lightness(-0.3)

**Generating Color Scales**

.. code-block:: python

   # Create a monochromatic scale
   base = Color('#e74c3c')
   scale = Gradient([
       base.adjust_lightness(0.4),   # Very light
       base.adjust_lightness(0.2),   # Light
       base,                         # Base
       base.adjust_lightness(-0.2),  # Dark
       base.adjust_lightness(-0.4)   # Very dark
   ], 20)

**Data Visualization Setup**

.. code-block:: python

   import matplotlib.pyplot as plt
   from chromo_map import get_gradient
   
   # Get a perceptually uniform colormap
   gradient = get_gradient('viridis')
   
   # Use with matplotlib
   plt.imshow(data, cmap=gradient.to_mpl())
   plt.colorbar()

Matplotlib Compatibility
-------------------------

The `Gradient` class is fully compatible with matplotlib colormaps, allowing you to use any chromo-map gradient as a drop-in replacement. This gives you access to professional color schemes from Plotly and Palettable that aren't available in matplotlib.

**Using Plotly Colors in Matplotlib**

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   from chromo_map import cmaps
   
   # Get the Plotly qualitative palette (10 colors)
   plotly_colors = cmaps.plotly_by_type['qualitative']['Plotly']
   
   # Create sample data for area plot
   x = np.linspace(0, 10, 100)
   data = np.array([np.sin(x + i) + i*0.3 for i in range(len(plotly_colors))])
   
   # Create area plot using each color from the Plotly palette
   fig, ax = plt.subplots(figsize=(10, 6))
   for i, series in enumerate(data):
       ax.fill_between(x, i*0.2, series + i*0.2, 
                      color=plotly_colors[i].hex, 
                      alpha=0.7, label=f'Series {i+1}')
   
   ax.set_title('Area Plot Using Plotly Color Palette')
   ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
   plt.tight_layout()

**Enhanced Color Manipulation**

.. code-block:: python

   # Create a lightened version of the same palette
   lightened_colors = plotly_colors.adjust_saturation(.75)
   
   # Create another plot with the modified colors
   fig, ax = plt.subplots(figsize=(10, 6))
   for i, series in enumerate(data):
       ax.fill_between(x, i*0.2, series + i*0.2, 
                      color=lightened_colors[i].hex, 
                      alpha=0.7, label=f'Light Series {i+1}')
   
   ax.set_title('Same Plot with Lightened Plotly Colors')
   ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
   plt.tight_layout()

This demonstrates the key advantage of chromo-map: access to professional color palettes with enhanced manipulation capabilities while maintaining full matplotlib compatibility.

Next Steps
----------

- Learn about :doc:`accessibility` features for WCAG-compliant colors
- Explore :doc:`color_theory` for advanced color relationships
- Check out the :doc:`../examples/gallery` for more complex examples

This covers the fundamental usage patterns. The API is designed to be intuitive and follows Python conventions, making it easy to integrate into existing workflows.

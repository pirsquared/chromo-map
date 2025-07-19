Core Classes
============

The core module contains the fundamental classes for color manipulation in chromo-map.

Color Class
-----------

.. autoclass:: chromo_map.Color
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __str__, __repr__, __eq__, __hash__

The Color class is the fundamental building block for color operations. It provides:

- Multiple input formats (hex, RGB, RGBA, named colors)
- Color space conversions (RGB, HSV, HSL)
- Color manipulation methods (adjust hue, saturation, brightness)
- Accessibility methods (contrast ratio, WCAG compliance)
- Rich display representations for Jupyter notebooks

Example Usage:

.. code-block:: python

   from chromo_map import Color
   
   # Create colors in different formats
   red = Color('red')
   blue = Color('#0066cc')
   green = Color('rgb(0, 255, 0)')
   
   # Access color properties
   print(f"Red HSV: {red.hsv}")
   print(f"Blue hex: {blue.hex}")
   
   # Color manipulation
   darker_red = red.adjust_brightness(-0.2)
   complementary = red.complementary()

Gradient Class
--------------

.. autoclass:: chromo_map.Gradient
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __str__, __repr__, __len__, __getitem__

The Gradient class represents sequences of colors with interpolation capabilities:

- Create gradients from color lists, matplotlib colormaps, or palettes
- Resample to different lengths
- Apply transformations (reverse, adjust alpha)
- Rich HTML representations
- Integration with matplotlib and plotly

Example Usage:

.. code-block:: python

   from chromo_map import Gradient, Color
   
   # Create gradients
   grad1 = Gradient(['red', 'blue'], 10)
   grad2 = Gradient.from_mpl('viridis', 20)
   
   # Manipulate gradients
   reversed_grad = grad1.reverse()
   resampled = grad1.resample(5)
   
   # Access colors
   first_color = grad1[0]
   middle_colors = grad1[2:8]

Swatch Class
------------

.. autoclass:: chromo_map.Swatch
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __str__, __repr__, __len__

The Swatch class manages collections of gradients with grid-based visualization:

- Organize multiple gradients
- Grid-based display in Jupyter notebooks
- Batch operations on gradient collections
- Export capabilities

Example Usage:

.. code-block:: python

   from chromo_map import Swatch, Gradient
   
   # Create swatch with multiple gradients
   gradients = [
       Gradient(['red', 'white'], 10),
       Gradient(['blue', 'white'], 10),
       Gradient(['green', 'white'], 10)
   ]
   
   swatch = Swatch(gradients, ncols=2)
   
   # Display in Jupyter (shows as grid)
   swatch

Class Hierarchy
---------------

.. inheritance-diagram:: chromo_map.Color chromo_map.Gradient chromo_map.Swatch
   :parts: 1

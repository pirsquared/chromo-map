Utility Functions
=================

The utilities module provides helper functions for color format conversion and manipulation.

Color Format Conversion
------------------------

.. autofunction:: chromo_map.rgba_to_tup

Convert RGBA values to tuples:

.. code-block:: python

   from chromo_map import rgba_to_tup
   
   # Convert rgba string to tuple
   rgba_str = "rgba(255, 128, 0, 0.8)"
   rgba_tuple = rgba_to_tup(rgba_str)
   print(rgba_tuple)  # (255, 128, 0, 0.8)

.. autofunction:: chromo_map.hexstr_to_tup

Convert hex strings to RGB tuples:

.. code-block:: python

   from chromo_map import hexstr_to_tup
   
   # Convert hex to RGB tuple
   hex_color = "#ff8000"
   rgb_tuple = hexstr_to_tup(hex_color)
   print(rgb_tuple)  # (255, 128, 0)
   
   # Works with 3-digit hex too
   short_hex = "#f80"
   rgb_tuple = hexstr_to_tup(short_hex)
   print(rgb_tuple)  # (255, 136, 0)

.. autofunction:: chromo_map.clr_to_tup

Universal color-to-tuple converter:

.. code-block:: python

   from chromo_map import clr_to_tup
   
   # Works with various formats
   from_hex = clr_to_tup("#ff8000")        # (255, 128, 0)
   from_rgba = clr_to_tup("rgba(255, 128, 0, 1)")  # (255, 128, 0, 1)
   from_name = clr_to_tup("orange")        # Named color
   from_tuple = clr_to_tup((255, 128, 0))  # Pass-through

Format Support
--------------

The utility functions support a wide range of color formats:

**Hex Formats**
   - ``#RRGGBB`` (6-digit hex)
   - ``#RGB`` (3-digit hex, expanded to 6-digit)
   - With or without the ``#`` prefix

**RGB/RGBA Formats**
   - ``rgb(r, g, b)`` string format
   - ``rgba(r, g, b, a)`` string format with alpha
   - Tuple formats: ``(r, g, b)`` and ``(r, g, b, a)``

**Named Colors**
   - CSS color names (``red``, ``blue``, ``orange``, etc.)
   - Matplotlib color names
   - X11 color names

**Normalized Formats**
   - Floating-point values in range [0, 1]
   - Integer values in range [0, 255]

Conversion Examples
-------------------

**Hex to RGB**

.. code-block:: python

   from chromo_map import hexstr_to_tup
   
   colors = ["#ff0000", "#00ff00", "#0000ff"]
   rgb_colors = [hexstr_to_tup(color) for color in colors]
   print(rgb_colors)
   # [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

**RGBA String Parsing**

.. code-block:: python

   from chromo_map import rgba_to_tup
   
   rgba_strings = [
       "rgba(255, 0, 0, 1.0)",
       "rgba(0, 255, 0, 0.5)",
       "rgb(0, 0, 255)"  # Also handles rgb format
   ]
   
   tuples = [rgba_to_tup(rgba) for rgba in rgba_strings]
   print(tuples)
   # [(255, 0, 0, 1.0), (0, 255, 0, 0.5), (0, 0, 255)]

**Universal Conversion**

.. code-block:: python

   from chromo_map import clr_to_tup
   
   mixed_formats = [
       "#ff0000",              # Hex
       "rgb(0, 255, 0)",       # RGB string
       "blue",                 # Named color
       (255, 255, 0),          # RGB tuple
       (255, 0, 255, 0.8)      # RGBA tuple
   ]
   
   standardized = [clr_to_tup(color) for color in mixed_formats]

Error Handling
--------------

The utility functions include robust error handling:

.. code-block:: python

   from chromo_map import clr_to_tup
   
   try:
       # Invalid hex format
       result = clr_to_tup("#invalid")
   except ValueError as e:
       print(f"Error: {e}")
   
   try:
       # Invalid RGB values
       result = clr_to_tup("rgb(300, 400, 500)")  # Values > 255
   except ValueError as e:
       print(f"Error: {e}")

Integration with Core Classes
-----------------------------

These utilities are used internally by the core classes but are also available for direct use:

.. code-block:: python

   from chromo_map import Color, clr_to_tup
   
   # Manual conversion
   rgb_tuple = clr_to_tup("#ff8000")
   
   # Automatic conversion in Color class
   color = Color("#ff8000")  # Uses clr_to_tup internally
   
   # Both produce equivalent results
   assert color.rgb == rgb_tuple[:3]  # (ignoring alpha)

Performance Considerations
--------------------------

**Caching**
   The conversion functions use internal caching for named colors to improve performance.

**Input Validation**
   All functions validate input formats and provide clear error messages for invalid inputs.

**Memory Efficiency**
   Functions avoid creating unnecessary intermediate objects for large batch conversions.

Best Practices
--------------

**Use Universal Converter**
   When working with mixed input formats, use ``clr_to_tup()`` for consistency.

**Batch Processing**
   For converting many colors, consider using list comprehensions or map():

.. code-block:: python

   from chromo_map import clr_to_tup
   
   # Efficient batch conversion
   hex_colors = ["#ff0000", "#00ff00", "#0000ff"]
   rgb_tuples = list(map(clr_to_tup, hex_colors))

**Type Consistency**
   Ensure consistent output types in your applications by choosing the appropriate conversion function.

Extension Points
----------------

The utility module is designed to be extensible. You can add custom format support by:

1. Extending the conversion functions
2. Adding new format detection logic
3. Integrating with additional color libraries

This makes chromo-map adaptable to specialized color format requirements in specific domains.

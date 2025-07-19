Accessibility Module
====================

The accessibility module provides functions for creating WCAG-compliant color combinations and maximizing contrast ratios.

Contrast Analysis
-----------------

.. autofunction:: chromo_map.contrast_ratio

Calculate the contrast ratio between two colors according to WCAG guidelines.

.. code-block:: python

   from chromo_map import Color, contrast_ratio
   
   color1 = Color('#ff0000')  # Red
   color2 = Color('#ffffff')  # White
   
   ratio = contrast_ratio(color1, color2)
   print(f"Contrast ratio: {ratio:.2f}")  # Should be ~4.0

.. autofunction:: chromo_map.is_accessible

Check if a color combination meets WCAG accessibility standards.

.. code-block:: python

   from chromo_map import is_accessible
   
   # Check AA compliance (4.5:1 for normal text)
   accessible_aa = is_accessible('#666666', 'white', level='AA')
   
   # Check AAA compliance (7:1 for normal text)
   accessible_aaa = is_accessible('#666666', 'white', level='AAA')

Color Optimization
------------------

.. autofunction:: chromo_map.find_accessible_color

Find an accessible version of a color that meets WCAG requirements.

.. code-block:: python

   from chromo_map import find_accessible_color
   
   # Make a color accessible against white background
   original = '#ff6b6b'  # Light red
   accessible = find_accessible_color(original, 'white', level='AA')
   
   print(f"Original: {original}")
   print(f"Accessible: {accessible.hex}")

Advanced Contrast Optimization
------------------------------

.. autofunction:: chromo_map.find_maximal_contrast_iterative

Enhanced iterative approach for finding maximum contrast:

.. code-block:: python

   from chromo_map import find_maximal_contrast_iterative
   
   # Find maximum contrast using iterative approach
   optimized = find_maximal_contrast_iterative('#888888', 'white')
   print(f"Optimized color: {optimized.hex}")

.. autofunction:: chromo_map.find_maximal_contrast_binary_search

Binary search approach for precise contrast optimization:

.. code-block:: python

   from chromo_map import find_maximal_contrast_binary_search
   
   # Find maximum contrast using binary search
   optimized = find_maximal_contrast_binary_search(
       '#888888', 'white', precision=0.001
   )

.. autofunction:: chromo_map.find_maximal_contrast_optimization

Mathematical optimization approach for absolute maximum contrast:

.. code-block:: python

   from chromo_map import find_maximal_contrast_optimization
   
   # Find absolute maximum contrast
   optimized = find_maximal_contrast_optimization(
       '#888888', 'white', method='golden_section'
   )

When to Use Each Method
-----------------------

**find_accessible_color**
   Use when you need basic WCAG compliance quickly. Good for most web applications.

**find_maximal_contrast_iterative**
   Use when you want better results than basic accessibility but don't need perfect optimization.

**find_maximal_contrast_binary_search**
   Use when you need precise, consistent results with good performance.

**find_maximal_contrast_optimization**
   Use when you need the absolute best contrast possible and can afford computational cost.

Performance Comparison
----------------------

.. list-table:: Method Performance
   :header-rows: 1
   :widths: 30 20 20 30

   * - Method
     - Speed
     - Accuracy
     - Best Use Case
   * - find_accessible_color
     - Fastest
     - Good
     - Basic compliance
   * - iterative
     - Fast
     - Better
     - Balanced performance
   * - binary_search
     - Medium
     - High
     - Automated systems
   * - optimization
     - Slower
     - Highest
     - Maximum quality

WCAG Guidelines
---------------

The Web Content Accessibility Guidelines (WCAG) define contrast requirements:

- **AA Level**: 4.5:1 for normal text, 3:1 for large text
- **AAA Level**: 7:1 for normal text, 4.5:1 for large text
- **Large text**: 18pt+ or 14pt+ bold

All accessibility functions in chromo-map follow these standards.

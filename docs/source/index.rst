chromo-map - Color Management Library
=====================================

A powerful Python package for color manipulation, accessibility compliance, and color palette generation. The `Gradient` class is fully compatible with matplotlib colormaps, giving you access to hundreds of professional color schemes from Plotly, Palettable, and matplotlib through a single, unified interface.

**Key Advantage**: Use any chromo-map gradient as a drop-in replacement for matplotlib colormaps while gaining access to enhanced color manipulation features.

Installation
------------

.. code-block:: bash

   pip install chromo-map

Quick Start
-----------

.. code-block:: python

   from chromo_map import Color, Gradient, find_accessible_color, cmaps
   import matplotlib.pyplot as plt
   import numpy as np

   # Create colors
   color = Color('#ff6b6b')

   # Find accessible version
   accessible = find_accessible_color('#ff6b6b', 'white')
   print(f"Accessible color: {accessible.hex}")

   # Work with gradients (matplotlib compatible!)
   grad = Gradient(['red', 'blue'], 10)

   # Use Plotly colors in matplotlib plots
   plotly_colors = cmaps.plotly_by_type['qualitative']['Plotly']

   # Generate sample data for the scatter plot
   x = np.random.randn(50)
   y = np.random.randn(50)

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/core
   api/accessibility
   api/analysis
   api/catalog
   api/utilities

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   guides/basic_usage
   guides/accessibility
   guides/color_theory

.. toctree::
   :maxdepth: 1
   :caption: Interactive Examples:

   examples/jupyter_integration
   examples/gallery
   
.. toctree::
   :maxdepth: 1
   :caption: Visual Catalogs:

   catalog_visual
   catalog_plotly
   catalog_matplotlib
   catalog_palettable

.. toctree::
   :maxdepth: 1
   :caption: Additional:

   about
   phase5_documentation

Coverage Report
---------------

The test coverage report can be found `here <_static/coverage/index.html>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


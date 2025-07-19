Jupyter Integration
===================

chromo-map provides exceptional integration with Jupyter notebooks, offering rich visual representations for colors, gradients, and swatches. This makes it perfect for interactive color exploration and development.

Interactive Notebook Demo
-------------------------

The following notebook demonstrates all the key Jupyter integration features with live examples:

.. toctree::
   :maxdepth: 1

   jupyter_integration_demo.ipynb

Key Features
------------

**Rich Visual Display**
   - Colors display as colored squares with detailed information
   - Gradients show as smooth horizontal color bars  
   - Swatches organize multiple gradients in neat grids

**Interactive Exploration**
   - Real-time visual feedback for color manipulations
   - Immediate results when adjusting brightness, saturation, hue
   - Side-by-side comparisons of color variations

**Professional Integration**
   - Access to hundreds of curated color palettes
   - Visual browsing of Plotly, matplotlib, and Palettable collections
   - Perfect for iterative color design workflows

**matplotlib Compatibility**
   - Use any chromo-map gradient as a matplotlib colormap
   - Access professional color schemes not available in matplotlib
   - Enhanced color manipulation while maintaining full compatibility

Getting Started
---------------

To get started with chromo-map in Jupyter:

1. **Install chromo-map**: ``pip install chromo-map``
2. **Launch Jupyter**: ``jupyter notebook`` or ``jupyter lab``
3. **Import and explore**:

.. code-block:: python

   from chromo_map import Color, Gradient, cmaps
   
   # Colors display automatically
   Color('#ff6b35')
   
   # Gradients show as color bars
   Gradient(['red', 'blue'], 20)
   
   # Access professional palettes
   cmaps.plotly_by_type['qualitative']['Plotly']

The notebook above provides comprehensive examples of all these features in action!

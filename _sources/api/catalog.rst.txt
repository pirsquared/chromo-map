Catalog Module
==============

The catalog module provides access to over 240 carefully curated color gradients from popular libraries including matplotlib, Plotly, and Palettable.

Catalog Access
--------------

The main catalog object provides organized access to over 240 color gradients:

.. code-block:: python

   from chromo_map import cmaps
   
   # Access different catalog sources
   mpl_maps = cmaps.matplotlib_by_type
   plotly_maps = cmaps.plotly_by_type  
   palettable_maps = cmaps.palettable_by_type
   
   # Access all maps in a flat structure
   all_maps = cmaps.all
   
   # Example: Get a specific gradient
   viridis = cmaps.all['viridis']
   plasma = cmaps.all['plasma']

The catalog is organized by source and type, making it easy to discover and access color palettes from different libraries.

Matplotlib Integration
----------------------

Access matplotlib's extensive colormap collection:

.. code-block:: python

   from chromo_map import cmaps
   
   # Browse matplotlib categories
   print(list(cmaps.matplotlib.keys()))
   # Output: ['Perceptually Uniform Sequential', 'Sequential', 'Diverging', ...]
   
   # Access specific categories
   sequential = cmaps.matplotlib['Sequential']
   diverging = cmaps.matplotlib['Diverging']
   
   # Get specific colormaps
   viridis = cmaps.matplotlib['Perceptually Uniform Sequential']['viridis']
   plasma = cmaps.matplotlib['Perceptually Uniform Sequential']['plasma']

Plotly Color Scales
--------------------

Access Plotly's beautiful color scales:

.. code-block:: python

   from chromo_map import cmaps
   
   # Browse Plotly scales
   print(list(cmaps.plotly.keys()))
   
   # Access specific scales
   plotly_viridis = cmaps.plotly['Viridis']
   plotly_plasma = cmaps.plotly['Plasma']
   
   # Plotly categorical scales
   plotly_set1 = cmaps.plotly['Set1']

Palettable Collections
----------------------

Access curated palettes from the Palettable library:

.. code-block:: python

   from chromo_map import cmaps
   
   # Browse Palettable collections
   print(list(cmaps.palettable.keys()))
   # Output: ['cartocolors', 'colorbrewer', 'scientific', ...]
   
   # Access ColorBrewer palettes
   colorbrewer = cmaps.palettable['colorbrewer']
   
   # Scientific color palettes
   scientific = cmaps.palettable['scientific']

Catalog Organization
--------------------

The catalog is hierarchically organized:

.. code-block:: text

   cmaps/
   ├── matplotlib/
   │   ├── Perceptually Uniform Sequential/
   │   │   ├── viridis
   │   │   ├── plasma
   │   │   └── ...
   │   ├── Sequential/
   │   └── Diverging/
   ├── plotly/
   │   ├── Viridis
   │   ├── Plasma
   │   └── ...
   └── palettable/
       ├── colorbrewer/
       ├── scientific/
       └── cartocolors/

Search and Discovery
--------------------

Multiple ways to find the perfect colormap:

**Direct Access**

.. code-block:: python

   # If you know exactly what you want
   viridis = cmaps.matplotlib['Perceptually Uniform Sequential']['viridis']

**Search Function**

.. code-block:: python

   from chromo_map import get_gradient
   
   # Flexible search with patterns
   viridis = get_gradient('viridis')  # Exact match
   blues = get_gradient('blue.*')     # Regex pattern
   any_plasma = get_gradient('plasma', case_sensitive=False)

**Browsing**

.. code-block:: python

   # Explore available options
   for category in cmaps.matplotlib:
       print(f"Category: {category}")
       for name in list(cmaps.matplotlib[category].keys())[:3]:
           print(f"  - {name}")

Catalog Properties
------------------

**Lazy Loading**
   Color maps are loaded only when accessed, keeping memory usage low.

**Automatic Conversion**
   All colormaps are automatically converted to chromo-map Gradient objects.

**Consistent Interface**
   Regardless of source (matplotlib, Plotly, Palettable), all gradients have the same interface.

**Rich Metadata**
   Each gradient includes information about its source, length, and characteristics.

Working with Gradients
-----------------------

Once you have a gradient from the catalog, you can use all chromo-map features:

.. code-block:: python

   from chromo_map import get_gradient
   
   # Get a gradient
   viridis = get_gradient('viridis')
   
   # Use chromo-map features
   reversed_viridis = viridis.reverse()
   shorter_viridis = viridis.resample(50)
   
   # Access individual colors
   start_color = viridis[0]
   end_color = viridis[-1]
   
   # Create variations
   darker_viridis = viridis.adjust_brightness(-0.2)

Catalog Statistics
------------------

The catalog contains:

- **Matplotlib**: 100+ colormaps across 8 categories
- **Plotly**: 20+ built-in color scales
- **Palettable**: 200+ curated scientific and cartographic palettes
- **Total**: 300+ high-quality color gradients

Popular Gradients
-----------------

Some of the most commonly used gradients:

**For Data Visualization**
   - viridis, plasma, inferno (perceptually uniform)
   - coolwarm, RdBu (diverging)
   - Blues, Reds, Greens (sequential)

**For Scientific Applications**
   - jet (classic, though not perceptually uniform)
   - thermal, matter, algae (scientific palettes)

**For Web/UI Design**
   - Plotly color scales for modern aesthetics
   - ColorBrewer palettes for print-safe colors

Integration Examples
--------------------

The catalog integrates seamlessly with plotting libraries:

.. code-block:: python

   import matplotlib.pyplot as plt
   from chromo_map import get_gradient
   
   # Use with matplotlib
   gradient = get_gradient('viridis')
   plt.imshow(data, cmap=gradient.to_mpl())
   
   # Use with plotly
   import plotly.graph_objects as go
   colors = [color.hex for color in gradient]
   fig = go.Figure(data=go.Scatter(y=data, marker=dict(color=colors)))

This makes chromo-map a powerful bridge between different color libraries and visualization tools.

Visual Gallery
--------------

For a visual overview of all available color palettes, browse our organized galleries:

:doc:`Visual Color Catalog Overview <../catalog_visual>`

**Individual Source Galleries:**

- :doc:`Plotly Color Scales <../catalog_plotly>` - Modern web-friendly colors
- :doc:`Matplotlib Colormaps <../catalog_matplotlib>` - Scientific colormaps  
- :doc:`Palettable Palettes <../catalog_palettable>` - Professional color schemes

These galleries display all color palettes with beautiful visual swatches, organized by source and type for easy browsing and selection.

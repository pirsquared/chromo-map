"""chromo_map package for color management."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap as LSC

from .core.color import Color
from .core.gradient import Gradient
from .core.swatch import Swatch

# Import from the new modular structure
from .utils.color_utils import rgba_to_tup, hexstr_to_tup, clr_to_tup

from .accessibility.contrast import (
    contrast_ratio,
    is_accessible,
    find_accessible_color,
    find_maximal_contrast_iterative,
    find_maximal_contrast_binary_search,
    find_maximal_contrast_optimization,
)

from .analysis.palette import (
    generate_color_palette,
    analyze_color_harmony,
    get_gradient,
)

# Import the catalog
from .catalog import cmaps
from pirrtools import AttrDict

__all__ = [
    "Color",
    "Gradient",
    "Swatch",
    "plt",
    "np",
    "LSC",
    "AttrDict",
    # Utility functions
    "rgba_to_tup",
    "hexstr_to_tup",
    "clr_to_tup",
    # Accessibility functions
    "contrast_ratio",
    "is_accessible",
    "find_accessible_color",
    "find_maximal_contrast_iterative",
    "find_maximal_contrast_binary_search",
    "find_maximal_contrast_optimization",
    # Analysis functions
    "generate_color_palette",
    "analyze_color_harmony",
    "get_gradient",
    # Catalog
    "cmaps",
]

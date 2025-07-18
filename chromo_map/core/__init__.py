"""Core color functionality for chromo_map."""

from .color import (
    Color,
    find_accessible_color,
    find_maximal_contrast_iterative,
    find_maximal_contrast_binary_search,
    find_maximal_contrast_optimization,
    rgba_to_tup,
    hexstr_to_tup,
    clr_to_tup,
)

from .gradient import Gradient
from .swatch import Swatch

__all__ = [
    "Color",
    "Gradient",
    "find_accessible_color",
    "find_maximal_contrast_iterative",
    "find_maximal_contrast_binary_search",
    "find_maximal_contrast_optimization",
    "rgba_to_tup",
    "hexstr_to_tup",
    "clr_to_tup",
]

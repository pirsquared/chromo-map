"""Catalog module for chromo_map package."""

from .builders import (_build_matplotlib_catalog, _build_palettable_catalog,
                       _build_plotly_catalog, _build_unified_catalog)
from .catalog import ColorMapDict, cmaps

__all__ = [
    "ColorMapDict",
    "cmaps",
    "_build_matplotlib_catalog",
    "_build_plotly_catalog",
    "_build_palettable_catalog",
    "_build_unified_catalog",
]

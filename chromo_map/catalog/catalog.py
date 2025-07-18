# mypy: ignore-errors
"""Catalog class for chromo_map package."""

from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
from pirrtools import AttrDict

if TYPE_CHECKING:
    from chromo_map.core.gradient import Gradient
    from chromo_map.core.swatch import Swatch
else:
    from chromo_map.core.gradient import Gradient
    from chromo_map.core.swatch import Swatch


class ColorMapDict(AttrDict):
    """AttrDict subclass that displays collections of gradients as a Swatch."""

    def _repr_html_(self) -> str:
        """Return HTML representation for Jupyter notebook display."""
        # Collect all gradient values from this dict
        gradients = []
        for value in self.values():
            if isinstance(value, Gradient):
                gradients.append(value)
            elif isinstance(value, ColorMapDict):
                # Recursively collect gradients from nested dicts
                gradients.extend(self._collect_gradients(value))

        if gradients:
            swatch = Swatch(gradients)
            return swatch._repr_html_()
        return f"<div>Empty ColorMapDict with {len(self)} categories</div>"

    def _collect_gradients(self, nested_dict):
        """Recursively collect all gradients from nested structure."""
        gradients = []
        for value in nested_dict.values():
            if isinstance(value, Gradient):
                gradients.append(value)
            elif isinstance(value, ColorMapDict):
                gradients.extend(self._collect_gradients(value))
        return gradients


def _dig_for_gradients(gradient_nest, prefix=tuple()):
    """Recursively dig through nested structures to find gradients."""
    for name, value in gradient_nest.items():
        if isinstance(value, dict):
            yield from _dig_for_gradients(value, (*prefix, name))
        else:
            yield ((*prefix, name), value)


def _gud_name(name):
    """Check if a name is a valid gradient name (not private or reversed)."""
    return not (name[0] == "_" or name[-2:] == "_r")


# Build the unified colormap catalog
try:
    from .builders import _build_unified_catalog

    cmaps = _build_unified_catalog()
except ImportError:
    # Fallback in case of circular import
    cmaps = None

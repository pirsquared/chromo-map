"""Color utility functions for chromo_map package."""

import re
from typing import Tuple, Optional, Any, List
from matplotlib.colors import to_rgba, to_rgb
import matplotlib.pyplot as plt


# Color parsing utilities
def _rgb_c(c: str) -> str:
    """Helper function for regex pattern building."""
    return rf"(?P<{c}>[^,\s]+)"


_COMMA = r"\s*,\s*"
_red = _rgb_c("red")
_grn = _rgb_c("grn")
_blu = _rgb_c("blu")
_alp = _rgb_c("alp")
_rgb_pat = _COMMA.join([_red, _grn, _blu]) + f"({_COMMA}{_alp})?"
_RGB_PATTERN = re.compile(rf"rgba?\({_rgb_pat}\)")

_VALID_MPL_COLORS = plt.colormaps()


def rgba_to_tup(rgbstr: str) -> Optional[Tuple[float, float, float, float]]:
    """Convert an RGBA string to a tuple."""
    match = _RGB_PATTERN.match(rgbstr)
    if match:
        gdict = match.groupdict()
        red = int(gdict["red"])
        grn = int(gdict["grn"])
        blu = int(gdict["blu"])
        if (alp := gdict["alp"]) is not None:
            alp = float(alp)
            if not 0 <= alp <= 1:
                raise ValueError("Alpha must be between 0 and 1.")
        else:
            alp = 1
        rgb_vals = to_rgb(f"#{red:02x}{grn:02x}{blu:02x}")
        return (rgb_vals[0], rgb_vals[1], rgb_vals[2], alp)
    return None


def hexstr_to_tup(hexstr: str) -> Optional[Tuple[float, float, float, float]]:
    """Convert a hex string to a tuple."""
    try:
        rgba_vals = to_rgba(hexstr)
        return (rgba_vals[0], rgba_vals[1], rgba_vals[2], rgba_vals[3])
    except ValueError:
        return None


def _is_valid_color_values(vals: List[float]) -> bool:
    """Check if values are valid color values (0-1 range)."""
    return all(0 <= x <= 1 for x in vals)


def clr_to_tup(clr: Any) -> Any:
    """Convert a color to a tuple."""
    if isinstance(clr, str):
        return hexstr_to_tup(clr) or rgba_to_tup(clr)

    if isinstance(clr, (tuple, list)):
        clr_list = list(clr)

        # Handle 3 or 4 element sequences
        if len(clr_list) in (3, 4):
            try:
                numeric_vals = [float(x) for x in clr_list]
                if _is_valid_color_values(numeric_vals):
                    # Add alpha if missing
                    if len(numeric_vals) == 3:
                        numeric_vals.append(1.0)
                    return tuple(numeric_vals)
            except (ValueError, TypeError):
                pass

        # Return original format if not valid color values
        return tuple(clr_list) if isinstance(clr, tuple) else clr_list

    # Try matplotlib's to_rgba as fallback
    try:
        rgba_vals = to_rgba(clr)
        return (rgba_vals[0], rgba_vals[1], rgba_vals[2], rgba_vals[3])
    except (ValueError, TypeError):
        return None

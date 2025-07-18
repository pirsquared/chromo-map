"""
Gradient class for chromo-map.

This module contains the Gradient class that represents a color gradient
and provides methods for color interpolation, resizing, and accessibility adjustments.
"""

import base64
import uuid
from math import gcd
from functools import reduce
from textwrap import dedent
from typing import Any, Dict, List, Union

import numpy as np
import svgwrite
from bs4 import BeautifulSoup
from IPython.display import HTML
from jinja2 import Template
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
from matplotlib.colors import ListedColormap as LC
from PIL import Image

from chromo_map.core.color import Color


def lcm(a, b):
    """Calculate the least common multiple of two numbers."""
    return abs(a * b) // gcd(a, b)


def lcm_of_list(numbers):
    """Calculate the least common multiple of a list of numbers."""
    return reduce(lcm, numbers)


class Gradient(LSC):
    """A color gradient class that extends matplotlib's LinearSegmentedColormap.

    This class provides functionality for creating and manipulating color gradients,
    including interpolation, resizing, and accessibility adjustments.

    Parameters
    ----------
    colors : various
        Input colors in various formats (list, Gradient, colormap, etc.)
    name : str, optional
        Name of the gradient
    alpha : float, optional
        Alpha transparency value

    Examples
    --------
    Create a gradient from a list of colors:

    .. testcode::

        from chromo_map import Gradient
        colors = ['#ff0000', '#00ff00', '#0000ff']
        gradient = Gradient(colors, name='RGB')
        gradient

    .. html-output::

        from chromo_map import Gradient
        colors = ['#ff0000', '#00ff00', '#0000ff']
        gradient = Gradient(colors, name='RGB')
        print(gradient._repr_html_())

    """

    def __init__(self, colors, name=None, alpha=None):
        """Initialize a Gradient object."""
        if isinstance(colors, Gradient):
            self.colors = colors.colors
            self.name = colors.name
            # Handle _segmentdata attribute safely
            segmentdata = getattr(colors, '_segmentdata', {})
            super().__init__(colors.name, segmentdata, colors.N)
        elif isinstance(colors, (list, tuple)):
            self._update_from_list(colors, name, alpha)
        elif isinstance(colors, np.ndarray):
            self._update_from_list(list(colors), name, alpha)
        elif isinstance(colors, (LSC, LC)):
            color_array = colors(np.arange(colors.N))
            self._update_from_list(list(color_array), name, alpha)
        elif isinstance(colors, str):
            # Handle string colormap names
            cmap = plt.get_cmap(colors)
            color_array = cmap(np.arange(cmap.N))
            # Convert RGBA tuples to hex strings for matplotlib compatibility
            color_list = []
            for rgba in color_array:
                # Convert RGBA tuple to hex
                r, g, b, a = rgba
                hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                color_list.append(hex_color)
            self._update_from_list(color_list, name, alpha)
        else:
            # Use LSC.from_list for better type compatibility
            if name is None:
                name = "custom"
            
            # Handle dictionary input for LinearSegmentedColormap
            if isinstance(colors, dict):
                cmap = LSC(name, colors)
            else:
                cmap = LSC.from_list(name, colors)
            color_array = cmap(np.arange(cmap.N))
            self._update_from_list(list(color_array), name, alpha)

    def _update_from_list(self, colors, name=None, alpha=None):
        """Update the gradient from a list of colors."""
        if name is None:
            name = "custom"
        
        # Check for empty colors list
        if not colors:
            raise ValueError("No valid colors found.")
        
        self.colors = [Color(c) for c in colors]
        
        if alpha is not None:
            self.colors = [c.with_alpha(alpha) for c in self.colors]
        
        self.name = name
        
        # Create the matplotlib colormap
        # Convert to normalized RGBA tuples (0-1 range)
        color_list = []
        for c in self.colors:
            r, g, b, a = c.rgbatup
            color_list.append((r/255.0, g/255.0, b/255.0, a))
        super().__init__(name, LSC.from_list(name, color_list)._segmentdata, len(color_list))

    def with_alpha(self, alpha):
        """Return a new gradient with the specified alpha value.

        Parameters
        ----------
        alpha : float
            The alpha value (0-1)

        Returns
        -------
        Gradient
            A new gradient with the specified alpha value

        Examples
        --------

        Create a gradient with 50% transparency:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            transparent = gradient.with_alpha(0.5)
            transparent

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            transparent = gradient.with_alpha(0.5)
            print(transparent._repr_html_())

        """
        return Gradient([c.with_alpha(alpha) for c in self.colors], name=self.name)

    def __eq__(self, other):
        """Check if two gradients are equal based on their colors."""
        if not isinstance(other, Gradient):
            return False
        return np.isclose(self.tup, other.tup, atol=1e-2).all()

    def __repr__(self) -> str:
        """Return a rich colored representation of the gradient."""
        from rich.console import Console
        from rich.text import Text
        
        # Force terminal mode to enable colors on Windows
        console = Console(force_terminal=True)
        
        # Check if colors are supported
        if console.is_terminal and console.color_system:
            # Create colored blocks for each color in the gradient
            result = Text()
            
            # Limit display to 64 characters maximum
            max_chars = 64
            colors_to_display = self.colors
            
            # If we have more than 64 colors, resample down to 64
            if len(self.colors) > max_chars:
                # Use the resize method to get a resampled version
                resampled_gradient = self.resize(max_chars)
                colors_to_display = resampled_gradient.colors
            
            # Determine spacing based on number of colors to display
            # Use 2 spaces for <= 32 colors, 1 space for > 32 colors
            if len(colors_to_display) <= 32:
                char_per_color = "  "  # 2 spaces
            else:
                char_per_color = " "   # 1 space
            
            # Add colored blocks for each color using background colors
            for color in colors_to_display:
                colored_block = Text(char_per_color, style=f"on {color.hex}")
                result.append(colored_block)
            
            # Add gradient info
            gradient_info = Text(f" Gradient({self.name}, {len(self.colors)} colors)", style="default")
            result.append(gradient_info)
            
            # Use console to render to string
            with console.capture() as capture:
                console.print(result, end="")
            
            return capture.get()
        else:
            # Fallback to plain text representation
            return f"Gradient({self.name}, {len(self.colors)} colors)"

    def __getattr__(self, name):
        """Get attributes from underlying colors."""
        pass_through = (
            "tup",
            "hex",
            "hexa",
            "rgb",
            "rgba",
            "hextup",
            "rgbtup",
            "hexatup",
            "rgbatup",
            "r",
            "g",
            "b",
            "a",
        )
        if name in pass_through:
            return [getattr(clr, name) for clr in self.colors]
        raise AttributeError(f"'Gradient' object has no attribute '{name}'")

    def __getitem__(self, key):
        """Get colors from the gradient by index or fraction."""
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or 1
            num = key.step or len(self.colors)
            return self[np.linspace(start, stop, num)]
        if isinstance(key, int) and 0 <= key < len(self):
            return self.colors[key]
        if isinstance(key, float) and 0 <= key <= 1:
            if key == 0:
                return self.colors[0]
            if key == 1:
                return self.colors[-1]

            x, i = np.modf(key * (self.N - 1))
            i = int(i)
            j = i + 1
            c0 = self.colors[i]
            c1 = self.colors[j]
            return c0.interpolate(c1, x)
        if isinstance(key, (list, tuple, np.ndarray)):
            return Gradient([self[x] for x in key])
        raise IndexError(f"Invalid index: {key}")

    def __iter__(self):
        """Iterate over the colors in the gradient."""
        return iter(self.colors)

    def reversed(self, name=None):
        """Return a new gradient with the colors reversed.

        Parameters
        ----------
        name : str, optional
            The name of the new gradient.

        Returns
        -------
        Gradient
            The new gradient with the colors reversed.

        Examples
        --------

        Create a reversed gradient:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='rGb')
            gradient.reversed()

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='rGb')
            print(gradient.reversed()._repr_html_())

        """
        if name is None:
            name = f"{self.name}_r"
        return Gradient(super().reversed(name=name))

    @property
    def _r(self):
        """Return a reversed gradient."""
        return self.reversed()

    def __len__(self):
        """Return the number of colors in the gradient."""
        return len(self.colors)

    def resize(self, num):
        """Resize the gradient to a new number of colors.

        Parameters
        ----------
        num : int
            The new number of colors.

        Returns
        -------
        Gradient
            The new gradient with the new number of colors.

        Examples
        --------

        Resize the gradient to 32 colors:

        .. testcode::

                from chromo_map import Gradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = Gradient(colors, name='rGb')
                gradient.resize(32)

        .. html-output::

                from chromo_map import Gradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = Gradient(colors, name='rGb')
                print(gradient.resize(32)._repr_html_())

        """
        return Gradient(self.resampled(num), name=self.name)

    def to_div(self, maxn=None, as_png=False):
        """Convert the gradient to an HTML div.

        Parameters
        ----------
        maxn : int, optional
            The maximum number of colors to display.

        as_png : bool, optional
            Whether to display the gradient as a PNG image.

        Returns
        -------
        HTML
            The gradient as an HTML div.

        Examples
        --------

        Convert the gradient to an HTML div:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='rGb')
            gradient.to_div(as_png=False)

        .. html-output::

                from chromo_map import Gradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = Gradient(colors, name='rGb')
                print(gradient.to_div(as_png=False).data)

        """
        max_flex_width = 500 / 16
        n = len(self.colors)
        if n == 0:
            return ""

        if maxn is not None and n > maxn:
            cmap = self.resize(maxn)
        else:
            cmap = self

        template = Template(
            dedent(
                """\
        <div class="gradient">
            <style>
                #_{{ random_id }} {
                    display: flex; gap: 0rem; width: {{ max_width }}rem;
                }
                #_{{ random_id }} div { flex: 1 1 0; }
                #_{{ random_id }} div.color { width: 100%; height: 100%; }
                #_{{ random_id }} div.cmap { width: 100%; height: auto; }
                #_{{ random_id }} div.cmap > img { width: 100%; height: 100%; }
            </style>
            <strong>{{ name }}</strong>
            {% if as_png %}
            {{ colors.to_png().data }}
            {% else %}
            <div id="_{{ random_id }}" class="color-map">
                {% for clr in colors.colors %}
                    {{ clr._repr_html_() }}
                {% endfor %}
            </div>
            {% endif %}
        </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return HTML(
            template.render(
                name=cmap.name,
                colors=cmap,
                random_id=random_id,
                max_width=max_flex_width,
                as_png=as_png,
            )
        )

    def to_matplotlib(self):
        """Convert the gradient to a matplotlib figure."""
        gradient = np.linspace(0, 1, self.N)
        gradient = np.vstack((gradient, gradient))

        _, ax = plt.subplots(figsize=(5, 0.5))
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax.set_position((0, 0, 1, 1))
        ax.margins(0)
        ax.imshow(gradient, aspect="auto", cmap=self)
        ax.set_title(self.name)
        ax.axis("off")
        plt.show()

    def to_drawing(self, width=500, height=50, filename=None):
        """Convert the gradient to an SVG drawing."""
        dwg = svgwrite.Drawing(filename, profile="tiny", size=(width, height))
        rect_width = width / self.N

        left = 0
        for i, color in enumerate(self, 1):
            right = int(i * rect_width)
            actual_width = right - left + 1
            dwg.add(
                dwg.rect(
                    insert=(left, 0),
                    size=(actual_width, height),
                    fill=color.hex,
                    fill_opacity=color.a,
                )
            )
            left = right

        return dwg

    def to_png(self):
        """Convert the gradient to a PNG image."""
        png_bytes = self._repr_png_()
        png_base64 = base64.b64encode(png_bytes).decode("ascii")
        div = f'<div class="cmap"><img src="data:image/png;base64,{png_base64}"></div>'
        return HTML(div)

    def _repr_html_(self, skip_super=False):
        """Return HTML representation of the gradient."""
        if hasattr(super(), "_repr_html_") and not skip_super:
            return BeautifulSoup(super()._repr_html_(), "html.parser").prettify()
        return self.to_div().data

    def __add__(self, other):
        """Add two gradients together."""
        name = f"{self.name} + {other.name}"
        return Gradient(self.colors + other.colors, name=name)

    def __mul__(self, other):
        """Multiply gradient by an integer."""
        if isinstance(other, int):
            return Gradient(self.colors * other, name=self.name)
        raise ValueError("Invalid multiplication.")

    def __rmul__(self, other):
        """Reverse multiplication."""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Divide gradient by a number."""
        if isinstance(other, (int, float)):
            step = int(other * len(self))
            return Gradient(self[::step], name=self.name)
        raise ValueError("Invalid division.")

    def __or__(self, other):
        """Blend two gradients together."""
        n = lcm(len(self), len(other))
        a = self.resize(n)
        b = other.resize(n)
        name = f"{self.name} | {other.name}"
        return Gradient([x | y for x, y in zip(a, b)], name=name)

    def rename(self, new_name: str):
        """Rename the gradient.

        Parameters
        ----------
        new_name : str
            The new name for the gradient.

        Returns
        -------
        Gradient
            The gradient with the new name.

        Examples
        --------

        Rename the gradient:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='rGb')
            gradient.rename('New Gradient')

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='rGb')
            print(gradient.rename('New Gradient')._repr_html_())

        """
        return Gradient(self.colors, name=new_name)

    def adjust_hue(self, degrees: float) -> 'Gradient':
        """Adjust the hue of all colors in the gradient.

        Parameters
        ----------
        degrees : float
            The number of degrees to adjust the hue by.

        Returns
        -------
        Gradient
            A new gradient with adjusted hue.

        Examples
        --------

        Adjust hue by 60 degrees:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            shifted = gradient.adjust_hue(60)
            shifted

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            shifted = gradient.adjust_hue(60)
            print(shifted._repr_html_())

        """
        new_colors = [color.adjust_hue(degrees) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_hue{degrees:+.0f}")

    def adjust_saturation(self, factor: float) -> 'Gradient':
        """Adjust the saturation of all colors in the gradient.

        Parameters
        ----------
        factor : float
            The factor to multiply saturation by.

        Returns
        -------
        Gradient
            A new gradient with adjusted saturation.

        Examples
        --------

        Decrease saturation by 50%:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            desaturated = gradient.adjust_saturation(0.5)
            desaturated

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            desaturated = gradient.adjust_saturation(0.5)
            print(desaturated._repr_html_())

        """
        new_colors = [color.adjust_saturation(factor) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_sat{factor:.1f}")

    def adjust_brightness(self, factor: float) -> 'Gradient':
        """Adjust the brightness of all colors in the gradient.

        Parameters
        ----------
        factor : float
            The factor to multiply brightness by.

        Returns
        -------
        Gradient
            A new gradient with adjusted brightness.

        Examples
        --------

        Increase brightness by 20%:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            bright = gradient.adjust_brightness(1.2)
            bright

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            bright = gradient.adjust_brightness(1.2)
            print(bright._repr_html_())

        """
        new_colors = [color.adjust_brightness(factor) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_bright{factor:.1f}")

    def adjust_lightness(self, factor: float) -> 'Gradient':
        """Adjust the lightness of all colors in the gradient.

        Parameters
        ----------
        factor : float
            The factor to multiply lightness by.

        Returns
        -------
        Gradient
            A new gradient with adjusted lightness.

        Examples
        --------

        Decrease lightness by 30%:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            dark = gradient.adjust_lightness(0.7)
            dark

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            dark = gradient.adjust_lightness(0.7)
            print(dark._repr_html_())

        """
        new_colors = [color.adjust_lightness(factor) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_light{factor:.1f}")

    def make_accessible(self, background_color: Union[Color, str], level: str = 'AA') -> 'Gradient':
        """Make all colors in the gradient accessible against a background color.

        Parameters
        ----------
        background_color : Color or str
            The background color to ensure accessibility against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').

        Returns
        -------
        Gradient
            A new gradient with accessible colors.

        Examples
        --------

        Make gradient accessible against white background:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ffcccc', '#ccffcc', '#ccccff']
            gradient = Gradient(colors, name='Pastels')
            accessible = gradient.make_accessible('white')
            accessible

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ffcccc', '#ccffcc', '#ccccff']
            gradient = Gradient(colors, name='Pastels')
            accessible = gradient.make_accessible('white')
            print(accessible._repr_html_())

        """
        from chromo_map.core.color import find_accessible_color
        background = Color(background_color) if not isinstance(background_color, Color) else background_color
        new_colors = [find_accessible_color(color, background, level) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_accessible")

    def complementary(self) -> 'Gradient':
        """Get the complementary gradient (all colors shifted 180 degrees).

        Returns
        -------
        Gradient
            A new gradient with complementary colors.

        Examples
        --------

        Get complementary gradient:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            complement = gradient.complementary()
            complement

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = Gradient(colors, name='RGB')
            complement = gradient.complementary()
            print(complement._repr_html_())

        """
        new_colors = [color.complementary() for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_complementary")

    def analyze_contrast(self, background_color: Union[Color, str]) -> Dict[str, Any]:
        """Analyze contrast ratios of all colors against a background.

        Parameters
        ----------
        background_color : Color or str
            The background color to analyze against.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing contrast analysis results.

        Examples
        --------

        Analyze contrast against white background:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#000000', '#808080', '#ffffff']
            gradient = Gradient(colors, name='Grayscale')
            analysis = gradient.analyze_contrast('white')
            print(f"Average contrast: {analysis['average_contrast']:.2f}")

        .. testoutput::

            Average contrast: 8.65

        """
        background = Color(background_color) if not isinstance(background_color, Color) else background_color
        contrasts = [color.contrast_ratio(background) for color in self.colors]
        accessible_aa = sum(1 for c in contrasts if c >= 4.5)
        accessible_aaa = sum(1 for c in contrasts if c >= 7.0)
        
        return {
            'average_contrast': sum(contrasts) / len(contrasts) if contrasts else 0,
            'min_contrast': min(contrasts) if contrasts else 0,
            'max_contrast': max(contrasts) if contrasts else 0,
            'accessible_aa_count': accessible_aa,
            'accessible_aaa_count': accessible_aaa,
            'accessibility_aa_score': accessible_aa / len(contrasts) if contrasts else 0,
            'accessibility_aaa_score': accessible_aaa / len(contrasts) if contrasts else 0,
            'contrasts': contrasts
        }

    def find_accessible_version(self, background_color: Union[Color, str], level: str = 'AA') -> 'Gradient':
        """Find accessible version of all colors in the gradient.

        Parameters
        ----------
        background_color : Color or str
            The background color to ensure accessibility against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').

        Returns
        -------
        Gradient
            A new gradient with accessible colors.

        Examples
        --------

        Find accessible version of gradient:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ffcccc', '#ccffcc', '#ccccff']
            gradient = Gradient(colors, name='Pastels')
            accessible = gradient.find_accessible_version('white')
            accessible

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ffcccc', '#ccffcc', '#ccccff']
            gradient = Gradient(colors, name='Pastels')
            accessible = gradient.find_accessible_version('white')
            print(accessible._repr_html_())

        """
        return self.make_accessible(background_color, level)

    def maximize_contrast_iterative(self, background_color: Union[Color, str], level: str = 'AA',
                                   adjust_lightness: bool = True, step_size: float = 0.1,
                                   max_attempts: int = 50) -> 'Gradient':
        """Maximize contrast of all colors using iterative approach.

        Parameters
        ----------
        background_color : Color or str
            The background color to maximize contrast against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        adjust_lightness : bool, default True
            Whether to adjust lightness (True) or brightness/value (False).
        step_size : float, default 0.1
            The step size for adjustments.
        max_attempts : int, default 50
            Maximum number of adjustment attempts.

        Returns
        -------
        Gradient
            A new gradient with maximized contrast colors.

        Examples
        --------

        Maximize contrast iteratively:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_iterative('white')
            optimized

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_iterative('white')
            print(optimized._repr_html_())

        """
        from chromo_map.core.color import find_maximal_contrast_iterative
        background = Color(background_color) if not isinstance(background_color, Color) else background_color
        new_colors = [find_maximal_contrast_iterative(color, background, level, adjust_lightness, step_size, max_attempts) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_max_contrast_iterative")

    def maximize_contrast_binary_search(self, background_color: Union[Color, str], level: str = 'AA',
                                       adjust_lightness: bool = True, precision: float = 0.001) -> 'Gradient':
        """Maximize contrast of all colors using binary search.

        Parameters
        ----------
        background_color : Color or str
            The background color to maximize contrast against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        adjust_lightness : bool, default True
            Whether to adjust lightness (True) or brightness/value (False).
        precision : float, default 0.001
            The precision for binary search convergence.

        Returns
        -------
        Gradient
            A new gradient with maximized contrast colors.

        Examples
        --------

        Maximize contrast with binary search:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_binary_search('white')
            optimized

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_binary_search('white')
            print(optimized._repr_html_())

        """
        from chromo_map.core.color import find_maximal_contrast_binary_search
        background = Color(background_color) if not isinstance(background_color, Color) else background_color
        new_colors = [find_maximal_contrast_binary_search(color, background, level, adjust_lightness, precision) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_max_contrast_binary")

    def maximize_contrast_optimization(self, background_color: Union[Color, str], level: str = 'AA',
                                     method: str = 'golden_section') -> 'Gradient':
        """Maximize contrast of all colors using mathematical optimization.

        Parameters
        ----------
        background_color : Color or str
            The background color to maximize contrast against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        method : str, default 'golden_section'
            The optimization method to use ('golden_section' or 'gradient_descent').

        Returns
        -------
        Gradient
            A new gradient with maximized contrast colors.

        Examples
        --------

        Maximize contrast with optimization:

        .. testcode::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_optimization('white')
            optimized

        .. html-output::

            from chromo_map import Gradient
            colors = ['#ff6666', '#66ff66', '#6666ff']
            gradient = Gradient(colors, name='Light')
            optimized = gradient.maximize_contrast_optimization('white')
            print(optimized._repr_html_())

        """
        from chromo_map.core.color import find_maximal_contrast_optimization
        background = Color(background_color) if not isinstance(background_color, Color) else background_color
        new_colors = [find_maximal_contrast_optimization(color, background, level, method) for color in self.colors]
        return Gradient(new_colors, name=f"{self.name}_max_contrast_optimization")

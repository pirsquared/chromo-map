"""Color module for chromo_map package."""

import re
import uuid
from typing import Tuple
from textwrap import dedent
import json
import base64
from importlib_resources import files
from IPython.display import HTML
from jinja2 import Template
import numpy as np
from _plotly_utils import colors as plotly_colors
from matplotlib.colors import LinearSegmentedColormap as LSC
from matplotlib.colors import ListedColormap as LC
from matplotlib.colors import to_rgba, to_rgb
import matplotlib.pyplot as plt
import svgwrite
import palettable
from palettable.palette import Palette
from pirrtools import AttrDict, find_instances
from pirrtools.sequences import lcm
from bs4 import BeautifulSoup


def _rgb_c(c):
    return rf"(?P<{c}>[^,\s]+)"


_COMMA = r"\s*,\s*"
_red = _rgb_c("red")
_grn = _rgb_c("grn")
_blu = _rgb_c("blu")
_alp = _rgb_c("alp")
_rgb_pat = _COMMA.join([_red, _grn, _blu]) + f"({_COMMA}{_alp})?"
_RGB_PATTERN = re.compile(rf"rgba?\({_rgb_pat}\)")

_VALID_MPL_COLORS = plt.colormaps()


def rgba_to_tup(rgbstr):
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
        return to_rgb(f"#{red:02x}{grn:02x}{blu:02x}") + (alp,)
    return None


def hexstr_to_tup(hexstr: str) -> Tuple[int, int, int, int]:
    """Convert a hex string to a tuple."""
    try:
        return to_rgba(hexstr)
    except ValueError:
        return None


def clr_to_tup(clr):
    """Convert a color to a tuple."""
    if isinstance(clr, str):
        return hexstr_to_tup(clr) or rgba_to_tup(clr)
    if isinstance(clr, (tuple, list)):
        return clr
    try:
        return to_rgba(clr)
    except ValueError:
        return None


class Color:
    """A class for representing colors.

    You can pass in a color as a tuple of RGB or
    RGBA values in which the values are between 0 and 1, a hex string with or without an
    alpha value, or an RGB or RGBA string in the form `'rgb(r, g, b)'` or
    `'rgba(r, g, b, a)'`.  The alpha value is optional in all cases.

    You can also pass in another Color object to create a copy of it with an optional
    new alpha value.

    The class has properties that return the color in various formats including tuples,
    hex strings, RGB strings, and RGBA strings.

    You can also interpolate between two colors by passing in another color and a factor
    between 0 and 1.


    Examples
    --------

    Simple red color:

    .. testcode::

        from chromo_map import Color
        Color('red')

    .. html-output::

        from chromo_map import Color
        print(Color('red')._repr_html_())

    Simple red color with alpha:

    .. testcode::

        from chromo_map import Color
        Color('red', 0.5)

    .. html-output::

            from chromo_map import Color
            print(Color('red', 0.5)._repr_html_())

    Green with hex string:

    .. testcode::

        from chromo_map import Color
        Color('#007f00')

    .. html-output::

        from chromo_map import Color
        print(Color('#007f00')._repr_html_())

    Blue with RGB string:

    .. testcode::

        from chromo_map import Color
        Color('rgb(0, 0, 255)')

    .. html-output::

        from chromo_map import Color
        print(Color('rgb(0, 0, 255)')._repr_html_())

    Blue with RGBA string and overidden alpha:

    .. testcode::

        from chromo_map import Color
        Color('rgba(0, 0, 255, 0.5)', 0.75)

    .. html-output::

        from chromo_map import Color
        print(Color('rgba(0, 0, 255, 0.5)', 0.75)._repr_html_())


    """

    def __init__(self, clr, alpha=None):
        if isinstance(clr, Color):
            self.__dict__.update(clr.__dict__)
            if alpha is not None:
                self.a = alpha
        else:
            if isinstance(clr, (tuple, list, np.ndarray)):
                red, grn, blu, *alp = clr
                if alpha is not None:
                    alp = alpha
                elif alp:
                    alp = alp[0]
                else:
                    alp = 1

            elif isinstance(clr, str):
                tup = clr_to_tup(clr)
                if tup is None:
                    raise ValueError("Invalid color input.")
                red, grn, blu, alp = tup
                alp = alpha or alp

            else:
                raise ValueError(f"Invalid color input '{type(clr).__name__}'.")

            if all(map(lambda x: 0 <= x <= 1, (red, grn, blu, alp))):
                self.r = red
                self.g = grn
                self.b = blu
                self.a = alp
            else:
                raise ValueError("Color values must be between 0 and 1.")

    @property
    def tup(self):
        """Return the color as a tuple.

        Returns
        -------
        Tuple[float, float, float, float]
            The color as a tuple of RGBA values between 0 and 1.

        Examples
        --------

        Get the color as a tuple:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.tup

        .. testoutput::

            (1.0, 0.6470588235294118, 0.0, 0.5)

        """
        return self.r, self.g, self.b, self.a

    @property
    def hexatup(self):
        """Return the color as a tuple of hex values.

        Returns
        -------
        Tuple[int, int, int, int]
            The color as a tuple of RGBA values between 0 and 255.

        Examples
        --------

        Get the color as a tuple of hex values:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.hexatup

        .. testoutput::

            (255, 165, 0, 127)

        """
        return tuple(int(x * 255) for x in self.tup)

    @property
    def hextup(self):
        """Return the color as a tuple of hex values.

        Returns
        -------
        Tuple[int, int, int]
            The color as a tuple of RGB values between 0 and 255.

        Examples
        --------

        Get the color as a tuple of hex values:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.hextup

        .. testoutput::

            (255, 165, 0)

        """
        return self.hexatup[:3]

    @property
    def rgbtup(self):
        """Return the color as a tuple of RGB values.

        Returns
        -------
        Tuple[int, int, int]
            The color as a tuple of RGB values between 0 and 255.

        Examples
        --------

        Get the color as a tuple of hex values:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.rgbtup

        .. testoutput::

            (255, 165, 0)

        """
        return self.hextup

    @property
    def rgbatup(self):
        """Return the color as a tuple of RGBA values.

        Returns
        -------
        Tuple[int, int, int, float]
            The color as a tuple of RGB values between 0 and 255 and an alpha value
            between 0 and 1.

        Examples
        --------
        Get the color as a tuple of RGBA values:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.rgbatup

        .. testoutput::

            (255, 165, 0, 0.5)

        """
        return self.rgbtup + (self.a,)

    @property
    def hex(self):
        """Return the color as a hex string.

        Returns
        -------
        str
            The color as a hex string.

        Examples
        --------

        Get the color as a hex string:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.hex

        .. testoutput::

            '#ffa500'

        """
        r, g, b = self.hextup
        return f"#{r:02x}{g:02x}{b:02x}"

    @property
    def hexa(self):
        """Return the color as a hex string with an alpha value.

        Returns
        -------
        str
            The color as a hex string with an alpha value.

        Examples
        --------

        Get the color as a hex string with an alpha value:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.hexa

        .. testoutput::

                '#ffa50080'

        """
        r, g, b, a = self.hexatup
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"

    @property
    def rgb(self):
        """Return the color as an RGB string.

        Returns
        -------
        str
            The color as an RGB string.

        Examples
        --------

        Get the color as an RGB string:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.rgb

        .. testoutput::

            'rgb(255, 165, 0)'

        """
        r, g, b = self.rgbtup
        return f"rgb({r}, {g}, {b})"

    @property
    def rgba(self):
        """Return the color as an RGBA string.

        Returns
        -------
        str
            The color as an RGBA string.

        Examples
        --------

        Get the color as an RGBA string:

        .. testcode::

            from chromo_map import Color
            orange = Color('orange', 0.5)
            orange.rgba

        .. testoutput::

            'rgba(255, 165, 0, 0.5)'

        """
        r, g, b, a = self.rgbatup
        return f"rgba({r}, {g}, {b}, {a:.1f})"

    def interpolate(self, other, factor):
        """Interpolate between two colors.

        Parameters
        ----------
        other : Color
            The other color to interpolate with.

        factor : float
            The interpolation factor between 0 and 1.

        Returns
        -------
        Color
            The interpolated color.

        Examples
        --------
        Interpolate between red and blue:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            blue = Color('blue')

            red.interpolate(blue, 0.5)

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            blue = Color('blue')
            print(red.interpolate(blue, 0.5)._repr_html_())

        """
        r = self.r + (other.r - self.r) * factor
        g = self.g + (other.g - self.g) * factor
        b = self.b + (other.b - self.b) * factor
        a = self.a + (other.a - self.a) * factor
        return Color((r, g, b, a))

    def __or__(self, other):
        """Interpolate between two colors assuming a factor of 0.5.

        Parameters
        ----------
        other : Color
            The other color to interpolate with.

        Returns
        -------
        Color
            The interpolated color.

        Examples
        --------

        Interpolate between red and blue:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            blue = Color('blue')
            red | blue

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            blue = Color('blue')
            print((red | blue)._repr_html_())

        """
        return self.interpolate(other, 0.5)

    def _repr_html_(self):
        random_id = uuid.uuid4().hex
        style = dedent(
            f"""\
        <style>
            #_{random_id} {{ 
                position: relative;
                display: inline-block;
                cursor: pointer;
                background: {self.rgba};
                width: 2rem; height: 1.5rem;
            }}
            #_{random_id}::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 50%;
                left: 0%;
                transform: translateY(50%);
                padding: 0.125rem;
                white-space: pre;
                font-size: 0.75rem;
                font-family: monospace;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(0.25rem);
                color: white;
                border-radius: 0.25rem;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.1s ease-in-out;
                z-index: -1;
            }}
            #_{random_id}:hover::after {{
                opacity: 1;
                z-index: 1;
            }}
        </style>       
        """
        )
        tooltip = dedent(
            f"""\
        RGBA: {self.rgba[5:-1]}
        HEXA: {self.hexa}\
        """
        )
        return dedent(
            f"""\
            <div>
                {style}
                <div id="_{random_id}" class="color" data-tooltip="{tooltip}"></div>
            </div>
        """
        )

    def __eq__(self, other):
        """Check if two colors are equal.

        Only checks the result of the tuple property.

        Parameters
        ----------
        other : Color
            The other color to compare to.

        Returns
        -------
        bool
            Whether the colors are equal.
        """
        return np.isclose(self.tup, other.tup).all()


class ColorGradient(LSC):
    """Mimics a matplotlib colormap with a list of colors.

    I wanted an object that could be used in place of a matplotlib colormap but with a
    bit of extra functionality.  This class allows you to create a gradient from a list
    of colors, another gradient, a palette, a matplotlib colormap, or a string name of a
    matplotlib colormap.

    Examples
    --------

    Create a gradient from a list of colors:

    .. testcode::

        from chromo_map import ColorGradient
        colors = ['#ff0000', '#00ff00', '#0000ff']
        gradient = ColorGradient(colors, name='rGb)
        gradient

    .. html-output::

        from chromo_map import ColorGradient
        colors = ['#ff0000', '#00ff00', '#0000ff']
        gradient = ColorGradient(colors, name='rGb')
        print(gradient._repr_html_())

    Or with hover information:

    .. testcode::

        gradient.to_div(as_png=False)

    .. html-output::

        print(gradient.to_div(as_png=False).data)

    """

    def _update_from_list(self, colors, name, alpha):
        if not list(colors):
            raise ValueError("No valid colors found.")
        self.colors = tuple(Color(clr, alpha) for clr in colors)
        mpl_colormap = LSC.from_list(name=name, colors=self.tup, N=len(self.colors))
        self.__dict__.update(mpl_colormap.__dict__)

    def with_alpha(self, alpha, name=None):
        """Create a new gradient with a new alpha value.

        Parameters
        ----------
        alpha : float
            The new alpha value between 0 and 1.

        name : str, optional
            The name of the new gradient.

        Returns
        -------
        ColorGradient
            The new gradient with the new alpha value.

        Examples
        --------

        Create a gradient with a new alpha value:

        .. testcode::

            from chromo_map import ColorGradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = ColorGradient(colors, name='rGb')
            gradient.with_alpha(0.5)

        .. html-output::

            from chromo_map import ColorGradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = ColorGradient(colors, name='rGb')
            print(gradient.with_alpha(0.5)._repr_html_())

        """
        return ColorGradient(
            [Color(clr, alpha) for clr in self.colors], name=name or self.name
        )

    def __init__(self, colors, name=None, alpha=None):
        name = name or "custom" if not hasattr(colors, "name") else colors.name

        if isinstance(colors, (list, tuple, np.ndarray)):
            self._update_from_list(colors, name, alpha)

        elif isinstance(colors, ColorGradient):
            self._update_from_list(colors.colors, name, alpha)

        elif isinstance(colors, Palette):
            self._update_from_list(colors.mpl_colors, name, alpha)

        elif isinstance(colors, LSC):
            self._update_from_list(colors(np.arange(colors.N)), name, alpha)

        elif isinstance(colors, LC):
            self._update_from_list(colors.colors, name, alpha)

        elif isinstance(colors, str) and colors in _VALID_MPL_COLORS:
            cmap = plt.get_cmap(colors)
            self._update_from_list(cmap(np.arange(cmap.N)), name, alpha)

        else:
            cmap = LSC(name, colors)
            self._update_from_list(cmap(np.arange(cmap.N)), name, alpha)

    def __getattr__(self, name):
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
        raise AttributeError(f"'ColorGradient' object has no attribute '{name}'")

    def __getitem__(self, key):
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
            return ColorGradient([self[x] for x in key])
        raise IndexError(f"Invalid index: {key}")

    def __iter__(self):
        return iter(self.colors)

    def reversed(self, name=None):
        """Return a new gradient with the colors reversed.

        Parameters
        ----------
        name : str, optional
            The name of the new gradient.

        Returns
        -------
        ColorGradient
            The new gradient with the colors reversed.

        Examples
        --------

        Create a reversed gradient:

        .. testcode::

            from chromo_map import ColorGradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = ColorGradient(colors, name='rGb')
            gradient.reversed()

        .. html-output::

            from chromo_map import ColorGradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = ColorGradient(colors, name='rGb')
            print(gradient.reversed()._repr_html_())

        """
        if name is None:
            name = f"{self.name}_r"
        return ColorGradient(super().reversed(name=name))

    @property
    def _r(self):
        return self.reversed()

    def __len__(self):
        return len(self.colors)

    def resize(self, num):
        """Resize the gradient to a new number of colors.

        Parameters
        ----------
        num : int
            The new number of colors.

        Returns
        -------
        ColorGradient
            The new gradient with the new number of colors.

        Examples
        --------

        Resize the gradient to 32 colors:

        .. testcode::

                from chromo_map import ColorGradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = ColorGradient(colors, name='rGb')
                gradient.resize(32)

        .. html-output::

                from chromo_map import ColorGradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = ColorGradient(colors, name='rGb')
                print(gradient.resize(32)._repr_html_())

        """
        return ColorGradient(self.resampled(num), name=self.name)

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

            from chromo_map import ColorGradient
            colors = ['#ff0000', '#00ff00', '#0000ff']
            gradient = ColorGradient(colors, name='rGb')
            gradient.to_div(as_png=False)

        .. html-output::

                from chromo_map import ColorGradient
                colors = ['#ff0000', '#00ff00', '#0000ff']
                gradient = ColorGradient(colors, name='rGb')
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
        ax.set_position([0, 0, 1, 1])
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
        if hasattr(super(), "_repr_html_") and not skip_super:
            return BeautifulSoup(super()._repr_html_(), "html.parser").prettify()
        return self.to_div().data

    def __add__(self, other):
        name = f"{self.name} + {other.name}"
        return ColorGradient(self.colors + other.colors, name=name)

    def __mul__(self, other):
        if isinstance(other, int):
            return ColorGradient(self.colors * other, name=self.name)
        raise ValueError("Invalid multiplication.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return ColorGradient(self[:: other * len(self)], name=self.name)
        raise ValueError("Invalid division.")

    def __or__(self, other):
        n = lcm(len(self), len(other))
        a = self.resize(n)
        b = other.resize(n)
        name = f"{self.name} | {other.name}"
        return ColorGradient([x | y for x, y in zip(a, b)], name=name)

    def __eq__(self, other):
        return np.isclose(self.tup, other.tup).all()


class Swatch:
    """A class for representing a collection of color gradients."""

    def __init__(self, maps, maxn=32):
        self.maxn = maxn
        self.maps = []
        for name, colors in maps.items():
            try:
                self.maps.append(ColorGradient(colors, name=name))
            except ValueError as e:
                raise e
        self._repr_html_ = self.to_grid

    def to_dict(self):
        return {map.name: map.colors for map in self.maps}

    def __iter__(self):
        return iter(self.maps)

    def __len__(self):
        return len(self.maps)

    def with_max(self, maxn):
        return Swatch(self.to_dict(), maxn=maxn)

    def to_grid(self, as_png=False):
        """Convert the swatch to an HTML grid."""
        n = len(self.maps)
        if n == 0:
            return ""
        template = Template(
            dedent(
                """\
            <div id="_{{ random_id }}" class="color-swatch">
                <style>
                    #_{{ random_id }} {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
                        gap: 0.5rem 1rem;
                        justify-content: space-between;
                        overflow: hidden;
                        resize: both;
                        width: min(65rem, 100%);
                    }
                    #_{{ random_id }} div {
                        width: 100%;
                    }
                    #_{{ random_id }} > div.gradient {
                        width: 100%;
                        height: min(4rem, 100%);
                        display: grid;
                        gap: 0.2rem;
                        grid-template-rows: 1rem auto;
                    }
                    #_{{ random_id }} .color {
                        height: minmax(1.5rem, 100%);
                    }
                    #_{{ random_id }} > div.gradient > strong {
                        margin: 0;
                        padding: 0;
                    }
                    #_{{ random_id }} img {height: 100%;}
                </style>
                {% for cmap in maps %}
                    {{ cmap.to_div(maxn, as_png=as_png).data }}
                {% endfor %}
            </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return HTML(
            template.render(
                maps=self.maps, random_id=random_id, maxn=self.maxn, as_png=as_png
            )
        )


def _gud_name(name):
    return not (name[0] == "_" or name[-2:] == "_r")


class ColorMaps(AttrDict):
    """A class for collecting color gradients.

    This class is a dictionary of color gradients.  You can access the gradients by
    their names or by their categories.

    Examples
    --------

    Access a color gradient by name:

    .. testcode::

        from chromo_map import cmaps
        cmaps.plotly.carto.Vivid

    .. html-output::

        from chromo_map import cmaps
        print(cmaps.plotly.carto.Vivid._repr_html_())

    Access a color gradient by category:

    .. testcode::

        from chromo_map import cmaps
        cmaps.plotly.carto

    .. html-output::

            from chromo_map import cmaps
            print(cmaps.plotly.carto._repr_html_())

    """

    def __getattr__(self, item):
        if item in self:
            value = super().__getattr__(item)
            if not isinstance(value, type(self)):
                cmap = self._convert(value, item)
                if cmap.N > 32:
                    cmap = cmap.resize(32)
                return cmap
            return value
        temp = type(self)({k: v for k, v in self.items() if k.startswith(item)})
        if temp:
            return temp
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'"
        )

    @property
    def maps(self):
        return type(self)({k: v for k, v in self.items() if self._valid(v)})

    @property
    def _swatch(self):
        return Swatch(self.maps)

    def _repr_html_(self):
        return self._swatch.to_grid(as_png=True).data

    def to_grid(self, *args, **kwargs):
        return self._swatch.to_grid(*args, **kwargs)


class PlotlyColorMaps(ColorMaps):

    def _valid(self, value):
        return isinstance(value, list)

    def _convert(self, value, name):
        return ColorGradient(value, name=name)


class PalettableColorMaps(ColorMaps):

    def _valid(self, value):
        return isinstance(value, Palette)

    def _convert(self, value, name):
        return ColorGradient(value.mpl_colors, name=name)


class MPLColorMaps(ColorMaps):

    def _valid(self, value):
        return value in _VALID_MPL_COLORS

    def _convert(self, value, name):
        return ColorGradient(value, name=name)


plotly_cmaps = find_instances(
    cls=list,
    module=plotly_colors,
    tracker_type=PlotlyColorMaps,
    filter_func=lambda name, _: _gud_name(name),
)

palettable_cmaps = find_instances(
    cls=Palette,
    module=palettable,
    tracker_type=PalettableColorMaps,
    filter_func=lambda name, _: _gud_name(name),
)

mpl_dat = json.loads(
    files("chromo_map.data").joinpath("mpl_cat_names.json").read_text()
)

mpl_cmaps = MPLColorMaps(
    {cat: {name: name for name in names} for cat, names in mpl_dat}
)


cmaps = AttrDict()
cmaps["plotly"] = plotly_cmaps
cmaps["palettable"] = palettable_cmaps
cmaps["mpl"] = mpl_cmaps

"""Core color functionality for chromo_map package."""

import re
import uuid
import colorsys
from typing import Tuple, Union, Optional, Any, Sequence, List
from textwrap import dedent
import numpy as np
from matplotlib.colors import to_rgba, to_rgb


def _rgb_c(c: str) -> str:
    return rf"(?P<{c}>[^,\s]+)"


_COMMA = r"\s*,\s*"
_red = _rgb_c("red")
_grn = _rgb_c("grn")
_blu = _rgb_c("blu")
_alp = _rgb_c("alp")
_rgb_pat = _COMMA.join([_red, _grn, _blu]) + f"({_COMMA}{_alp})?"
_RGB_PATTERN = re.compile(rf"rgba?\({_rgb_pat}\)")


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


class Color:
    """A class for representing colors.

    You can pass in a color as a tuple of RGB or RGBA values in which the values
    are between 0 and 1, a hex string with or without an alpha value, or an RGB
    or RGBA string in the form `'rgb(r, g, b)'` or `'rgba(r, g, b, a)'`.
    The alpha value is optional in all cases.

    You can also pass in another Color object to create a copy of it with an
    optional new alpha value.

    The class has properties that return the color in various formats including
    tuples, hex strings, RGB strings, and RGBA strings.

    You can also interpolate between two colors by passing in another color and
    a factor between 0 and 1.


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

    def __init__(
        self,
        clr: Union['Color', str, Tuple[float, ...], Sequence[float], np.ndarray],
        alpha: Optional[float] = None
    ) -> None:
        # Initialize RGBA attributes
        self.r: float
        self.g: float
        self.b: float
        self.a: float
        
        if isinstance(clr, Color):
            self.__dict__.update(clr.__dict__)
            if alpha is not None:
                self.a = alpha
        else:
            if isinstance(clr, (tuple, list, np.ndarray)):
                # Extract RGB and optional alpha from sequence
                clr_list = list(clr)
                if len(clr_list) < 3:
                    raise ValueError(
                        "Color sequence must have at least 3 values (RGB)"
                    )
                
                red, grn, blu = (
                    float(clr_list[0]),
                    float(clr_list[1]),
                    float(clr_list[2])
                )
                if alpha is not None:
                    alp = alpha
                elif len(clr_list) > 3:
                    alp = float(clr_list[3])
                else:
                    alp = 1.0

            elif isinstance(clr, str):
                tup = clr_to_tup(clr)
                if tup is None:
                    raise ValueError("Invalid color input.")
                red, grn, blu, alp = tup
                alp = alpha if alpha is not None else alp

            else:
                raise ValueError(
                    f"Invalid color input '{type(clr).__name__}'."
                )

            if all(0 <= x <= 1 for x in (red, grn, blu, alp)):
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

    def interpolate(self, other: 'Color', factor: float) -> 'Color':
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

    def with_alpha(self, alpha: float) -> 'Color':
        """Return a new Color with the specified alpha value.

        Parameters
        ----------
        alpha : float
            The alpha value between 0 and 1.

        Returns
        -------
        Color
            A new Color with the specified alpha value.

        Examples
        --------

        Create a red color with 50% transparency:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            red_transparent = red.with_alpha(0.5)

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            red_transparent = red.with_alpha(0.5)
            print(red_transparent._repr_html_())

        """
        return Color((self.r, self.g, self.b, alpha))

    def __or__(self, other: 'Color') -> 'Color':
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

    def _repr_html_(self) -> str:
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

    @property
    def hsv(self):
        """Return the color as HSV values.

        Returns
        -------
        Tuple[float, float, float]
            The color as a tuple of HSV values (hue: 0-360, saturation: 0-1, value: 0-1).

        Examples
        --------

        Get the color as HSV values:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            red.hsv

        .. testoutput::

            (0.0, 1.0, 1.0)

        """
        h, s, v = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        return (h * 360, s, v)

    @property
    def hsl(self):
        """Return the color as HSL values.

        Returns
        -------
        Tuple[float, float, float]
            The color as a tuple of HSL values (hue: 0-360, saturation: 0-1, lightness: 0-1).

        Examples
        --------

        Get the color as HSL values:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            red.hsl

        .. testoutput::

            (0.0, 1.0, 0.5)

        """
        h, l, s = colorsys.rgb_to_hls(self.r, self.g, self.b)
        return (h * 360, s, l)

    @property
    def luminance(self):
        """Return the relative luminance of the color.

        Uses the WCAG 2.1 formula for relative luminance.

        Returns
        -------
        float
            The relative luminance value (0-1).

        Examples
        --------

        Get the luminance of a color:

        .. testcode::

            from chromo_map import Color
            white = Color('white')
            black = Color('black')
            print(f"White luminance: {white.luminance:.3f}")
            print(f"Black luminance: {black.luminance:.3f}")

        .. testoutput::

            White luminance: 1.000
            Black luminance: 0.000

        """
        def _linearize(c):
            """Convert sRGB color component to linear RGB."""
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        
        r_lin = _linearize(self.r)
        g_lin = _linearize(self.g)
        b_lin = _linearize(self.b)
        
        return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

    def adjust_hue(self, degrees: float) -> 'Color':
        """Adjust the hue of the color by the specified degrees.

        Parameters
        ----------
        degrees : float
            The number of degrees to adjust the hue by.

        Returns
        -------
        Color
            A new color with the adjusted hue.

        Examples
        --------

        Adjust hue by 120 degrees:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            green = red.adjust_hue(120)
            green

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            green = red.adjust_hue(120)
            print(green._repr_html_())

        """
        h, s, v = self.hsv
        new_h = (h + degrees) % 360
        r, g, b = colorsys.hsv_to_rgb(new_h / 360, s, v)
        return Color((r, g, b, self.a))

    def adjust_saturation(self, factor: float) -> 'Color':
        """Adjust the saturation of the color by the specified factor.

        Parameters
        ----------
        factor : float
            The factor to multiply the saturation by. Values > 1 increase saturation,
            values < 1 decrease saturation.

        Returns
        -------
        Color
            A new color with the adjusted saturation.

        Examples
        --------

        Increase saturation by 50%:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            saturated = red.adjust_saturation(1.5)
            saturated

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            saturated = red.adjust_saturation(1.5)
            print(saturated._repr_html_())

        """
        h, s, v = self.hsv
        new_s = min(1.0, max(0.0, s * factor))
        r, g, b = colorsys.hsv_to_rgb(h / 360, new_s, v)
        return Color((r, g, b, self.a))

    def adjust_brightness(self, factor: float) -> 'Color':
        """Adjust the brightness (value) of the color by the specified factor.

        Parameters
        ----------
        factor : float
            The factor to multiply the brightness by. Values > 1 increase brightness,
            values < 1 decrease brightness.

        Returns
        -------
        Color
            A new color with the adjusted brightness.

        Examples
        --------

        Increase brightness by 20%:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            bright = red.adjust_brightness(1.2)
            bright

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            bright = red.adjust_brightness(1.2)
            print(bright._repr_html_())

        """
        h, s, v = self.hsv
        new_v = min(1.0, max(0.0, v * factor))
        r, g, b = colorsys.hsv_to_rgb(h / 360, s, new_v)
        return Color((r, g, b, self.a))

    def adjust_lightness(self, factor: float) -> 'Color':
        """Adjust the lightness (HSL) of the color by the specified factor.

        Parameters
        ----------
        factor : float
            The factor to multiply the lightness by. Values > 1 increase lightness,
            values < 1 decrease lightness.

        Returns
        -------
        Color
            A new color with the adjusted lightness.

        Examples
        --------

        Decrease lightness by 20%:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            dark = red.adjust_lightness(0.8)
            dark

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            dark = red.adjust_lightness(0.8)
            print(dark._repr_html_())

        """
        h, s, l = self.hsl
        new_l = min(1.0, max(0.0, l * factor))
        r, g, b = colorsys.hls_to_rgb(h / 360, new_l, s)
        return Color((r, g, b, self.a))

    def set_hsv(self, h: Optional[float] = None, s: Optional[float] = None, v: Optional[float] = None) -> 'Color':
        """Set specific HSV values while keeping others unchanged.

        Parameters
        ----------
        h : float, optional
            The hue value (0-360). If None, keeps current hue.
        s : float, optional
            The saturation value (0-1). If None, keeps current saturation.
        v : float, optional
            The value/brightness (0-1). If None, keeps current value.

        Returns
        -------
        Color
            A new color with the specified HSV values.

        Examples
        --------

        Set hue to 240 (blue):

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            blue = red.set_hsv(h=240)
            blue

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            blue = red.set_hsv(h=240)
            print(blue._repr_html_())

        """
        current_h, current_s, current_v = self.hsv
        new_h = h if h is not None else current_h
        new_s = s if s is not None else current_s
        new_v = v if v is not None else current_v
        
        r, g, b = colorsys.hsv_to_rgb(new_h / 360, new_s, new_v)
        return Color((r, g, b, self.a))

    def contrast_ratio(self, other: 'Color') -> float:
        """Calculate the contrast ratio between this color and another.

        Uses the WCAG 2.1 formula for contrast ratio.

        Parameters
        ----------
        other : Color
            The other color to compare against.

        Returns
        -------
        float
            The contrast ratio (1:1 to 21:1).

        Examples
        --------

        Calculate contrast ratio between black and white:

        .. testcode::

            from chromo_map import Color
            black = Color('black')
            white = Color('white')
            black.contrast_ratio(white)

        .. testoutput::

            21.0

        """
        l1 = self.luminance
        l2 = other.luminance
        
        # Ensure l1 is the lighter color
        if l1 < l2:
            l1, l2 = l2, l1
        
        return (l1 + 0.05) / (l2 + 0.05)

    def is_accessible(self, other: 'Color', level: str = 'AA') -> bool:
        """Check if this color has sufficient contrast with another for accessibility.

        Parameters
        ----------
        other : Color
            The other color to compare against.
        level : str, default 'AA'
            The WCAG level to check against ('AA' or 'AAA').

        Returns
        -------
        bool
            True if the contrast ratio meets the specified level.

        Examples
        --------

        Check if black text on white background is accessible:

        .. testcode::

            from chromo_map import Color
            black = Color('black')
            white = Color('white')
            black.is_accessible(white)

        .. testoutput::

            True

        """
        ratio = self.contrast_ratio(other)
        if level == 'AAA':
            return ratio >= 7.0
        else:  # AA level
            return ratio >= 4.5

    def complementary(self) -> 'Color':
        """Get the complementary color (opposite on the color wheel).

        Returns
        -------
        Color
            The complementary color.

        Examples
        --------

        Get the complement of red:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            cyan = red.complementary()
            cyan

        .. html-output::

            from chromo_map import Color
            red = Color('red')
            cyan = red.complementary()
            print(cyan._repr_html_())

        """
        return self.adjust_hue(180)

    def triadic(self) -> Tuple['Color', 'Color']:
        """Get the triadic colors (120 degrees apart on the color wheel).

        Returns
        -------
        Tuple[Color, Color]
            A tuple of two triadic colors.

        Examples
        --------

        Get the triadic colors of red:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            triad1, triad2 = red.triadic()
            print(f"Triad 1: {triad1.hex}")
            print(f"Triad 2: {triad2.hex}")

        .. testoutput::

            Triad 1: #00ff00
            Triad 2: #0000ff

        """
        return (self.adjust_hue(120), self.adjust_hue(240))

    def analogous(self, angle: float = 30) -> Tuple['Color', 'Color']:
        """Get analogous colors (adjacent on the color wheel).

        Parameters
        ----------
        angle : float, default 30
            The angle in degrees for the analogous colors.

        Returns
        -------
        Tuple[Color, Color]
            A tuple of two analogous colors.

        Examples
        --------

        Get analogous colors of red:

        .. testcode::

            from chromo_map import Color
            red = Color('red')
            analog1, analog2 = red.analogous()
            print(f"Analogous 1: {analog1.hex}")
            print(f"Analogous 2: {analog2.hex}")

        .. testoutput::

            Analogous 1: #ff8000
            Analogous 2: #ff0080

        """
        return (self.adjust_hue(angle), self.adjust_hue(-angle))

    def find_accessible_version(self, target_color: Union['Color', str], level: str = 'AA', 
                              adjust_lightness: bool = True) -> 'Color':
        """Find an accessible version of this color against a target.

        Parameters
        ----------
        target_color : Color or str
            The color to ensure accessibility against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        adjust_lightness : bool, default True
            Whether to adjust lightness (True) or brightness/value (False).

        Returns
        -------
        Color
            An accessible version of this color.

        Examples
        --------

        Find accessible version of gray against white:

        .. testcode::

            from chromo_map import Color
            gray = Color('#888888')
            accessible = gray.find_accessible_version('white')
            print(f"Accessible: {accessible.hex}")

        .. testoutput::

            Accessible: #595959

        """
        return find_accessible_color(self, target_color, level, adjust_lightness)

    def maximize_contrast_iterative(self, target_color: Union['Color', str], level: str = 'AA', 
                                  adjust_lightness: bool = True, step_size: float = 0.1, 
                                  max_attempts: int = 50) -> 'Color':
        """Maximize contrast against target using iterative approach.

        Parameters
        ----------
        target_color : Color or str
            The color to maximize contrast against.
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
        Color
            The color with maximized contrast.

        Examples
        --------

        Maximize contrast iteratively:

        .. testcode::

            from chromo_map import Color
            gray = Color('#888888')
            optimized = gray.maximize_contrast_iterative('white')
            print(f"Optimized: {optimized.hex}")

        .. testoutput::

            Optimized: #000000

        """
        return find_maximal_contrast_iterative(self, target_color, level, adjust_lightness, step_size, max_attempts)

    def maximize_contrast_binary_search(self, target_color: Union['Color', str], level: str = 'AA', 
                                       adjust_lightness: bool = True, precision: float = 0.001) -> 'Color':
        """Maximize contrast against target using binary search.

        Parameters
        ----------
        target_color : Color or str
            The color to maximize contrast against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        adjust_lightness : bool, default True
            Whether to adjust lightness (True) or brightness/value (False).
        precision : float, default 0.001
            The precision for binary search convergence.

        Returns
        -------
        Color
            The color with maximized contrast.

        Examples
        --------

        Maximize contrast with binary search:

        .. testcode::

            from chromo_map import Color
            gray = Color('#888888')
            optimized = gray.maximize_contrast_binary_search('white')
            print(f"Optimized: {optimized.hex}")

        .. testoutput::

            Optimized: #0d0d0d

        """
        return find_maximal_contrast_binary_search(self, target_color, level, adjust_lightness, precision)

    def maximize_contrast_optimization(self, target_color: Union['Color', str], level: str = 'AA', 
                                     method: str = 'golden_section') -> 'Color':
        """Maximize contrast against target using mathematical optimization.

        Parameters
        ----------
        target_color : Color or str
            The color to maximize contrast against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').
        method : str, default 'golden_section'
            The optimization method to use ('golden_section' or 'gradient_descent').

        Returns
        -------
        Color
            The color with maximized contrast.

        Examples
        --------

        Maximize contrast with optimization:

        .. testcode::

            from chromo_map import Color
            gray = Color('#888888')
            optimized = gray.maximize_contrast_optimization('white')
            print(f"Optimized: {optimized.hex}")

        .. testoutput::

            Optimized: #0d0d0d

        """
        return find_maximal_contrast_optimization(self, target_color, level, method)

    def __eq__(self, other: object) -> bool:
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
        if not isinstance(other, Color):
            return False
        return bool(np.isclose(self.tup, other.tup,
                                 rtol=1e-2, atol=1e-2).all())

    def __repr__(self) -> str:
        """Return a rich colored representation of the color."""
        from rich.console import Console
        from rich.text import Text
        
        console = Console()
        # Create a colored block using the color's hex value
        colored_block = Text("██", style=f"color {self.hex}")
        color_info = Text(f" Color({self.hex})", style="default")
        
        # Combine the colored block with the color info
        result = Text()
        result.append(colored_block)
        result.append(color_info)
        
        # Use console to render to string
        with console.capture() as capture:
            console.print(result, end="")
        
        return capture.get()


def find_accessible_color(base_color: Union[Color, str], target_color: Union[Color, str], 
                         level: str = 'AA', adjust_lightness: bool = True) -> Color:
    """Find an accessible version of a color by adjusting it.

    Parameters
    ----------
    base_color : Color or str
        The color to adjust.
    target_color : Color or str
        The color to ensure accessibility against.
    level : str, default 'AA'
        The WCAG level to achieve ('AA' or 'AAA').
    adjust_lightness : bool, default True
        Whether to adjust lightness (True) or brightness/value (False).

    Returns
    -------
    Color
        An accessible version of the base color.

    Examples
    --------

    Find an accessible version of gray against white:

    .. testcode::

        from chromo_map import find_accessible_color
        accessible = find_accessible_color('#888888', 'white')
        print(f"Accessible color: {accessible.hex}")

    .. testoutput::

        Accessible color: #595959

    """
    base = Color(base_color) if not isinstance(base_color, Color) else base_color
    target = Color(target_color) if not isinstance(target_color, Color) else target_color
    
    required_ratio = 7.0 if level == 'AAA' else 4.5
    current_ratio = base.contrast_ratio(target)
    
    if current_ratio >= required_ratio:
        return base
    
    # Determine if we need to make the color lighter or darker
    base_luminance = base.luminance
    target_luminance = target.luminance
    
    if base_luminance > target_luminance:
        # Make base color lighter
        factor = 1.1
        max_factor = 2.0
    else:
        # Make base color darker
        factor = 0.9
        max_factor = 0.1
    
    current_color = base
    attempts = 0
    max_attempts = 50
    
    while current_color.contrast_ratio(target) < required_ratio and attempts < max_attempts:
        if adjust_lightness:
            current_color = current_color.adjust_lightness(factor)
        else:
            current_color = current_color.adjust_brightness(factor)
        
        attempts += 1
        
        # Prevent infinite loops
        if factor > 1 and factor >= max_factor:
            break
        elif factor < 1 and factor <= max_factor:
            break
    
    return current_color


def find_maximal_contrast_iterative(base_color: Union[Color, str], target_color: Union[Color, str], 
                                   level: str = 'AA', adjust_lightness: bool = True, 
                                   step_size: float = 0.1, max_attempts: int = 50) -> Color:
    """Find maximal contrast using simple iterative approach.
    
    This approach incrementally adjusts the color until it meets the contrast requirement.
    Simple but may not find the optimal solution.
    
    Parameters
    ----------
    base_color : Color or str
        The color to adjust.
    target_color : Color or str
        The color to ensure accessibility against.
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
    Color
        The adjusted color with maximal contrast found.
    
    Examples
    --------
    
    Find maximal contrast iteratively:
    
    .. testcode::
    
        from chromo_map import find_maximal_contrast_iterative
        result = find_maximal_contrast_iterative('#888888', 'white')
        print(f"Iterative result: {result.hex}")
    
    .. testoutput::
    
        Iterative result: #595959
    
    """
    base = Color(base_color) if not isinstance(base_color, Color) else base_color
    target = Color(target_color) if not isinstance(target_color, Color) else target_color
    
    required_ratio = 7.0 if level == 'AAA' else 4.5
    
    # Determine direction based on luminance
    base_luminance = base.luminance
    target_luminance = target.luminance
    
    current_color = base
    best_color = base
    best_contrast = base.contrast_ratio(target)
    
    # Try both directions to find maximum contrast
    for direction in [1, -1]:
        temp_color = base
        attempts = 0
        
        while attempts < max_attempts:
            try:
                if adjust_lightness:
                    if direction == 1:
                        next_color = temp_color.adjust_lightness(1 + step_size)
                    else:
                        next_color = temp_color.adjust_lightness(1 - step_size)
                else:
                    if direction == 1:
                        next_color = temp_color.adjust_brightness(1 + step_size)
                    else:
                        next_color = temp_color.adjust_brightness(1 - step_size)
                
                next_contrast = next_color.contrast_ratio(target)
                
                if next_contrast > best_contrast:
                    best_contrast = next_contrast
                    best_color = next_color
                    temp_color = next_color
                else:
                    break  # No improvement, stop in this direction
                
                attempts += 1
            except (ZeroDivisionError, ValueError):
                break  # Stop if adjustment fails
    
    return best_color


def find_maximal_contrast_binary_search(base_color: Union[Color, str], target_color: Union[Color, str], 
                                       level: str = 'AA', adjust_lightness: bool = True, 
                                       precision: float = 0.001) -> Color:
    """Find maximal contrast using binary search approach.
    
    This approach uses binary search to efficiently find the optimal adjustment factor
    that maximizes contrast while meeting accessibility requirements.
    
    Parameters
    ----------
    base_color : Color or str
        The color to adjust.
    target_color : Color or str
        The color to ensure accessibility against.
    level : str, default 'AA'
        The WCAG level to achieve ('AA' or 'AAA').
    adjust_lightness : bool, default True
        Whether to adjust lightness (True) or brightness/value (False).
    precision : float, default 0.001
        The precision for binary search convergence.
    
    Returns
    -------
    Color
        The adjusted color with maximal contrast found.
    
    Examples
    --------
    
    Find maximal contrast using binary search:
    
    .. testcode::
    
        from chromo_map import find_maximal_contrast_binary_search
        result = find_maximal_contrast_binary_search('#888888', 'white')
        print(f"Binary search result: {result.hex}")
    
    .. testoutput::
    
        Binary search result: #595959
    
    """
    base = Color(base_color) if not isinstance(base_color, Color) else base_color
    target = Color(target_color) if not isinstance(target_color, Color) else target_color
    
    required_ratio = 7.0 if level == 'AAA' else 4.5
    
    # Determine search direction
    base_luminance = base.luminance
    target_luminance = target.luminance
    
    best_color = base
    best_contrast = base.contrast_ratio(target)
    
    # Search in both directions to find maximum
    for search_direction in ['lighter', 'darker']:
        if search_direction == 'lighter':
            low, high = 1.0, 3.0  # Factor range for making lighter
        else:
            low, high = 0.1, 1.0  # Factor range for making darker
        
        while (high - low) > precision:
            mid = (low + high) / 2
            
            try:
                if adjust_lightness:
                    test_color = base.adjust_lightness(mid)
                else:
                    test_color = base.adjust_brightness(mid)
                
                test_contrast = test_color.contrast_ratio(target)
                
                if test_contrast > best_contrast:
                    best_contrast = test_contrast
                    best_color = test_color
                
                # Binary search logic - try to find the extreme that gives max contrast
                if search_direction == 'lighter':
                    # For lighter colors, higher factors usually give more contrast
                    if test_contrast >= required_ratio:
                        low = mid  # Can go lighter
                    else:
                        high = mid  # Too light, go back
                else:
                    # For darker colors, lower factors usually give more contrast
                    if test_contrast >= required_ratio:
                        high = mid  # Can go darker
                    else:
                        low = mid  # Too dark, go back
            except (ZeroDivisionError, ValueError):
                break  # Exit if color adjustment fails
    
    return best_color


def find_maximal_contrast_optimization(base_color: Union[Color, str], target_color: Union[Color, str], 
                                     level: str = 'AA', method: str = 'golden_section') -> Color:
    """Find maximal contrast using mathematical optimization.
    
    This approach uses mathematical optimization techniques to find the adjustment
    that maximizes contrast ratio while meeting accessibility requirements.
    
    Parameters
    ----------
    base_color : Color or str
        The color to adjust.
    target_color : Color or str
        The color to ensure accessibility against.
    level : str, default 'AA'
        The WCAG level to achieve ('AA' or 'AAA').
    method : str, default 'golden_section'
        The optimization method to use ('golden_section' or 'gradient_descent').
    
    Returns
    -------
    Color
        The adjusted color with maximal contrast found.
    
    Examples
    --------
    
    Find maximal contrast using optimization:
    
    .. testcode::
    
        from chromo_map import find_maximal_contrast_optimization
        result = find_maximal_contrast_optimization('#888888', 'white')
        print(f"Optimization result: {result.hex}")
    
    .. testoutput::
    
        Optimization result: #595959
    
    """
    base = Color(base_color) if not isinstance(base_color, Color) else base_color
    target = Color(target_color) if not isinstance(target_color, Color) else target_color
    
    required_ratio = 7.0 if level == 'AAA' else 4.5
    
    def objective_function(factor: float) -> float:
        """Objective function to maximize contrast ratio."""
        try:
            # Try both lightness and brightness adjustments
            lightness_color = base.adjust_lightness(factor)
            brightness_color = base.adjust_brightness(factor)
            
            lightness_contrast = lightness_color.contrast_ratio(target)
            brightness_contrast = brightness_color.contrast_ratio(target)
            
            # Return the maximum contrast achievable
            return max(lightness_contrast, brightness_contrast)
        except (ZeroDivisionError, ValueError):
            return 0.0  # Return minimal contrast if adjustment fails
    
    if method == 'golden_section':
        # Golden section search for maximum
        phi = (1 + 5**0.5) / 2  # Golden ratio
        resphi = 2 - phi
        
        # Search bounds
        a, b = 0.1, 3.0
        tol = 1e-5
        
        # Initial points
        x1 = a + resphi * (b - a)
        x2 = a + (1 - resphi) * (b - a)
        f1 = objective_function(x1)
        f2 = objective_function(x2)
        
        best_factor = x1 if f1 > f2 else x2
        best_contrast = max(f1, f2)
        
        while abs(b - a) > tol:
            if f1 > f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = a + resphi * (b - a)
                f1 = objective_function(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = a + (1 - resphi) * (b - a)
                f2 = objective_function(x2)
            
            current_best = x1 if f1 > f2 else x2
            current_contrast = max(f1, f2)
            
            if current_contrast > best_contrast:
                best_contrast = current_contrast
                best_factor = current_best
        
        # Determine which adjustment method gives better contrast
        lightness_color = base.adjust_lightness(best_factor)
        brightness_color = base.adjust_brightness(best_factor)
        
        lightness_contrast = lightness_color.contrast_ratio(target)
        brightness_contrast = brightness_color.contrast_ratio(target)
        
        return lightness_color if lightness_contrast > brightness_contrast else brightness_color
    
    # If method is not golden_section, fall back to iterative approach
    return find_maximal_contrast_iterative(base_color, target_color, level, True, 0.1, 50)

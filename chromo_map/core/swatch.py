# mypy: ignore-errors
"""Swatch class for chromo_map package."""

import uuid
from typing import Union, Dict, Any, TYPE_CHECKING
from textwrap import dedent
from IPython.display import HTML
from jinja2 import Template

if TYPE_CHECKING:
    from chromo_map.core.color import Color
    from chromo_map.core.gradient import Gradient
else:
    from chromo_map.core.color import Color
    from chromo_map.core.gradient import Gradient


class Swatch:
    """A class for representing a collection of gradients."""

    def __init__(self, gradients, maxn=32):
        self.maxn = maxn
        self.gradients = []
        if isinstance(gradients, dict):
            for name, colors in gradients.items():
                try:
                    self.gradients.append(Gradient(colors, name=name))
                except ValueError as e:
                    raise e
        elif isinstance(gradients, (list, tuple)):
            self.gradients = list(gradients)
        else:
            raise ValueError("Gradients must be a dict or list of Gradient objects")

    def to_dict(self):
        """Convert to a dictionary of gradient names to colors."""
        return {gradient.name: gradient.colors for gradient in self.gradients}

    def __iter__(self):
        """Iterate over gradients."""
        return iter(self.gradients)

    def __len__(self):
        """Return the number of gradients."""
        return len(self.gradients)

    def with_max(self, maxn):
        """Return a new Swatch with a different maximum number of gradients."""
        return Swatch(self.gradients, maxn=maxn)

    def to_grid(self, as_png=False):
        """Convert the swatch to an HTML grid."""
        n = len(self.gradients)
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
                {% for gradient in gradients %}
                    {{ gradient.to_div(maxn, as_png=as_png).data }}
                {% endfor %}
            </div>
        """
            )
        )
        random_id = uuid.uuid4().hex
        return HTML(
            template.render(
                gradients=self.gradients,
                random_id=random_id,
                maxn=self.maxn,
                as_png=as_png,
            )
        )

    def append(self, gradient: "Gradient"):
        """Append a new gradient to the swatch.

        Parameters
        ----------
        gradient : Gradient
            The gradient to append.

        Returns
        -------
        None

        Examples
        --------

        Append a new gradient to the swatch:

        .. testcode::

            from chromo_map import Swatch, Gradient
            swatch = Swatch([])
            swatch.append(Gradient(['#ff0000', '#00ff00', '#0000ff'], name='RGB'))

        .. html-output::

            from chromo_map import Swatch, Gradient
            swatch = Swatch([])
            swatch.append(Gradient(['#ff0000', '#00ff00', '#0000ff'], name='RGB'))
            print(swatch.to_grid().data)

        """
        self.gradients.append(gradient)

    def adjust_hue(self, degrees: float) -> "Swatch":
        """Adjust the hue of all gradients in the swatch.

        Parameters
        ----------
        degrees : float
            The number of degrees to adjust the hue by.

        Returns
        -------
        Swatch
            A new swatch with adjusted hue.

        Examples
        --------

        Adjust hue by 90 degrees:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            shifted = swatch.adjust_hue(90)
            shifted

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            shifted = swatch.adjust_hue(90)
            print(shifted._repr_html_())

        """
        new_gradients = [gradient.adjust_hue(degrees) for gradient in self.gradients]
        return Swatch(new_gradients, maxn=self.maxn)

    def adjust_saturation(self, factor: float) -> "Swatch":
        """Adjust the saturation of all gradients in the swatch.

        Parameters
        ----------
        factor : float
            The factor to multiply saturation by.

        Returns
        -------
        Swatch
            A new swatch with adjusted saturation.

        Examples
        --------

        Decrease saturation by 25%:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            desaturated = swatch.adjust_saturation(0.75)
            desaturated

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            desaturated = swatch.adjust_saturation(0.75)
            print(desaturated._repr_html_())

        """
        new_gradients = [
            gradient.adjust_saturation(factor) for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def adjust_brightness(self, factor: float) -> "Swatch":
        """Adjust the brightness of all gradients in the swatch.

        Parameters
        ----------
        factor : float
            The factor to multiply brightness by.

        Returns
        -------
        Swatch
            A new swatch with adjusted brightness.

        Examples
        --------

        Increase brightness by 10%:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            bright = swatch.adjust_brightness(1.1)
            bright

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            bright = swatch.adjust_brightness(1.1)
            print(bright._repr_html_())

        """
        new_gradients = [
            gradient.adjust_brightness(factor) for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def adjust_lightness(self, factor: float) -> "Swatch":
        """Adjust the lightness of all gradients in the swatch.

        Parameters
        ----------
        factor : float
            The factor to multiply lightness by.

        Returns
        -------
        Swatch
            A new swatch with adjusted lightness.

        Examples
        --------

        Decrease lightness by 15%:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            dark = swatch.adjust_lightness(0.85)
            dark

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            dark = swatch.adjust_lightness(0.85)
            print(dark._repr_html_())

        """
        new_gradients = [
            gradient.adjust_lightness(factor) for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def make_accessible(
        self, background_color: Union[Color, str], level: str = "AA"
    ) -> "Swatch":
        """Make all gradients in the swatch accessible against a background color.

        Parameters
        ----------
        background_color : Color or str
            The background color to ensure accessibility against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').

        Returns
        -------
        Swatch
            A new swatch with accessible gradients.

        Examples
        --------

        Make swatch accessible against white background:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ffcccc', '#ccffcc'], name='Pastels')]
            swatch = Swatch(gradients)
            accessible = swatch.make_accessible('white')
            accessible

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ffcccc', '#ccffcc'], name='Pastels')]
            swatch = Swatch(gradients)
            accessible = swatch.make_accessible('white')
            print(accessible._repr_html_())

        """
        new_gradients = [
            gradient.make_accessible(background_color, level)
            for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def complementary(self) -> "Swatch":
        """Get the complementary swatch (all gradients with complementary colors).

        Returns
        -------
        Swatch
            A new swatch with complementary gradients.

        Examples
        --------

        Get complementary swatch:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            complement = swatch.complementary()
            complement

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff0000', '#00ff00'], name='RedGreen')]
            swatch = Swatch(gradients)
            complement = swatch.complementary()
            print(complement._repr_html_())

        """
        new_gradients = [gradient.complementary() for gradient in self.gradients]
        return Swatch(new_gradients, maxn=self.maxn)

    def analyze_contrast(self, background_color: Union[Color, str]) -> Dict[str, Any]:
        """Analyze contrast ratios of all gradients against a background.

        Parameters
        ----------
        background_color : Color or str
            The background color to analyze against.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing contrast analysis results for each gradient.

        Examples
        --------

        Analyze contrast against white background:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#000000', '#808080'], name='Darks')]
            swatch = Swatch(gradients)
            analysis = swatch.analyze_contrast('white')
            print(f"Gradients analyzed: {len(analysis['gradients'])}")

        .. testoutput::

            Gradients analyzed: 1

        """
        background = (
            Color(background_color)
            if not isinstance(background_color, Color)
            else background_color
        )
        gradient_analyses = []
        all_contrasts = []

        for gradient in self.gradients:
            analysis = gradient.analyze_contrast(background)
            gradient_analyses.append({"name": gradient.name, "analysis": analysis})
            all_contrasts.extend(analysis["contrasts"])

        # Overall statistics
        total_colors = len(all_contrasts)
        accessible_aa = sum(1 for c in all_contrasts if c >= 4.5)
        accessible_aaa = sum(1 for c in all_contrasts if c >= 7.0)

        return {
            "gradients": gradient_analyses,
            "total_colors": total_colors,
            "overall_average_contrast": (
                sum(all_contrasts) / total_colors if all_contrasts else 0
            ),
            "overall_min_contrast": min(all_contrasts) if all_contrasts else 0,
            "overall_max_contrast": max(all_contrasts) if all_contrasts else 0,
            "overall_accessible_aa_count": accessible_aa,
            "overall_accessible_aaa_count": accessible_aaa,
            "overall_accessibility_aa_score": (
                accessible_aa / total_colors if total_colors else 0
            ),
            "overall_accessibility_aaa_score": (
                accessible_aaa / total_colors if total_colors else 0
            ),
        }

    def find_accessible_version(
        self, background_color: Union[Color, str], level: str = "AA"
    ) -> "Swatch":
        """Find accessible version of all gradients in the swatch.

        Parameters
        ----------
        background_color : Color or str
            The background color to ensure accessibility against.
        level : str, default 'AA'
            The WCAG level to achieve ('AA' or 'AAA').

        Returns
        -------
        Swatch
            A new swatch with accessible gradients.

        Examples
        --------

        Find accessible version of swatch:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ffcccc', '#ccffcc'], name='Light')]
            swatch = Swatch(gradients)
            accessible = swatch.find_accessible_version('white')
            accessible

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ffcccc', '#ccffcc'], name='Light')]
            swatch = Swatch(gradients)
            accessible = swatch.find_accessible_version('white')
            print(accessible._repr_html_())

        """
        new_gradients = [
            gradient.find_accessible_version(background_color, level)
            for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def maximize_contrast_iterative(
        self,
        background_color: Union[Color, str],
        level: str = "AA",
        adjust_lightness: bool = True,
        step_size: float = 0.1,
        max_attempts: int = 50,
    ) -> "Swatch":
        """Maximize contrast of all gradients using iterative approach.

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
        Swatch
            A new swatch with maximized contrast gradients.

        Examples
        --------

        Maximize contrast iteratively:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_iterative('white')
            optimized

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_iterative('white')
            print(optimized._repr_html_())

        """
        new_gradients = [
            gradient.maximize_contrast_iterative(
                background_color, level, adjust_lightness, step_size, max_attempts
            )
            for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def maximize_contrast_binary_search(
        self,
        background_color: Union[Color, str],
        level: str = "AA",
        adjust_lightness: bool = True,
        precision: float = 0.001,
    ) -> "Swatch":
        """Maximize contrast of all gradients using binary search.

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
        Swatch
            A new swatch with maximized contrast gradients.

        Examples
        --------

        Maximize contrast with binary search:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_binary_search('white')
            optimized

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_binary_search('white')
            print(optimized._repr_html_())

        """
        new_gradients = [
            gradient.maximize_contrast_binary_search(
                background_color, level, adjust_lightness, precision
            )
            for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def maximize_contrast_optimization(
        self,
        background_color: Union[Color, str],
        level: str = "AA",
        method: str = "golden_section",
    ) -> "Swatch":
        """Maximize contrast of all gradients using mathematical optimization.

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
        Swatch
            A new swatch with maximized contrast gradients.

        Examples
        --------

        Maximize contrast with optimization:

        .. testcode::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_optimization('white')
            optimized

        .. html-output::

            from chromo_map import Swatch, Gradient
            gradients = [Gradient(['#ff6666', '#66ff66'], name='Light')]
            swatch = Swatch(gradients)
            optimized = swatch.maximize_contrast_optimization('white')
            print(optimized._repr_html_())

        """
        new_gradients = [
            gradient.maximize_contrast_optimization(background_color, level, method)
            for gradient in self.gradients
        ]
        return Swatch(new_gradients, maxn=self.maxn)

    def _repr_html_(self) -> str:
        """Return HTML representation for Jupyter notebook display."""
        result = self.to_grid()
        if hasattr(result, "data"):
            return result.data
        return str(result)

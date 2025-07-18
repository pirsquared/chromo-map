"""Accessibility functions for chromo_map package."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chromo_map.core.color import Color
else:
    from chromo_map.core.color import Color


def contrast_ratio(color1: "Color", color2: "Color") -> float:
    """Calculate the contrast ratio between two colors.

    Uses the WCAG 2.1 formula for contrast ratio.

    Parameters
    ----------
    color1 : Color
        The first color.
    color2 : Color
        The second color.

    Returns
    -------
    float
        The contrast ratio (1:1 to 21:1).

    Examples
    --------

    Calculate contrast ratio between black and white:

    .. testcode::

        from chromo_map import contrast_ratio
        ratio = contrast_ratio('black', 'white')
        print(f"Contrast ratio: {ratio:.1f}:1")

    .. testoutput::

        Contrast ratio: 21.0:1

    """
    c1 = Color(color1) if not isinstance(color1, Color) else color1
    c2 = Color(color2) if not isinstance(color2, Color) else color2
    return c1.contrast_ratio(c2)


def is_accessible(color1: "Color", color2: "Color", level: str = "AA") -> bool:
    """Check if two colors have sufficient contrast for accessibility.

    Parameters
    ----------
    color1 : Color
        The first color (typically text).
    color2 : Color
        The second color (typically background).
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

        from chromo_map import is_accessible
        is_accessible('black', 'white')

    .. testoutput::

        True

    """
    c1 = Color(color1) if not isinstance(color1, Color) else color1
    c2 = Color(color2) if not isinstance(color2, Color) else color2
    return c1.is_accessible(c2, level)


def find_accessible_color(
    base_color: "Color",
    target_color: "Color",
    level: str = "AA",
    adjust_lightness: bool = True,
) -> "Color":
    """Find an accessible version of a color by adjusting it.

    Parameters
    ----------
    base_color : Color
        The color to adjust.
    target_color : Color
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
    target = (
        Color(target_color) if not isinstance(target_color, Color) else target_color
    )

    required_ratio = 7.0 if level == "AAA" else 4.5
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

    while (
        current_color.contrast_ratio(target) < required_ratio
        and attempts < max_attempts
    ):
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


def find_maximal_contrast_iterative(
    base_color: "Color",
    target_color: "Color",
    level: str = "AA",
    adjust_lightness: bool = True,
    step_size: float = 0.1,
    max_attempts: int = 50,
) -> "Color":
    """Find maximal contrast using simple iterative approach.

    This approach incrementally adjusts the color until it meets the contrast requirement.
    Simple but may not find the optimal solution.

    Parameters
    ----------
    base_color : Color
        The color to adjust.
    target_color : Color
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
    target = (
        Color(target_color) if not isinstance(target_color, Color) else target_color
    )

    required_ratio = 7.0 if level == "AAA" else 4.5

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


def find_maximal_contrast_binary_search(
    base_color: "Color",
    target_color: "Color",
    level: str = "AA",
    adjust_lightness: bool = True,
    precision: float = 0.001,
) -> "Color":
    """Find maximal contrast using binary search approach.

    This approach uses binary search to efficiently find the optimal adjustment factor
    that maximizes contrast while meeting accessibility requirements.

    Parameters
    ----------
    base_color : Color
        The color to adjust.
    target_color : Color
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
    target = (
        Color(target_color) if not isinstance(target_color, Color) else target_color
    )

    required_ratio = 7.0 if level == "AAA" else 4.5

    # Determine search direction
    base_luminance = base.luminance
    target_luminance = target.luminance

    best_color = base
    best_contrast = base.contrast_ratio(target)

    # Search in both directions to find maximum
    for search_direction in ["lighter", "darker"]:
        if search_direction == "lighter":
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
                if search_direction == "lighter":
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


def find_maximal_contrast_optimization(
    base_color: "Color",
    target_color: "Color",
    level: str = "AA",
    method: str = "golden_section",
) -> "Color":
    """Find maximal contrast using mathematical optimization.

    This approach uses mathematical optimization techniques to find the adjustment
    that maximizes contrast ratio while meeting accessibility requirements.

    Parameters
    ----------
    base_color : Color
        The color to adjust.
    target_color : Color
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
    target = (
        Color(target_color) if not isinstance(target_color, Color) else target_color
    )

    required_ratio = 7.0 if level == "AAA" else 4.5

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

    if method == "golden_section":
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

        return (
            lightness_color
            if lightness_contrast > brightness_contrast
            else brightness_color
        )

    elif method == "gradient_descent":
        # Simple gradient descent
        factor = 1.0
        learning_rate = 0.1
        max_iterations = 100

        best_factor = factor
        best_contrast = objective_function(factor)

        for _ in range(max_iterations):
            # Numerical gradient estimation
            epsilon = 1e-6
            gradient = (
                objective_function(factor + epsilon)
                - objective_function(factor - epsilon)
            ) / (2 * epsilon)

            # Update factor in direction of gradient (maximize)
            new_factor = factor + learning_rate * gradient
            new_contrast = objective_function(new_factor)

            if new_contrast > best_contrast:
                best_contrast = new_contrast
                best_factor = new_factor
                factor = new_factor
            else:
                learning_rate *= 0.9  # Reduce learning rate

            # Early stopping if improvement is minimal
            if abs(new_contrast - best_contrast) < 1e-6:
                break

        # Determine which adjustment method gives better contrast
        lightness_color = base.adjust_lightness(best_factor)
        brightness_color = base.adjust_brightness(best_factor)

        lightness_contrast = lightness_color.contrast_ratio(target)
        brightness_contrast = brightness_color.contrast_ratio(target)

        return (
            lightness_color
            if lightness_contrast > brightness_contrast
            else brightness_color
        )

    else:
        raise ValueError(f"Unknown optimization method: {method}")

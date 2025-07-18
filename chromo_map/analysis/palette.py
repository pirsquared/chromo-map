"""Color analysis functions for chromo_map package."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from chromo_map.core.color import Color
    from chromo_map.core.gradient import Gradient
else:
    from chromo_map.core.color import Color
    from chromo_map.core.gradient import Gradient


def generate_color_palette(base_color: "Color", scheme: str = 'complementary', 
                          count: int = 5) -> List["Color"]:
    """Generate a color palette based on a base color and color scheme.

    Parameters
    ----------
    base_color : Color
        The base color for the palette.
    scheme : str, default 'complementary'
        The color scheme to use ('complementary', 'triadic', 'analogous', 'monochromatic', 'split_complementary').
    count : int, default 5
        The number of colors to generate.

    Returns
    -------
    List[Color]
        A list of colors forming the palette.

    Examples
    --------

    Generate a complementary palette:

    .. testcode::

        from chromo_map import generate_color_palette
        palette = generate_color_palette('red', 'complementary', 3)
        [color.hex for color in palette]

    .. testoutput::

        ['#ff0000', '#00ff00', '#0000ff']

    """
    base = Color(base_color) if not isinstance(base_color, Color) else base_color
    colors = [base]
    
    if scheme == 'complementary':
        if count > 1:
            colors.append(base.complementary())
        if count > 2:
            # Add variations of the base and complement
            for i in range(count - 2):
                factor = 0.7 + (i * 0.3 / (count - 3)) if count > 3 else 0.7
                colors.append(base.adjust_brightness(factor))
    
    elif scheme == 'triadic':
        triad1, triad2 = base.triadic()
        colors.extend([triad1, triad2])
        if count > 3:
            for i in range(count - 3):
                factor = 0.6 + (i * 0.4 / (count - 4)) if count > 4 else 0.6
                colors.append(base.adjust_saturation(factor))
    
    elif scheme == 'analogous':
        step = 30 if count <= 5 else 60 / (count - 1)
        for i in range(1, count):
            angle = step * i
            colors.append(base.adjust_hue(angle))
    
    elif scheme == 'monochromatic':
        for i in range(1, count):
            factor = 0.3 + (i * 0.7 / (count - 1))
            colors.append(base.adjust_brightness(factor))
    
    elif scheme == 'split_complementary':
        if count > 1:
            colors.append(base.adjust_hue(150))
        if count > 2:
            colors.append(base.adjust_hue(210))
        if count > 3:
            for i in range(count - 3):
                factor = 0.5 + (i * 0.5 / (count - 4)) if count > 4 else 0.5
                colors.append(base.adjust_saturation(factor))
    
    return colors[:count]


def analyze_color_harmony(colors: List["Color"]) -> dict:
    """Analyze the color harmony of a list of colors.

    Parameters
    ----------
    colors : List[Color]
        A list of colors to analyze.

    Returns
    -------
    dict
        A dictionary containing harmony analysis results.

    Examples
    --------

    Analyze a list of colors:

    .. testcode::

        from chromo_map import analyze_color_harmony
        analysis = analyze_color_harmony(['red', 'green', 'blue'])
        print(f"Average contrast: {analysis['average_contrast']:.2f}")

    .. testoutput::

        Average contrast: 3.08

    """
    color_objects = [Color(c) if not isinstance(c, Color) else c for c in colors]
    
    if len(color_objects) < 2:
        return {
            'average_contrast': 0.0,
            'min_contrast': 0.0,
            'max_contrast': 0.0,
            'accessibility_score': 0.0,
            'hue_distribution': [],
            'saturation_range': (0.0, 0.0),
            'brightness_range': (0.0, 0.0)
        }
    
    # Calculate contrast ratios
    contrasts = []
    for i in range(len(color_objects)):
        for j in range(i + 1, len(color_objects)):
            contrasts.append(color_objects[i].contrast_ratio(color_objects[j]))
    
    # Calculate accessibility score (percentage of pairs that meet AA standard)
    accessible_pairs = sum(1 for c in contrasts if c >= 4.5)
    accessibility_score = accessible_pairs / len(contrasts) if contrasts else 0
    
    # Analyze hue distribution
    hues = [c.hsv[0] for c in color_objects]
    hue_distribution = sorted(hues)
    
    # Analyze saturation and brightness ranges
    saturations = [c.hsv[1] for c in color_objects]
    brightnesses = [c.hsv[2] for c in color_objects]
    
    return {
        'average_contrast': sum(contrasts) / len(contrasts) if contrasts else 0,
        'min_contrast': min(contrasts) if contrasts else 0,
        'max_contrast': max(contrasts) if contrasts else 0,
        'accessibility_score': accessibility_score,
        'hue_distribution': hue_distribution,
        'saturation_range': (min(saturations), max(saturations)),
        'brightness_range': (min(brightnesses), max(brightnesses))
    }


def get_gradient(name: str, case_sensitive: bool = False) -> Optional["Gradient"]:
    """
    Search for a gradient by name with regex support across all sources.
    
    Parameters
    ----------
    name : str
        The name or regex pattern to search for
    case_sensitive : bool, default False
        Whether to perform case-sensitive search
        
    Returns
    -------
    Optional[Gradient]
        The best matching gradient, or None if no match found
        
    Examples
    --------
    
    Search for viridis:
    
    .. testcode::
    
        from chromo_map import get_gradient
        grad = get_gradient('viridis')
        print(grad.name if grad else 'Not found')
        
    .. testoutput::
    
        viridis
        
    Search with regex:
    
    .. testcode::
    
        from chromo_map import get_gradient
        grad = get_gradient('vir.*')
        print(grad.name if grad else 'Not found')
        
    .. testoutput::
    
        viridis
    """
    # Return None for empty string
    if not name or not name.strip():
        return None
        
    import re
    from typing import List, Dict, Any
    from ..catalog import cmaps
    
    # Compile regex pattern
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(name, flags)
    except re.error:
        # If regex is invalid, treat as literal string
        pattern = re.compile(re.escape(name), flags)
    
    # Collect all matching gradients with metadata
    matches: List[Dict[str, Any]] = []
    
    # Search through all catalog sources
    catalog_sources = [
        ('palettable', cmaps.palettable),
        ('matplotlib', cmaps.matplotlib), 
        ('plotly', cmaps.plotly)
    ]
    
    for source_name, source_catalog in catalog_sources:
        # Recursively search through the catalog structure
        def search_recursive(obj, path=""):
            if hasattr(obj, '_data') and hasattr(obj._data, 'items'):
                # This is a ColorMapDict or AttrDict
                for key, value in obj._data.items():
                    if hasattr(value, 'colors') and hasattr(value, 'name'):
                        # This is a Gradient object
                        if pattern.search(key) or pattern.search(value.name):
                            matches.append({
                                'gradient': value,
                                'source': source_name,
                                'length': len(value.colors),
                                'name': value.name,
                                'match_key': key
                            })
                    else:
                        # Recurse deeper
                        search_recursive(value, f"{path}.{key}")
            elif hasattr(obj, 'items'):
                # This is a regular dict
                for key, value in obj.items():
                    if hasattr(value, 'colors') and hasattr(value, 'name'):
                        # This is a Gradient object
                        if pattern.search(key) or pattern.search(value.name):
                            matches.append({
                                'gradient': value,
                                'source': source_name,
                                'length': len(value.colors),
                                'name': value.name,
                                'match_key': key
                            })
                    else:
                        # Recurse deeper
                        search_recursive(value, f"{path}.{key}")
        
        try:
            search_recursive(source_catalog)
        except Exception:
            # If there's an error with this source, skip it
            continue
    
    # If no matches found, return None
    if not matches:
        return None
    
    # Sort matches by preference: palettable > matplotlib > plotly, then by length (descending)
    source_priority = {'palettable': 3, 'matplotlib': 2, 'plotly': 1}
    
    matches.sort(key=lambda x: (source_priority.get(x['source'], 0), x['length']), reverse=True)
    
    # Return the best match
    best_match = matches[0]['gradient']
    # Type assertion to help mypy understand this is a Gradient
    return best_match  # type: ignore

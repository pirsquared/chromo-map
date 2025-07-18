# mypy: ignore-errors
"""Catalog builders for chromo_map package."""

import json
from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
from importlib_resources import files
from pirrtools import AttrDict, find_instances
from palettable.palette import Palette
import palettable
from _plotly_utils import colors as plotly_colors

if TYPE_CHECKING:
    from chromo_map.core.gradient import Gradient
else:
    from chromo_map.core.gradient import Gradient

from .catalog import ColorMapDict, _dig_for_gradients, _gud_name


def _build_matplotlib_catalog() -> Dict[str, Dict[str, str]]:
    """Build catalog of matplotlib colormaps organized by category."""
    mpl_data = json.loads(
        files("chromo_map.data").joinpath("mpl_cat_names.json").read_text()
    )

    # Map matplotlib categories to standardized types
    category_mapping = {
        "Perceptually Uniform Sequential": "sequential",
        "Sequential": "sequential",
        "Sequential (2)": "sequential",
        "Diverging": "diverging",
        "Cyclic": "cyclic",
        "Qualitative": "qualitative",
        "Miscellaneous": "miscellaneous",
    }

    # Build the catalog
    catalog = {}
    for category, names in mpl_data:
        mapped_category = category_mapping.get(category, "miscellaneous")
        catalog[mapped_category] = catalog.get(mapped_category, {})
        for name in names:
            catalog[mapped_category][name] = name

    return catalog


def _build_plotly_catalog() -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """Build catalog of plotly color scales organized by category."""
    catalog: Dict[str, Dict[str, Dict[str, List[str]]]] = {}

    # Get all color scales from plotly using find_instances
    plotly_cmaps = find_instances(
        cls=list,
        module=plotly_colors,
        tracker_type=AttrDict,
        filter_func=lambda name, _: _gud_name(name),
    )

    # Convert to flat structure
    plotly_collections = dict(_dig_for_gradients(plotly_cmaps))

    # Define plotly types
    plotly_types = {"sequential", "diverging", "qualitative", "cyclical"}

    for key, value in plotly_collections.items():
        original_key = key

        # Handle different key structures
        if len(key) == 1:
            key = ("miscellaneous", "plotly", key[0])
        elif len(key) >= 2:
            if key[0] not in plotly_types:
                key = ("miscellaneous", key[0], key[1] if len(key) > 1 else key[0])
            else:
                key = (key[0], "plotly", key[1] if len(key) > 1 else key[0])

        typ, palette_name, gradient_name = key[:3]

        try:
            # Ensure the structure exists
            if typ not in catalog:
                catalog[typ] = {}
            if palette_name not in catalog[typ]:
                catalog[typ][palette_name] = {}

            # Store the color list directly
            catalog[typ][palette_name][gradient_name] = value
        except Exception as e:
            print(f"Error processing plotly colormap {original_key}: {e}")

    return catalog


def _build_palettable_catalog() -> Dict[str, Dict[str, Dict[str, Palette]]]:
    """Build catalog of palettable palettes organized by module and category."""
    catalog: Dict[str, Dict[str, Dict[str, Palette]]] = {}

    # Get all palettes using find_instances
    palettes = find_instances(
        cls=Palette,
        module=palettable,
        tracker_type=AttrDict,
        filter_func=lambda name, _: _gud_name(name),
    )

    # Convert to nested structure and process
    palettes_sift = {}
    for key, value in _dig_for_gradients(palettes):
        # Handle different key structures
        if len(key) == 2:
            key = (key[0], "special", key[1])

        if len(key) >= 3:
            palette_name, palette_type, gradient_name = key[:3]

            # Extract gradient name without number suffix
            if "_" in gradient_name:
                gradient_name, number_suffix = gradient_name.rsplit("_", maxsplit=1)

            # Build nested structure
            if palette_type not in palettes_sift:
                palettes_sift[palette_type] = {}
            if palette_name not in palettes_sift[palette_type]:
                palettes_sift[palette_type][palette_name] = {}
            if gradient_name.lower() not in palettes_sift[palette_type][palette_name]:
                palettes_sift[palette_type][palette_name][gradient_name.lower()] = {}

            palettes_sift[palette_type][palette_name][gradient_name.lower()][
                key[-1]
            ] = value

    # Select best representative for each gradient
    for palette_type, level1 in palettes_sift.items():
        for palette_name, level2 in level1.items():
            for gradient_name, gradients in level2.items():
                if palette_type not in catalog:
                    catalog[palette_type] = {}
                if palette_name not in catalog[palette_type]:
                    catalog[palette_type][palette_name] = {}

                # Select the gradient with the most colors
                best_gradient = max(gradients.values(), key=lambda x: len(x.mpl_colors))
                catalog[palette_type][palette_name][gradient_name] = best_gradient

    return catalog


def _calculate_quality_score(colors: List[str], source: str) -> float:
    """Calculate a quality score for a colormap based on various factors."""
    score = 0.0

    # Length bonus (more colors generally better)
    score += min(len(colors) / 10.0, 1.0) * 20

    # Source preference (matplotlib > plotly > palettable for consistency)
    source_scores = {"matplotlib": 30, "plotly": 25, "palettable": 20}
    score += source_scores.get(source, 10)

    # Name quality (shorter, cleaner names preferred)
    name_penalty = len(colors[0]) / 50.0 if colors else 0
    score -= name_penalty * 5

    # Smoothness (for gradients - check if colors form a smooth progression)
    if len(colors) >= 3:
        try:
            # Simple heuristic: check if colors progress smoothly
            gradient = Gradient(colors[: min(len(colors), 8)])
            score += 10  # Bonus for being able to create gradient
        except:
            pass  # No penalty if gradient creation fails

    return score


def _find_best_representative(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Find the best representative from a list of candidates."""
    if not candidates:
        return {}

    # Calculate scores for all candidates
    scored = []
    for candidate in candidates:
        score = _calculate_quality_score(
            candidate.get("colors", []), candidate.get("source", "")
        )
        scored.append((score, candidate))

    # Return the highest scoring candidate
    return max(scored, key=lambda x: x[0])[1]


def _build_unified_catalog() -> ColorMapDict:
    """Build a unified catalog with multiple organization structures."""
    cmaps = ColorMapDict()

    # Build individual catalogs
    mpl_catalog = _build_matplotlib_catalog()
    plotly_catalog = _build_plotly_catalog()
    palettable_catalog = _build_palettable_catalog()

    # === MATPLOTLIB STRUCTURES ===
    # 1. matplotlib_by_type_by_palette_name
    cmaps.matplotlib_by_type_by_palette_name = ColorMapDict()
    for typ, colormaps in mpl_catalog.items():
        cmaps.matplotlib_by_type_by_palette_name[typ] = ColorMapDict()
        for name, cmap_name in colormaps.items():
            cmaps.matplotlib_by_type_by_palette_name[typ][name] = Gradient(
                cmap_name, name=name
            )

    # 2. matplotlib_by_palette_name (flat by name)
    cmaps.matplotlib_by_palette_name = ColorMapDict()
    for typ, colormaps in mpl_catalog.items():
        for name, cmap_name in colormaps.items():
            cmaps.matplotlib_by_palette_name[name] = Gradient(cmap_name, name=name)

    # 3. matplotlib_by_type (grouped by type)
    cmaps.matplotlib_by_type = ColorMapDict()
    for typ, colormaps in mpl_catalog.items():
        gradients = [
            Gradient(cmap_name, name=name) for name, cmap_name in colormaps.items()
        ]
        cmaps.matplotlib_by_type[typ] = ColorMapDict(
            {name: grad for name, grad in zip(colormaps.keys(), gradients)}
        )

    # === PLOTLY STRUCTURES ===
    # 1. plotly_by_type_by_palette_name
    cmaps.plotly_by_type_by_palette_name = ColorMapDict()
    for typ, palettes in plotly_catalog.items():
        cmaps.plotly_by_type_by_palette_name[typ] = ColorMapDict()
        for palette_name, gradients in palettes.items():
            cmaps.plotly_by_type_by_palette_name[typ][palette_name] = ColorMapDict()
            for gradient_name, colors in gradients.items():
                try:
                    cmaps.plotly_by_type_by_palette_name[typ][palette_name][
                        gradient_name
                    ] = Gradient(colors, name=gradient_name)
                except:
                    continue

    # 2. plotly_by_palette_name (flat by name)
    cmaps.plotly_by_palette_name = ColorMapDict()
    for typ, palettes in plotly_catalog.items():
        for palette_name, gradients in palettes.items():
            for gradient_name, colors in gradients.items():
                try:
                    cmaps.plotly_by_palette_name[gradient_name] = Gradient(
                        colors, name=gradient_name
                    )
                except:
                    continue

    # 3. plotly_by_type (grouped by type)
    cmaps.plotly_by_type = ColorMapDict()
    for typ, palettes in plotly_catalog.items():
        cmaps.plotly_by_type[typ] = ColorMapDict()
        for palette_name, gradients in palettes.items():
            for gradient_name, colors in gradients.items():
                try:
                    cmaps.plotly_by_type[typ][gradient_name] = Gradient(
                        colors, name=gradient_name
                    )
                except:
                    continue

    # === PALETTABLE STRUCTURES ===
    # 1. palettable_by_type_by_palette_name
    cmaps.palettable_by_type_by_palette_name = ColorMapDict()
    for typ, palettes in palettable_catalog.items():
        cmaps.palettable_by_type_by_palette_name[typ] = ColorMapDict()
        for palette_name, gradients in palettes.items():
            cmaps.palettable_by_type_by_palette_name[typ][palette_name] = ColorMapDict()
            for gradient_name, palette in gradients.items():
                try:
                    cmaps.palettable_by_type_by_palette_name[typ][palette_name][
                        gradient_name
                    ] = Gradient(palette.mpl_colors, name=gradient_name)
                except:
                    continue

    # 2. palettable_by_palette_name (flat by name)
    cmaps.palettable_by_palette_name = ColorMapDict()
    for typ, palettes in palettable_catalog.items():
        for palette_name, gradients in palettes.items():
            for gradient_name, palette in gradients.items():
                try:
                    cmaps.palettable_by_palette_name[gradient_name] = Gradient(
                        palette.mpl_colors, name=gradient_name
                    )
                except:
                    continue

    # 3. palettable_by_type (grouped by type)
    cmaps.palettable_by_type = ColorMapDict()
    for typ, palettes in palettable_catalog.items():
        cmaps.palettable_by_type[typ] = ColorMapDict()
        for palette_name, gradients in palettes.items():
            for gradient_name, palette in gradients.items():
                try:
                    cmaps.palettable_by_type[typ][gradient_name] = Gradient(
                        palette.mpl_colors, name=gradient_name
                    )
                except:
                    continue

    # === LEGACY STRUCTURES (for backward compatibility) ===
    cmaps.matplotlib = cmaps.matplotlib_by_type_by_palette_name
    cmaps.plotly = cmaps.plotly_by_type_by_palette_name
    cmaps.palettable = cmaps.palettable_by_type_by_palette_name

    # === UNIFIED FLAT ACCESS ===
    # Build unified flat access with best representatives
    all_colormaps: Dict[str, List[Dict[str, Any]]] = {}

    # Collect all colormaps with metadata
    for typ, colormaps in mpl_catalog.items():
        for name, cmap_name in colormaps.items():
            key = name.lower()
            if key not in all_colormaps:
                all_colormaps[key] = []
            all_colormaps[key].append(
                {
                    "name": name,
                    "source": "matplotlib",
                    "colors": cmap_name,
                    "category": typ,
                    "gradient": Gradient(cmap_name, name=name),
                }
            )

    for typ, palettes in plotly_catalog.items():
        for palette_name, gradients in palettes.items():
            for gradient_name, colors in gradients.items():
                key = gradient_name.lower()
                if key not in all_colormaps:
                    all_colormaps[key] = []
                try:
                    all_colormaps[key].append(
                        {
                            "name": gradient_name,
                            "source": "plotly",
                            "colors": colors,
                            "category": typ,
                            "gradient": Gradient(colors, name=gradient_name),
                        }
                    )
                except:
                    continue

    for typ, palettes in palettable_catalog.items():
        for palette_name, gradients in palettes.items():
            for gradient_name, palette in gradients.items():
                key = gradient_name.lower()
                if key not in all_colormaps:
                    all_colormaps[key] = []
                try:
                    all_colormaps[key].append(
                        {
                            "name": gradient_name,
                            "source": "palettable",
                            "colors": palette.mpl_colors,
                            "category": f"{typ}.{palette_name}",
                            "gradient": Gradient(
                                palette.mpl_colors, name=gradient_name
                            ),
                        }
                    )
                except:
                    continue

    # Create flat access with best representatives
    cmaps.all = ColorMapDict()
    for key, candidates in all_colormaps.items():
        best = _find_best_representative(candidates)
        if best:
            cmaps.all[key] = best["gradient"]

    return cmaps

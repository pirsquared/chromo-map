#!/usr/bin/env python3
"""Generate visual catalog HTML for documentation."""

import sys
import os

sys.path.insert(0, os.path.abspath(".."))


def generate_visual_catalog():
    """Generate HTML content for the visual catalog documentation."""

    try:
        from chromo_map import cmaps

        print("Successfully imported cmaps")
        print(f"Type of cmaps: {type(cmaps)}")

        # Check if cmaps has the expected structure
        if hasattr(cmaps, "plotly_by_type"):
            print("Found plotly_by_type")
        if hasattr(cmaps, "matplotlib_by_type"):
            print("Found matplotlib_by_type")
        if hasattr(cmaps, "palettable_by_type"):
            print("Found palettable_by_type")

        # Generate separate pages for each source
        sources = {
            "plotly_by_type": {
                "title": "Plotly Color Scales",
                "filename": "catalog_plotly.rst",
                "description": "Beautiful, modern color scales from Plotly for web visualizations and interactive plots.",
            },
            "matplotlib_by_type": {
                "title": "Matplotlib Colormaps",
                "filename": "catalog_matplotlib.rst",
                "description": "Comprehensive collection of scientific colormaps from matplotlib, including perceptually uniform and classic options.",
            },
            "palettable_by_type": {
                "title": "Palettable Palettes",
                "filename": "catalog_palettable.rst",
                "description": "Curated color palettes from Palettable, including ColorBrewer and other professional color schemes.",
            },
        }

        # Generate individual source pages
        for attr_name, source_info in sources.items():
            if hasattr(cmaps, attr_name):
                source_dict = getattr(cmaps, attr_name)
                print(f"Processing {attr_name}: {type(source_dict)}")

                html_content = []

                # Process each category in this source
                for category_name, category_dict in source_dict.items():
                    if hasattr(category_dict, "_repr_html_"):
                        print(f"  Found category: {category_name}")

                        # Add horizontal rule for visual separation (except for first category)
                        if html_content:  # Only add HR if this isn't the first category
                            html_content.append("\n----\n")

                        html_content.append(
                            f"\n{category_name.title()}\n{'-' * len(category_name)}\n"
                        )
                        html_content.append(".. raw:: html\n\n")

                        # Get the HTML content and indent it properly for RST
                        html_output = category_dict._repr_html_()
                        indented_html = "\n".join(
                            "   " + line for line in html_output.split("\n")
                        )
                        html_content.append(indented_html + "\n")

                        # Add extra spacing after each category
                        html_content.append(
                            "\n|\n"
                        )  # RST forced line break with spacing
                    else:
                        print(f"  Category {category_name} has no _repr_html_ method")

                # Write individual source RST content
                rst_content = "\n".join(html_content)

                rst_template = f"""{source_info['title']}
{'=' * len(source_info['title'])}

{source_info['description']}

{rst_content}

Navigation
----------

:doc:`Back to Visual Catalog Overview <catalog_visual>`

:doc:`Back to Catalog API <api/catalog>`
"""

                with open(
                    f'source/{source_info["filename"]}', "w", encoding="utf-8"
                ) as f:
                    f.write(rst_template)

                print(f"Generated {source_info['filename']} successfully!")

        # Generate main overview page
        overview_template = """Visual Color Catalog
====================

This page provides access to visual galleries for all color palette sources in chromo-map.

Overview
--------

Browse beautiful color swatches organized by source and type. Each source provides hundreds of carefully curated color palettes for different use cases.

Sources
-------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   catalog_plotly
   catalog_matplotlib  
   catalog_palettable

Source Details
--------------

**Plotly Color Scales**
   Modern, web-friendly color scales perfect for interactive visualizations and dashboards.
   
   :doc:`Browse Plotly Colors <catalog_plotly>`

**Matplotlib Colormaps**
   Scientific and perceptually uniform colormaps from the matplotlib library.
   
   :doc:`Browse Matplotlib Colors <catalog_matplotlib>`

**Palettable Palettes**
   Professional color schemes including ColorBrewer and other curated collections.
   
   :doc:`Browse Palettable Colors <catalog_palettable>`

Navigation
----------

:doc:`Back to Catalog API <api/catalog>`
"""

        with open("source/catalog_visual.rst", "w", encoding="utf-8") as f:
            f.write(overview_template)

        print("Generated catalog_visual.rst overview page successfully!")

    except Exception as e:
        print(f"Error generating visual catalog: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    generate_visual_catalog()

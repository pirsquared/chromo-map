# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from bs4 import BeautifulSoup


sys.path.insert(0, os.path.abspath("../.."))
import chromo_map as cm  # noqa: E402
from chromo_map import Color  # noqa: E402
print(os.path.abspath("."))

project = "chromo_map"
copyright = "2024, Sean Smith"
author = "Sean Smith"
release = "0.1.14"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
]

autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Static files ------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path

html_favicon = "_static/pirr_logo.svg"


class HTMLOutputDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        # Combine all lines into a single string
        code = "\n".join(self.content)

        # Capture stdout and stderr
        stdout = io.StringIO()
        stderr = io.StringIO()

        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # Execute the code
                exec(code, globals())

            output = stdout.getvalue()
            error = stderr.getvalue()

            # Create the output node
            if output:
                output = rf"""
                <div class="highlight-none notranslate">
                    <div class="html-output">{output}</div>
                </div>
                """
                output = BeautifulSoup(output, "html.parser").prettify()
                return [nodes.raw("", output, format="html")]
            elif error:
                return [nodes.error(None, nodes.paragraph(text=f"Error: {error}"))]
            else:
                return [nodes.paragraph(text="No output generated.")]

        except Exception as e:
            return [nodes.error(None, nodes.paragraph(text=f"Error: {str(e)}"))]


def setup(app):
    app.add_directive("html-output", HTMLOutputDirective)
    app.add_css_file("custom.css")

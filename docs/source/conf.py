# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import io
import sys
import doctest
from contextlib import redirect_stdout, redirect_stderr
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from bs4 import BeautifulSoup


sys.path.insert(0, os.path.abspath("../.."))

project = "chromo_map"
copyright = "2024, Sean Smith"
author = "Sean Smith"
release = "0.1.15"

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
    "sphinx.ext.inheritance_diagram",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
    "nbsphinx",
]

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
    'exclude-members': '__weakref__',
}

autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# nbsphinx configuration for Jupyter notebooks
nbsphinx_execute = 'always'  # Always execute notebooks
nbsphinx_kernel_name = 'python3'  # Use Python 3 kernel
nbsphinx_allow_errors = True  # Continue building even if cells have errors
nbsphinx_timeout = 60  # Timeout for cell execution (seconds)

# Doctest configuration
doctest_default_flags = (
    doctest.ELLIPSIS |
    doctest.IGNORE_EXCEPTION_DETAIL |
    doctest.NORMALIZE_WHITESPACE |
    doctest.DONT_ACCEPT_TRUE_FOR_1
)

# Don't add input/output prompts to code blocks
nbsphinx_prolog = """
.. raw:: html

    <style>
    .nbinput .prompt, .nboutput .prompt {
        display: none;
    }
    </style>
"""

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

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


def generate_visual_catalog_hook(app, config):
    """Hook to generate visual catalog before building documentation."""
    try:
        print("Generating visual catalog...")
        import subprocess
        import os
        
        # Get the docs directory
        docs_dir = os.path.dirname(os.path.dirname(__file__))
        script_path = os.path.join(docs_dir, 'generate_visual_catalog.py')
        
        if os.path.exists(script_path):
            # Run the visual catalog generation script
            result = subprocess.run([sys.executable, script_path], 
                                  cwd=docs_dir, 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print("Visual catalog generated successfully!")
            else:
                print(f"Warning: Visual catalog generation failed: {result.stderr}")
        else:
            print("Warning: generate_visual_catalog.py not found")
            
    except Exception as e:
        print(f"Warning: Could not generate visual catalog: {e}")


def setup(app):
    app.add_directive("html-output", HTMLOutputDirective)
    app.add_css_file("custom.css")
    
    # Add the visual catalog generation hook
    app.connect('config-inited', generate_visual_catalog_hook)

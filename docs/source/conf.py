# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import shutil

sys.path.insert(0, os.path.abspath("../.."))

project = "chromo_map"
copyright = "2024, Sean Smith"
author = "Sean Smith"
release = "0.1.12"

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

def copy_coverage_report(app, exception):
    src = os.path.join(app.outdir, '..', '..', '..', 'htmlcov')
    dst = os.path.join(app.outdir, 'coverage')
    if os.path.exists(src) and os.path.isdir(src):
        shutil.copytree(src, dst)


def setup(app):
    app.add_css_file("custom.css")
    app.connect('build-finished', copy_coverage_report)

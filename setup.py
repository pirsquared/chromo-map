"""setup.py.

This minimal setup.py file is included to support editable installations using
pip's `-e` option. The primary project configuration is specified in the
pyproject.toml file. This setup.py is only used for development installations
and ensures compatibility with tools and workflows that rely on setup.py.
"""

from setuptools import setup

# All configuration is in pyproject.toml
# This setup.py exists only for editable installs compatibility
setup()

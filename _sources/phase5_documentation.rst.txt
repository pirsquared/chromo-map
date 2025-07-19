Comprehensive Documentation for chromo-map Phase 5
==================================================

This document provides detailed documentation for all the new functions and improvements
implemented in Phase 5 of the chromo-map project.

Functions Covered:
- get_gradient()
- Color.__repr__() improvements
- Gradient.__repr__() improvements

Classes Covered:
- Color (rich output enhancements)
- Gradient (rich output enhancements)

get_gradient() Function
-----------------------

.. autofunction:: chromo_map.get_gradient
   :no-index:

The get_gradient function provides a powerful search capability for finding gradients
from multiple colormap sources.

**Parameters:**

- ``name`` (str): The name or pattern to search for. Can be:
  - Exact colormap name (e.g., 'viridis')
  - Regex pattern (e.g., 'vir.*', 'Set[0-9]+')
  - Partial name (e.g., 'plas' for 'plasma')

- ``case_sensitive`` (bool, optional): Whether to perform case-sensitive search.
  Default is False.

**Returns:**

- ``Optional[Gradient]``: The best matching gradient, or None if no matches found.

**Search Algorithm:**

1. **Source Priority**: Searches sources in order of preference:
   - Palettable (highest priority)
   - Matplotlib 
   - Plotly (lowest priority)

2. **Pattern Matching**: Uses regex search for flexible pattern matching

3. **Length Preference**: Within same source, prefers longer gradients

4. **Error Handling**: Invalid regex patterns are treated as literal strings

**Examples:**

.. code-block:: python

    # Exact match
    gradient = get_gradient('viridis')
    
    # Case insensitive (default)
    gradient = get_gradient('VIRIDIS')
    
    # Case sensitive
    gradient = get_gradient('viridis', case_sensitive=True)
    
    # Regex pattern
    gradient = get_gradient('vir.*')  # Matches viridis
    gradient = get_gradient('Set[0-9]+')  # Matches Set1, Set2, etc.
    
    # Partial match
    gradient = get_gradient('plas')  # May match plasma

**Use Cases:**

- **Interactive Exploration**: Quickly find gradients without knowing exact names
- **Fuzzy Search**: Find gradients with partial or approximate names
- **Pattern-Based Discovery**: Use regex to find families of related gradients
- **Source-Aware Selection**: Automatically prefer higher-quality sources

**Implementation Details:**

The function recursively searches through all available colormap catalogs,
applying regex patterns to find matches. Results are sorted by source priority
and gradient length, ensuring the best available match is returned.

Color.__repr__() Improvements
-----------------------------

The Color class now provides rich terminal output with Windows compatibility.

**Key Features:**

- **Windows Compatibility**: Uses background colors instead of Unicode blocks
- **Rich Integration**: Seamlessly integrates with the rich library
- **Visual Feedback**: Provides immediate visual representation of colors
- **Consistent Formatting**: Maintains consistent output across platforms

**Technical Implementation:**

.. code-block:: python

    def __repr__(self) -> str:
        '''Rich representation showing color as background with spaces.'''
        from rich.text import Text
        
        # Use background color with spaces for Windows compatibility
        text = Text('  ', style=f'on {self.hex}')
        return text

**Benefits:**

- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Terminal Integration**: Displays colors directly in terminal output
- **Development Workflow**: Enhances debugging and interactive development
- **User Experience**: Provides immediate visual feedback

Gradient.__repr__() Improvements
--------------------------------

The Gradient class now provides sophisticated rich output with intelligent scaling.

**Key Features:**

- **Character Limit**: Maximum 64 characters for manageable output
- **Intelligent Resampling**: Automatically resamples long gradients
- **Adaptive Spacing**: Scales from 2 spaces to 1 space based on length
- **Visual Progression**: Shows clear color transitions

**Technical Implementation:**

.. code-block:: python

    def __repr__(self) -> str:
        '''Rich representation with 64-character limit and adaptive spacing.'''
        from rich.text import Text
        
        max_chars = 64
        
        # Determine spacing based on length
        if len(self.colors) <= 32:
            spaces_per_color = 2
        else:
            spaces_per_color = 1
        
        # Calculate required colors for display
        required_colors = max_chars // spaces_per_color
        
        # Resample if necessary
        if len(self.colors) > required_colors:
            display_gradient = self.resize(required_colors)
        else:
            display_gradient = self
        
        # Build rich text representation
        text = Text()
        for color in display_gradient.colors:
            text.append(' ' * spaces_per_color, style=f'on {color.hex}')
        
        return text

**Scaling Logic:**

- **≤32 colors**: 2 spaces per color (detailed view)
- **>32 colors**: 1 space per color (compact view)
- **>64 spaces needed**: Automatically resample to fit

**Benefits:**

- **Scalability**: Handles gradients of any length
- **Readability**: Maintains visual clarity at all scales
- **Performance**: Efficient rendering through intelligent sampling
- **Consistency**: Predictable output format

Rich Library Integration
------------------------

All improvements are built on the rich library for cross-platform compatibility.

**Key Components:**

- **Text Objects**: Use rich.text.Text for styled output
- **Style Syntax**: Leverage rich's style system for colors
- **Console Integration**: Seamless integration with rich console
- **Platform Compatibility**: Automatic platform-specific adaptations

**Style Format:**

.. code-block:: python

    # Background color style
    style = f'on {color.hex}'  # e.g., 'on #FF0000'
    
    # Create styled text
    text = Text('  ', style=style)

**Console Usage:**

.. code-block:: python

    from rich.console import Console
    
    console = Console()
    color = Color('#FF0000')
    gradient = get_gradient('viridis')
    
    # Print with rich formatting
    console.print(color)
    console.print(gradient)

Testing Strategy
----------------

Comprehensive test suites cover all new functionality:

**Test Categories:**

1. **Unit Tests**: Individual function behavior
2. **Integration Tests**: Cross-component interactions
3. **Visual Tests**: Rich output validation
4. **Edge Cases**: Boundary conditions and error handling
5. **Performance Tests**: Scalability and efficiency
6. **Platform Tests**: Cross-platform compatibility

**Test Files:**

- ``test_get_gradient.py``: Comprehensive get_gradient testing
- ``test_color_rich.py``: Color class rich output testing
- ``test_gradient_rich.py``: Gradient class rich output testing

**Coverage Goals:**

- >90% code coverage for new functions
- All edge cases and error conditions
- Platform-specific behavior validation
- Performance benchmarks

Future Enhancements
-------------------

Planned improvements for future phases:

1. **Additional Sources**: Support for more colormap libraries
2. **Caching**: Intelligent caching for performance
3. **Configuration**: User-configurable search preferences
4. **Export Options**: Multiple output formats for gradients
5. **Interactive Tools**: CLI tools for gradient exploration

**Compatibility:**

- Python 3.8+
- Rich library 10.0+
- Windows 10+, macOS 10.14+, Linux (modern distributions)

**Dependencies:**

- rich: Terminal formatting and styling
- matplotlib: Core colormap functionality
- palettable: Additional colormap sources
- plotly: Web-based colormap sources

This comprehensive documentation provides complete coverage of all Phase 5
enhancements, ensuring users can fully leverage the new functionality.
"""

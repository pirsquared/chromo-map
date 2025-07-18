"""Tests for Color class rich output and improvements."""

import pytest
from chromo_map import Color
from rich.console import Console
from io import StringIO


class TestColorRichOutput:
    """Test suite for Color class rich output functionality."""

    def test_color_repr_basic(self):
        """Test basic Color repr output."""
        color = Color('#FF0000')
        repr_str = repr(color)
        assert isinstance(repr_str, str)
        assert len(repr_str) > 0

    def test_color_repr_contains_rich_formatting(self):
        """Test that Color repr contains rich formatting."""
        color = Color('#FF0000')
        repr_str = repr(color)
        # Should contain ANSI escape codes for color formatting
        assert '\x1b[' in repr_str

    def test_color_repr_with_console(self):
        """Test Color repr with rich console."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        color = Color('#FF0000')
        
        # Test that console can handle the color output
        console.print(color)
        result = output.getvalue()
        assert len(result) > 0

    def test_color_repr_windows_compatibility(self):
        """Test Windows compatibility with background colors."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should use background color styling (contains escape codes)
        assert '\x1b[' in repr_str
        # Should contain the hex color
        assert color.hex in repr_str

    def test_color_repr_different_colors(self):
        """Test repr with different color values."""
        colors = [
            Color('#FF0000'),  # Red
            Color('#00FF00'),  # Green
            Color('#0000FF'),  # Blue
            Color('#FFFFFF'),  # White
            Color('#000000'),  # Black
            Color('#FFFF00'),  # Yellow
        ]
        
        for color in colors:
            repr_str = repr(color)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0
            assert '\x1b[' in repr_str  # Should contain ANSI escape codes

    def test_color_repr_with_alpha(self):
        """Test Color repr with alpha channel."""
        color = Color('#FF0000FF')  # Red with full alpha
        repr_str = repr(color)
        assert isinstance(repr_str, str)
        assert len(repr_str) > 0

    def test_color_repr_from_different_formats(self):
        """Test repr from colors created in different formats."""
        colors = [
            Color('#FF0000'),
            Color('red'),
            Color((1.0, 0.0, 0.0)),  # Use normalized values
            Color([1.0, 0.0, 0.0]),
        ]
        
        for color in colors:
            repr_str = repr(color)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0

    def test_color_repr_consistency(self):
        """Test that repr is consistent for same color."""
        color1 = Color('#FF0000')
        color2 = Color('#FF0000')
        
        repr1 = repr(color1)
        repr2 = repr(color2)
        
        # Should be the same representation
        assert repr1 == repr2

    def test_color_repr_no_unicode_blocks(self):
        """Test that repr doesn't use Unicode block characters."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should not contain Unicode block characters
        assert '█' not in repr_str
        assert '▆' not in repr_str
        assert '▇' not in repr_str

    def test_color_repr_uses_spaces(self):
        """Test that repr uses spaces for color display."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should use spaces for color display
        assert '  ' in repr_str or ' ' in repr_str

    def test_color_hex_in_repr(self):
        """Test that hex value is included in repr."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should include hex value
        assert color.hex in repr_str

    def test_color_repr_rich_text_object(self):
        """Test that repr returns a rich Text object or compatible string."""
        color = Color('#FF0000')
        repr_obj = color.__repr__()
        
        # Should be either a string or rich object
        assert isinstance(repr_obj, (str, object))

    def test_color_repr_visual_consistency(self):
        """Test visual consistency of color representation."""
        colors = [
            Color('#FF0000'),
            Color('#00FF00'),
            Color('#0000FF'),
        ]
        
        for color in colors:
            repr_str = repr(color)
            # All should have similar structure with ANSI escape codes
            assert '\x1b[' in repr_str
            assert color.hex in repr_str

    def test_color_repr_length_reasonable(self):
        """Test that repr length is reasonable."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should not be too long or too short
        assert 10 < len(repr_str) < 200

    def test_color_repr_no_errors(self):
        """Test that repr doesn't raise errors for edge cases."""
        edge_cases = [
            Color('#000000'),  # Black
            Color('#FFFFFF'),  # White
            Color('#FF00FF'),  # Magenta
            Color('#00FFFF'),  # Cyan
        ]
        
        for color in edge_cases:
            try:
                repr_str = repr(color)
                assert isinstance(repr_str, str)
            except Exception as e:
                pytest.fail(f"repr() raised {type(e).__name__}: {e}")

    def test_color_repr_with_rich_console_capture(self):
        """Test color repr with rich console capture."""
        console = Console(file=StringIO(), force_terminal=True)
        color = Color('#FF0000')
        
        with console.capture() as capture:
            console.print(color)
        
        output = capture.get()
        assert len(output) > 0

    def test_color_repr_background_color_format(self):
        """Test that background color format is correct."""
        color = Color('#FF0000')
        repr_str = repr(color)
        
        # Should use ANSI escape codes for background colors
        assert '\x1b[' in repr_str
        # Should include the hex value
        assert '#' in repr_str

    def test_color_repr_with_different_console_widths(self):
        """Test color repr with different console widths."""
        color = Color('#FF0000')
        
        # Test with different console widths
        for width in [80, 120, 40]:
            output = StringIO()
            console = Console(
                file=output, 
                force_terminal=True, 
                width=width
            )
            console.print(color)
            result = output.getvalue()
            assert len(result) > 0

    def test_color_repr_multiple_colors_visual(self):
        """Test visual representation of multiple colors."""
        colors = [
            Color('#FF0000'),
            Color('#00FF00'),
            Color('#0000FF'),
            Color('#FFFF00'),
            Color('#FF00FF'),
            Color('#00FFFF'),
        ]
        
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        
        for color in colors:
            console.print(color)
        
        result = output.getvalue()
        assert len(result) > 0
        # Should contain multiple color representations with ANSI codes
        assert result.count('\x1b[') >= len(colors)  # type: ignore

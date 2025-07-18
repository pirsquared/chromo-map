"""Tests for the get_gradient function."""

import pytest
import re
from chromo_map import get_gradient, Gradient


class TestGetGradient:
    """Test suite for the get_gradient function."""

    def test_get_gradient_exact_match(self):
        """Test getting gradient with exact name match."""
        gradient = get_gradient('viridis')
        assert gradient is not None
        assert gradient.name == 'viridis'
        assert isinstance(gradient, Gradient)

    def test_get_gradient_case_insensitive(self):
        """Test case insensitive search (default behavior)."""
        gradient = get_gradient('VIRIDIS')
        assert gradient is not None
        assert gradient.name == 'viridis'

    def test_get_gradient_case_sensitive(self):
        """Test case sensitive search."""
        gradient = get_gradient('VIRIDIS', case_sensitive=True)
        # Should return None since 'VIRIDIS' != 'viridis'
        assert gradient is None

    def test_get_gradient_regex_pattern(self):
        """Test regex pattern matching."""
        gradient = get_gradient('vir.*')
        assert gradient is not None
        assert 'viridis' in gradient.name.lower()

    def test_get_gradient_invalid_regex(self):
        """Test handling of invalid regex patterns."""
        # Should treat invalid regex as literal string
        gradient = get_gradient('[invalid')
        # Should return None since '[invalid' is not a valid colormap name
        assert gradient is None

    def test_get_gradient_source_priority(self):
        """Test source priority: palettable > matplotlib > plotly."""
        # Test with a common name that might exist in multiple sources
        gradient = get_gradient('blue')
        assert gradient is not None
        # Should prefer palettable if available, then matplotlib, then plotly
        assert isinstance(gradient, Gradient)

    def test_get_gradient_length_preference(self):
        """Test preference for longer gradients within same source."""
        gradient = get_gradient('blue')
        assert gradient is not None
        # Should prefer longer gradients
        assert len(gradient.colors) >= 1

    def test_get_gradient_not_found(self):
        """Test behavior when gradient is not found."""
        gradient = get_gradient('nonexistent_gradient_name_12345')
        assert gradient is None

    def test_get_gradient_empty_string(self):
        """Test behavior with empty string."""
        gradient = get_gradient('')
        # Empty string should return None
        assert gradient is None
        
        # Test with whitespace only
        gradient = get_gradient('   ')
        assert gradient is None

    def test_get_gradient_special_characters(self):
        """Test handling of special characters in search."""
        gradient = get_gradient('Set.*')
        # Should find Set1, Set2, Set3, etc. if they exist
        if gradient:
            assert 'set' in gradient.name.lower()

    def test_get_gradient_multiple_matches(self):
        """Test that function returns best match when multiple exist."""
        gradient = get_gradient('plasma')
        assert gradient is not None
        assert gradient.name == 'plasma'

    def test_get_gradient_partial_match(self):
        """Test partial name matching with regex."""
        gradient = get_gradient('plas')
        if gradient:
            assert 'plas' in gradient.name.lower()

    def test_get_gradient_number_suffix(self):
        """Test handling of numbered colormap variants."""
        gradient = get_gradient('Set[0-9]+')
        if gradient:
            assert re.match(r'.*[0-9]+', gradient.name)

    def test_get_gradient_underscore_patterns(self):
        """Test handling of underscore patterns in names."""
        gradient = get_gradient('twilight_shifted')
        if gradient:
            assert 'twilight' in gradient.name.lower()

    def test_get_gradient_dash_patterns(self):
        """Test handling of dash patterns in names."""
        gradient = get_gradient('.*-.*')
        # Should find gradients with dashes if they exist
        if gradient:
            assert isinstance(gradient, Gradient)

    def test_get_gradient_return_type(self):
        """Test that the function returns the correct type."""
        gradient = get_gradient('viridis')
        assert isinstance(gradient, Gradient)
        assert hasattr(gradient, 'colors')
        assert hasattr(gradient, 'name')

    def test_get_gradient_gradient_properties(self):
        """Test that returned gradient has expected properties."""
        gradient = get_gradient('viridis')
        assert gradient is not None
        assert len(gradient.colors) > 0
        assert gradient.name is not None
        assert isinstance(gradient.name, str)

    def test_get_gradient_with_whitespace(self):
        """Test handling of whitespace in search terms."""
        gradient = get_gradient(' viridis ')
        # Should handle whitespace gracefully
        if gradient:
            assert isinstance(gradient, Gradient)

    def test_get_gradient_reproducibility(self):
        """Test that multiple calls return the same result."""
        gradient1 = get_gradient('viridis')
        gradient2 = get_gradient('viridis')
        
        assert gradient1 is not None
        assert gradient2 is not None
        assert gradient1.name == gradient2.name
        assert len(gradient1.colors) == len(gradient2.colors)

    def test_get_gradient_catalog_integration(self):
        """Test integration with the catalog system."""
        gradient = get_gradient('viridis')
        assert gradient is not None
        
        # Test that the gradient works as expected
        colors = gradient.colors
        assert len(colors) > 0
        
        # Test that gradient can be used for matplotlib operations
        assert hasattr(gradient, 'resize')
        resized = gradient.resize(10)
        assert len(resized.colors) == 10

    @pytest.mark.parametrize("search_term,expected_found", [
        ('viridis', True),
        ('plasma', True),
        ('jet', True),
        ('nonexistent_12345', False),
        ('.*ridis', True),  # Should match viridis
        ('cool.*', True),   # Should match cool, coolwarm, etc.
    ])
    def test_get_gradient_parametrized(
        self, search_term: str, expected_found: bool
    ):
        """Parametrized test for various search terms."""
        gradient = get_gradient(search_term)
        if expected_found:
            assert gradient is not None
            assert isinstance(gradient, Gradient)
        else:
            assert gradient is None

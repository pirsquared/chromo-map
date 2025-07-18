"""Integration tests for all Color, Gradient, and Swatch utility functions."""

from chromo_map import Color, Gradient, Swatch


class TestUtilitiesIntegration:
    """Test suite for integrated utilities across all classes."""

    def test_color_gradient_swatch_consistency(self):
        """Test that utilities work consistently across Color, Gradient, and Swatch."""
        # Create test colors
        red = Color('#FF0000')
        green = Color('#00FF00')
        blue = Color('#0000FF')
        
        # Create gradient and swatch
        gradient = Gradient([red, green, blue], name='RGB')
        swatch = Swatch([gradient])
        
        # Test hue adjustment consistency
        adjusted_color = red.adjust_hue(60)
        adjusted_gradient = gradient.adjust_hue(60)
        adjusted_swatch = swatch.adjust_hue(60)
        
        # First color in gradient should match adjusted color
        assert abs(adjusted_color.hsv[0] - adjusted_gradient.colors[0].hsv[0]) < 1e-10
        
        # First color in swatch should match adjusted color
        assert abs(adjusted_color.hsv[0] - adjusted_swatch.gradients[0].colors[0].hsv[0]) < 1e-10

    def test_accessibility_cascade(self):
        """Test accessibility improvements cascade through all classes."""
        # Create light colors that need accessibility improvement
        light_red = Color('#FF9999')
        light_green = Color('#99FF99')
        light_blue = Color('#9999FF')
        
        # Test individual color accessibility
        accessible_red = light_red.find_accessible_version('white', level='AA')
        assert accessible_red.contrast_ratio(Color('#FFFFFF')) >= 4.5
        
        # Test gradient accessibility
        gradient = Gradient([light_red, light_green, light_blue], name='Light')
        accessible_gradient = gradient.make_accessible('white', level='AA')
        
        for color in accessible_gradient.colors:
            assert color.contrast_ratio(Color('#FFFFFF')) >= 4.5
        
        # Test swatch accessibility
        swatch = Swatch([gradient])
        accessible_swatch = swatch.make_accessible('white', level='AA')
        
        for swatch_gradient in accessible_swatch.gradients:
            for color in swatch_gradient.colors:
                assert color.contrast_ratio(Color('#FFFFFF')) >= 4.5

    def test_hsv_utilities_consistency(self):
        """Test HSV utilities work consistently across all classes."""
        # Create test colors
        colors = [Color('#FF0000'), Color('#FFFF00'), Color('#00FF00')]
        
        # Test individual color HSV access
        for color in colors:
            hsv = color.hsv
            hsl = color.hsl
            assert 0 <= hsv[0] <= 360  # Hue
            assert 0 <= hsv[1] <= 1    # Saturation
            assert 0 <= hsv[2] <= 1    # Value
            assert 0 <= hsl[0] <= 360  # Hue
            assert 0 <= hsl[1] <= 1    # Saturation
            assert 0 <= hsl[2] <= 1    # Lightness
        
        # Test gradient HSV consistency
        gradient = Gradient(colors, name='Test')
        adjusted_gradient = gradient.adjust_saturation(0.5)
        
        for i, color in enumerate(adjusted_gradient.colors):
            original_saturation = colors[i].hsv[1]
            expected_saturation = min(original_saturation * 0.5, 1.0)
            assert abs(color.hsv[1] - expected_saturation) < 1e-10
        
        # Test swatch HSV consistency
        swatch = Swatch([gradient])
        adjusted_swatch = swatch.adjust_saturation(0.5)
        
        for swatch_gradient in adjusted_swatch.gradients:
            for i, color in enumerate(swatch_gradient.colors):
                original_saturation = colors[i].hsv[1]
                expected_saturation = min(original_saturation * 0.5, 1.0)
                assert abs(color.hsv[1] - expected_saturation) < 1e-10

    def test_complementary_utilities(self):
        """Test complementary color utilities across all classes."""
        # Create test colors
        red = Color('#FF0000')
        cyan = Color('#00FFFF')
        
        # Test complementary color calculation
        red_comp = red.complementary()
        assert abs(red_comp.hsv[0] - 180.0) < 1e-10  # Red complement should be cyan
        
        # Test gradient complementary
        gradient = Gradient([red, cyan], name='RedCyan')
        comp_gradient = gradient.complementary()
        
        for i, color in enumerate(comp_gradient.colors):
            original_hue = gradient.colors[i].hsv[0]
            expected_hue = (original_hue + 180) % 360
            assert abs(color.hsv[0] - expected_hue) < 1e-10
        
        # Test swatch complementary
        swatch = Swatch([gradient])
        comp_swatch = swatch.complementary()
        
        for swatch_gradient in comp_swatch.gradients:
            for i, color in enumerate(swatch_gradient.colors):
                original_hue = gradient.colors[i].hsv[0]
                expected_hue = (original_hue + 180) % 360
                assert abs(color.hsv[0] - expected_hue) < 1e-10

    def test_contrast_utilities_integration(self):
        """Test contrast utilities integration across all classes."""
        # Create high contrast colors
        black = Color('#000000')
        white = Color('#FFFFFF')
        
        # Test basic contrast ratio
        contrast = black.contrast_ratio(white)
        assert contrast == 21.0  # Maximum contrast
        
        # Test luminance calculation
        assert black.luminance == 0.0
        assert white.luminance == 1.0
        
        # Test gradient contrast analysis
        gradient = Gradient([black, white], name='BlackWhite')
        analysis = gradient.analyze_contrast('white')
        
        assert analysis['max_contrast'] == 21.0
        assert analysis['min_contrast'] == 1.0
        assert analysis['accessible_aa_count'] >= 1
        assert analysis['accessible_aaa_count'] >= 1

    def test_chained_operations_all_classes(self):
        """Test chaining operations across all classes."""
        # Create starting colors
        colors = [Color('#FF6666'), Color('#66FF66'), Color('#6666FF')]
        
        # Test chained color operations
        color = colors[0]
        chained_color = (color
                        .adjust_hue(60)
                        .adjust_saturation(0.8)
                        .adjust_brightness(0.9))
        
        # Verify multiple adjustments were applied
        assert chained_color.hsv[0] == 60.0  # Hue adjusted
        assert chained_color.hsv[1] <= 0.8   # Saturation reduced
        assert chained_color.hsv[2] <= 0.9   # Brightness reduced
        
        # Test chained gradient operations
        gradient = Gradient(colors, name='Test')
        chained_gradient = (gradient
                           .adjust_hue(60)
                           .adjust_saturation(0.8)
                           .adjust_brightness(0.9))
        
        # Verify all colors in gradient were adjusted
        for i, color in enumerate(chained_gradient.colors):
            original_hue = colors[i].hsv[0]
            expected_hue = (original_hue + 60) % 360
            assert abs(color.hsv[0] - expected_hue) < 1e-10
            assert color.hsv[1] <= 0.8
            assert color.hsv[2] <= 0.9
        
        # Test chained swatch operations
        swatch = Swatch([gradient])
        chained_swatch = (swatch
                         .adjust_hue(60)
                         .adjust_saturation(0.8)
                         .adjust_brightness(0.9))
        
        # Verify all colors in swatch were adjusted
        for swatch_gradient in chained_swatch.gradients:
            for i, color in enumerate(swatch_gradient.colors):
                original_hue = colors[i].hsv[0]
                expected_hue = (original_hue + 60) % 360
                assert abs(color.hsv[0] - expected_hue) < 1e-10
                assert color.hsv[1] <= 0.8
                assert color.hsv[2] <= 0.9

    def test_accessibility_levels_all_classes(self):
        """Test accessibility levels work across all classes."""
        # Create medium contrast colors
        medium_colors = [Color('#808080'), Color('#999999'), Color('#AAAAAA')]
        
        # Test AA vs AAA levels for individual colors
        for color in medium_colors:
            aa_version = color.find_accessible_version('white', level='AA')
            aaa_version = color.find_accessible_version('white', level='AAA')
            
            aa_contrast = aa_version.contrast_ratio(Color('#FFFFFF'))
            aaa_contrast = aaa_version.contrast_ratio(Color('#FFFFFF'))
            
            assert aa_contrast >= 4.5
            assert aaa_contrast >= 7.0
        
        # Test gradient accessibility levels
        gradient = Gradient(medium_colors, name='Medium')
        aa_gradient = gradient.make_accessible('white', level='AA')
        aaa_gradient = gradient.make_accessible('white', level='AAA')
        
        white = Color('#FFFFFF')
        for color in aa_gradient.colors:
            assert color.contrast_ratio(white) >= 4.5
        
        for color in aaa_gradient.colors:
            assert color.contrast_ratio(white) >= 7.0

    def test_error_handling_consistency(self):
        """Test error handling is consistent across all classes."""
        # Test with edge case colors
        try:
            # These should not crash
            black = Color('#000000')
            white = Color('#FFFFFF')
            
            # Test extreme adjustments
            extreme_bright = black.adjust_brightness(1000.0)
            extreme_dark = white.adjust_brightness(0.0)
            
            # Should not crash
            assert extreme_bright is not None
            assert extreme_dark is not None
            
            # Test with gradient
            gradient = Gradient([black, white], name='Test')
            extreme_gradient = gradient.adjust_brightness(1000.0)
            assert extreme_gradient is not None
            
            # Test with swatch
            swatch = Swatch([gradient])
            extreme_swatch = swatch.adjust_brightness(1000.0)
            assert extreme_swatch is not None
            
        except Exception as e:
            # If there are exceptions, they should be reasonable
            assert "invalid" in str(e).lower() or "error" in str(e).lower()

    def test_name_propagation(self):
        """Test that names are properly propagated through utilities."""
        # Create named objects
        red = Color('#FF0000')
        gradient = Gradient([red, Color('#FF8080')], name='Red_Gradient')
        swatch = Swatch([gradient])
        
        # Test gradient name propagation
        adjusted_gradient = gradient.adjust_hue(60)
        assert 'Red_Gradient' in adjusted_gradient.name
        assert 'hue+60' in adjusted_gradient.name
        
        # Test swatch name propagation
        adjusted_swatch = swatch.adjust_hue(60)
        assert 'Red_Gradient' in adjusted_swatch.gradients[0].name
        assert 'hue+60' in adjusted_swatch.gradients[0].name
        
        # Test accessibility name propagation
        accessible_gradient = gradient.make_accessible('white', level='AA')
        assert 'Red_Gradient' in accessible_gradient.name
        assert 'accessible' in accessible_gradient.name

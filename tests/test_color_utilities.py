"""Tests for Color HSV, scaling, accessible, and contrast utilities."""

from chromo_map import Color, find_accessible_color


class TestColorHSVUtilities:
    """Test suite for Color HSV/HSL utilities."""

    def test_color_hsv_property(self):
        """Test HSV property returns correct values."""
        # Test primary colors
        red = Color("#FF0000")
        hsv = red.hsv
        assert hsv[0] == 0.0  # Hue
        assert hsv[1] == 1.0  # Saturation
        assert hsv[2] == 1.0  # Value

        # Test green
        green = Color("#00FF00")
        hsv = green.hsv
        assert hsv[0] == 120.0  # Hue
        assert hsv[1] == 1.0  # Saturation
        assert hsv[2] == 1.0  # Value

        # Test blue
        blue = Color("#0000FF")
        hsv = blue.hsv
        assert hsv[0] == 240.0  # Hue
        assert hsv[1] == 1.0  # Saturation
        assert hsv[2] == 1.0  # Value

    def test_color_hsl_property(self):
        """Test HSL property returns correct values."""
        # Test primary colors
        red = Color("#FF0000")
        hsl = red.hsl
        assert hsl[0] == 0.0  # Hue
        assert hsl[1] == 1.0  # Saturation
        assert hsl[2] == 0.5  # Lightness

        # Test white
        white = Color("#FFFFFF")
        hsl = white.hsl
        assert hsl[0] == 0.0  # Hue (undefined for white)
        assert hsl[1] == 0.0  # Saturation
        assert hsl[2] == 1.0  # Lightness

        # Test black
        black = Color("#000000")
        hsl = black.hsl
        assert hsl[0] == 0.0  # Hue
        assert hsl[1] == 0.0  # Saturation
        assert hsl[2] == 0.0  # Lightness

    def test_color_luminance(self):
        """Test luminance calculation."""
        # Test white (maximum luminance)
        white = Color("#FFFFFF")
        assert white.luminance == 1.0

        # Test black (minimum luminance)
        black = Color("#000000")
        assert black.luminance == 0.0

        # Test gray (mid-range luminance)
        gray = Color("#808080")
        luminance = gray.luminance
        assert 0.0 < luminance < 1.0


class TestColorScalingUtilities:
    """Test suite for Color scaling utilities."""

    def test_adjust_hue(self):
        """Test hue adjustment."""
        red = Color("#FF0000")  # Hue = 0

        # Rotate by 120 degrees (should become green)
        green_shifted = red.adjust_hue(120)
        assert green_shifted.hsv[0] == 120.0

        # Rotate by 240 degrees (should become blue)
        blue_shifted = red.adjust_hue(240)
        assert blue_shifted.hsv[0] == 240.0

        # Rotate by 360 degrees (should return to red)
        red_shifted = red.adjust_hue(360)
        assert abs(red_shifted.hsv[0] - 0.0) < 1e-10

    def test_adjust_saturation(self):
        """Test saturation adjustment."""
        red = Color("#FF0000")  # Full saturation

        # Reduce saturation by half
        desaturated = red.adjust_saturation(0.5)
        assert desaturated.hsv[1] == 0.5

        # Increase saturation (should cap at 1.0)
        oversaturated = red.adjust_saturation(2.0)
        assert oversaturated.hsv[1] == 1.0

        # Zero saturation (should become gray)
        gray = red.adjust_saturation(0.0)
        assert gray.hsv[1] == 0.0

    def test_adjust_brightness(self):
        """Test brightness/value adjustment."""
        red = Color("#FF0000")  # Full brightness

        # Reduce brightness by half
        darker = red.adjust_brightness(0.5)
        assert darker.hsv[2] == 0.5

        # Increase brightness (should cap at 1.0)
        brighter = red.adjust_brightness(2.0)
        assert brighter.hsv[2] == 1.0

        # Zero brightness (should become black)
        black = red.adjust_brightness(0.0)
        assert black.hsv[2] == 0.0

    def test_adjust_lightness(self):
        """Test lightness adjustment."""
        red = Color("#FF0000")  # Lightness = 0.5

        # Increase lightness
        lighter = red.adjust_lightness(1.5)
        assert lighter.hsl[2] == 0.75

        # Decrease lightness
        darker = red.adjust_lightness(0.5)
        assert darker.hsl[2] == 0.25

        # Maximum lightness (should become white)
        white = red.adjust_lightness(2.0)
        assert white.hsl[2] == 1.0

    def test_complementary(self):
        """Test complementary color generation."""
        red = Color("#FF0000")
        complementary = red.complementary()

        # Complementary should be 180 degrees apart
        hue_diff = abs(complementary.hsv[0] - red.hsv[0])
        assert abs(hue_diff - 180.0) < 1e-10

        # Test with different colors
        green = Color("#00FF00")
        comp_green = green.complementary()
        assert abs(comp_green.hsv[0] - 300.0) < 1e-10  # 120 + 180 = 300


class TestColorContrastUtilities:
    """Test suite for Color contrast utilities."""

    def test_contrast_ratio_basic(self):
        """Test basic contrast ratio calculation."""
        white = Color("#FFFFFF")
        black = Color("#000000")

        # Maximum contrast ratio
        contrast = white.contrast_ratio(black)
        assert contrast == 21.0

        # Same color should have ratio of 1.0
        white_contrast = white.contrast_ratio(white)
        assert white_contrast == 1.0

        # Symmetric property
        reverse_contrast = black.contrast_ratio(white)
        assert reverse_contrast == 21.0

    def test_contrast_ratio_intermediate(self):
        """Test contrast ratio with intermediate colors."""
        red = Color("#FF0000")
        blue = Color("#0000FF")

        contrast = red.contrast_ratio(blue)
        assert 1.0 < contrast < 21.0

        # Test with gray
        gray = Color("#808080")
        white = Color("#FFFFFF")

        gray_contrast = white.contrast_ratio(gray)
        assert 1.0 < gray_contrast < 21.0

    def test_contrast_ratio_edge_cases(self):
        """Test contrast ratio edge cases."""
        # Very similar colors
        color1 = Color("#FF0000")
        color2 = Color("#FE0000")

        contrast = color1.contrast_ratio(color2)
        assert 1.0 <= contrast <= 2.0

        # Colors with alpha (should use RGB values)
        alpha_color = Color("#FF000080")  # Red with 50% alpha
        red = Color("#FF0000")

        # Note: contrast calculation typically ignores alpha
        contrast = alpha_color.contrast_ratio(red)
        assert contrast == 1.0


class TestColorAccessibilityUtilities:
    """Test suite for Color accessibility utilities."""

    def test_find_accessible_version_aa(self):
        """Test finding accessible version with AA compliance."""
        # Light color on white background
        light_red = Color("#FFCCCC")
        white = Color("#FFFFFF")

        accessible = light_red.find_accessible_version(white, level="AA")
        contrast = accessible.contrast_ratio(white)
        assert contrast >= 4.5  # AA requirement

        # Should be darker than original
        assert accessible.luminance < light_red.luminance

    def test_find_accessible_version_aaa(self):
        """Test finding accessible version with AAA compliance."""
        light_blue = Color("#CCCCFF")
        white = Color("#FFFFFF")

        accessible = light_blue.find_accessible_version(white, level="AAA")
        contrast = accessible.contrast_ratio(white)
        assert contrast >= 7.0  # AAA requirement

    def test_find_accessible_version_dark_background(self):
        """Test accessibility against dark background."""
        dark_red = Color("#330000")
        black = Color("#000000")

        accessible = dark_red.find_accessible_version(black, level="AA")
        contrast = accessible.contrast_ratio(black)
        assert contrast >= 4.5

        # Should be lighter than original
        assert accessible.luminance > dark_red.luminance

    def test_maximize_contrast_iterative(self):
        """Test iterative contrast maximization."""
        red = Color("#FF6666")
        white = Color("#FFFFFF")

        maximized = red.maximize_contrast_iterative(white, level="AA")
        contrast = maximized.contrast_ratio(white)
        assert contrast >= 4.5

        # Should be more contrasted than original
        original_contrast = red.contrast_ratio(white)
        assert contrast >= original_contrast

    def test_maximize_contrast_binary_search(self):
        """Test binary search contrast maximization."""
        blue = Color("#6666FF")
        white = Color("#FFFFFF")

        maximized = blue.maximize_contrast_binary_search(white, level="AA")
        contrast = maximized.contrast_ratio(white)
        assert contrast >= 4.5

        # Should maintain hue
        assert abs(maximized.hsv[0] - blue.hsv[0]) < 1e-10

    def test_maximize_contrast_optimization(self):
        """Test optimization-based contrast maximization."""
        green = Color("#66FF66")
        black = Color("#000000")

        maximized = green.maximize_contrast_optimization(black, level="AA")
        contrast = maximized.contrast_ratio(black)
        assert contrast >= 4.5

    def test_find_accessible_color_function(self):
        """Test standalone find_accessible_color function."""
        base_color = Color("#FFCCCC")
        target_color = Color("#FFFFFF")

        accessible = find_accessible_color(base_color, target_color, level="AA")
        contrast = accessible.contrast_ratio(target_color)
        assert contrast >= 4.5

    def test_accessibility_with_different_levels(self):
        """Test accessibility with different compliance levels."""
        color = Color("#808080")
        background = Color("#FFFFFF")

        # AA level
        aa_accessible = color.find_accessible_version(background, level="AA")
        aa_contrast = aa_accessible.contrast_ratio(background)
        assert aa_contrast >= 4.5

        # AAA level
        aaa_accessible = color.find_accessible_version(background, level="AAA")
        aaa_contrast = aaa_accessible.contrast_ratio(background)
        assert aaa_contrast >= 7.0

        # AAA should be more contrasted than AA
        assert aaa_contrast >= aa_contrast


class TestColorUtilitiesIntegration:
    """Test suite for integrated Color utilities."""

    def test_hue_adjustment_preserves_saturation_brightness(self):
        """Test that hue adjustment preserves saturation and brightness."""
        original = Color("#FF8000")  # Orange
        adjusted = original.adjust_hue(60)  # Shift hue

        # Saturation and brightness should be preserved
        assert abs(adjusted.hsv[1] - original.hsv[1]) < 1e-10
        assert abs(adjusted.hsv[2] - original.hsv[2]) < 1e-10

    def test_saturation_adjustment_preserves_hue_brightness(self):
        """Test that saturation adjustment preserves hue and brightness."""
        original = Color("#FF8000")  # Orange
        adjusted = original.adjust_saturation(0.5)

        # Hue and brightness should be preserved
        assert abs(adjusted.hsv[0] - original.hsv[0]) < 1e-10
        assert abs(adjusted.hsv[2] - original.hsv[2]) < 1e-10

    def test_brightness_adjustment_preserves_hue_saturation(self):
        """Test that brightness adjustment preserves hue and saturation."""
        original = Color("#FF8000")  # Orange
        adjusted = original.adjust_brightness(0.5)

        # Hue and saturation should be preserved
        assert abs(adjusted.hsv[0] - original.hsv[0]) < 1e-10
        assert abs(adjusted.hsv[1] - original.hsv[1]) < 1e-10

    def test_chained_adjustments(self):
        """Test chaining multiple adjustments."""
        original = Color("#FF0000")

        # Chain multiple adjustments
        adjusted = original.adjust_hue(60).adjust_saturation(0.8).adjust_brightness(0.9)

        # Verify final values
        hsv = adjusted.hsv
        assert hsv[0] == 60.0
        assert hsv[1] == 0.8
        assert hsv[2] == 0.9

    def test_accessibility_preserves_hue(self):
        """Test that accessibility adjustments preserve hue."""
        original = Color("#FF6666")  # Light red
        white = Color("#FFFFFF")

        accessible = original.find_accessible_version(white, level="AA")

        # Hue should be preserved
        assert abs(accessible.hsv[0] - original.hsv[0]) < 1e-10

    def test_complementary_accessibility(self):
        """Test accessibility of complementary colors."""
        color = Color("#FF0000")
        complement = color.complementary()

        # Test contrast between color and complement
        contrast = color.contrast_ratio(complement)
        assert contrast > 1.0  # Should have some contrast

        # Make complement accessible against white
        white = Color("#FFFFFF")
        accessible_complement = complement.find_accessible_version(white, level="AA")
        final_contrast = accessible_complement.contrast_ratio(white)
        assert final_contrast >= 4.5

    def test_round_trip_conversions(self):
        """Test that color adjustments can be reversed."""
        original = Color("#FF8000")

        # Adjust hue and reverse
        adjusted = original.adjust_hue(60)
        reversed_color = adjusted.adjust_hue(-60)

        # Should be approximately equal (within floating point precision)
        assert abs(reversed_color.hsv[0] - original.hsv[0]) < 1e-10

    def test_extreme_values(self):
        """Test utilities with extreme values."""
        # Test with very dark color
        dark = Color("#010101")
        bright_adjusted = dark.adjust_brightness(10.0)  # Should multiply brightness

        # Brightness should be multiplied by 10, but original is very low
        original_brightness = dark.hsv[2]
        expected_brightness = min(original_brightness * 10.0, 1.0)
        assert abs(bright_adjusted.hsv[2] - expected_brightness) < 1e-10

        # Test with very bright color
        bright = Color("#FEFEFE")
        dark_adjusted = bright.adjust_brightness(0.1)
        original_brightness = bright.hsv[2]
        expected_brightness = max(original_brightness * 0.1, 0.0)
        assert abs(dark_adjusted.hsv[2] - expected_brightness) < 1e-10

        # Test hue wrapping
        red = Color("#FF0000")
        wrapped = red.adjust_hue(720)  # Two full rotations
        assert abs(wrapped.hsv[0] - 0.0) < 1e-10

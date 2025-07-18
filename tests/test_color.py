"""
This module contains test functions to be used with the pytest framework.
"""

import pytest

import chromo_map as cm
from chromo_map import Color, Gradient


# pylint: disable=protected-access
# pylint: disable=broad-exception-caught
# pylint: disable=missing-function-docstring
def test_colormaps():
    """Test colormap catalog system."""
    try:
        # Test the new unified catalog structure
        assert "matplotlib" in cm.cmaps
        assert "plotly" in cm.cmaps
        assert "palettable" in cm.cmaps
        assert "all" in cm.cmaps

        # Test basic access
        _ = len(cm.cmaps.all)  # Should have some colormaps

        # Test matplotlib access
        if hasattr(cm.cmaps.matplotlib, "PerceptuallyUniformSequential"):
            _ = cm.cmaps.matplotlib.PerceptuallyUniformSequential.viridis

        # Test unified access
        if hasattr(cm.cmaps.all, "viridis"):
            _ = cm.cmaps.all.viridis

    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover

    # Basic validation that our catalog structure works
    assert isinstance(cm.cmaps, cm.AttrDict)
    assert len(cm.cmaps.all) > 0  # Should have some colormaps


@pytest.mark.parametrize(
    "clr, alpha",
    [
        ("red", None),
        ("red", 1),
        ("red", 1.0),
        ("#f00", 1),
        ("#f00f", None),
        ("#ff0000", 1),
        ("#ff0000ff", None),
        ("rgb(255, 0, 0)", 1),
        ("rgb(255, 0, 0, 1)", None),
        ((1, 0, 0), 1),
        ((1, 0, 0, 1), None),
    ],
)
def test_color_01(clr, alpha):
    """Test Color class."""
    c = Color(clr, alpha)
    assert c.hex == "#ff0000"
    assert c.hexa == "#ff0000ff"
    assert c.rgbtup == (255, 0, 0)
    assert c.rgbatup == (255, 0, 0, 1.0)
    assert c.rgb == "rgb(255, 0, 0)"
    assert c.rgba == "rgba(255, 0, 0, 1.0)"
    assert c.tup == (1.0, 0.0, 0.0, 1.0)


@pytest.mark.parametrize(
    "clr, alpha",
    [
        ("red", 0.5),
        ("#f00", 0.5),
        ("#ff0000", 0.5),
        ("#ff0000af", 0.5),
        ("rgb(255, 0, 0)", 0.5),
        ("rgb(255, 0, 0, 0.5)", None),
        ("rgb(255, 0, 0, 0.15)", 0.5),
        ((1, 0, 0), 0.5),
        ((1, 0, 0, 0.5), None),
    ],
)
def test_color_02(clr, alpha):
    """Test Color class."""
    c = Color(clr, alpha)
    assert c.hex == "#ff0000"
    assert c.hexa == "#ff00007f"
    assert c.rgbtup == (255, 0, 0)
    assert c.rgbatup == (255, 0, 0, 0.5)
    assert c.rgb == "rgb(255, 0, 0)"
    assert c.rgba == "rgba(255, 0, 0, 0.5)"
    assert c.tup == (1.0, 0.0, 0.0, 0.5)


@pytest.mark.parametrize(
    "clr, alpha",
    [
        ("#0f0", 0.5),
        ("#00ff00", 0.5),
        ("#00ff00af", 0.5),
        ("rgb(0, 255, 0)", 0.5),
        ("rgb(0, 255, 0, 0.5)", None),
        ("rgb(0, 255, 0, 0.15)", 0.5),
        ((0, 1, 0), 0.5),
        ((0, 1, 0, 0.5), None),
    ],
)
def test_color_03(clr, alpha):
    """Test Color class."""
    c = Color(clr, alpha)
    assert c.hex == "#00ff00"
    assert c.hexa == "#00ff007f"
    assert c.rgbtup == (0, 255, 0)
    assert c.rgbatup == (0, 255, 0, 0.5)
    assert c.rgb == "rgb(0, 255, 0)"
    assert c.rgba == "rgba(0, 255, 0, 0.5)"
    assert c.tup == (0.0, 1.0, 0.0, 0.5)


def test_color_04():
    with pytest.raises(ValueError, match="Invalid color input."):
        Color("not going to match")


def test_color_05():
    with pytest.raises(ValueError, match="Invalid color input 'dict'."):
        Color({})


def test_color_06():
    with pytest.raises(ValueError, match="Color values must be between 0 and 1."):
        Color((1.1, 0, 0))


def test_color_html_01():
    c = Color("#f00")
    try:
        _ = c._repr_html_()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover
    else:
        assert True


def test_color_or_01():
    r = Color("#f00")
    g = Color("#0f0")
    c = r | g
    assert c.hex == "#7f7f00"


def test_gradient_01():
    g = Gradient(["#f00", "#00f"]).resize(3)
    c = Color(g(0.5))
    assert c.hex == "#7f007f"


def test_gradient_02():
    g = Gradient(["#f00", "#00f"])
    c = g[0.5]
    assert c.hex == "#7f007f"


def test_gradient_03():
    # Use matplotlib viridis which should be available
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = Gradient("viridis", "viridis")
    assert grad1 == grad2


def test_gradient_04():
    # Test with alpha modification
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis.with_alpha(0.5)
    grad2 = Gradient("viridis", "viridis", alpha=0.5)
    assert grad1 == grad2


def test_gradient_05():
    # Use matplotlib colormap instead of palettable
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = Gradient("viridis", "viridis")
    grad3 = Gradient("viridis")
    assert grad1 == grad2
    assert grad2 == grad3


def test_gradient_06():
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis.with_alpha(0.5)
    grad2 = Gradient("viridis", "viridis", alpha=0.5)
    assert grad1 == grad2


def test_gradient_07():
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = grad1.resize(grad1.N * 2 - 1)
    clrs = grad2.colors[::2]
    grad3 = Gradient(clrs, "BuGn_9")
    assert grad1 == grad3


def test_gradient_08():
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = grad1.resize(grad1.N * 2 - 1)
    clrs = grad2.colors[1::2]
    grad3 = Gradient(clrs, "viridis")
    grad4 = grad1[cm.np.linspace(0, 1, grad1.N * 2 - 1)[1::2]]
    assert grad3 == grad4


def test_gradient_09():
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = grad1 * 2
    grad3 = grad1 + grad1
    grad4 = Gradient(grad1.colors + grad1.colors, "viridis")
    grad5 = 2 * grad1
    assert grad2 == grad3
    assert grad2 == grad4
    assert grad2 == grad5
    with pytest.raises(ValueError, match="Invalid multiplication."):
        _ = grad1 * "one"


def test_gradient_10():
    grad1 = cm.cmaps.matplotlib.miscellaneous.viridis
    grad2 = grad1 / 2
    grad3 = grad1.resize(grad1.N * 2)
    assert grad2 == grad3
    with pytest.raises(ValueError, match="Invalid division."):
        _ = grad1 / "one"


def test_gradient_11():
    with pytest.raises(ValueError, match="No valid colors found."):
        Gradient([])


def test_gradient_12():
    lc = cm.plt.get_cmap("Accent")
    grad1 = Gradient(lc, "Accent")
    grad2 = cm.cmaps.matplotlib.qualitative.Accent
    assert grad1 == grad2


def test_gradient_13():
    data = {
        "red": [(0, 1, 1), (0.5, 1, 0), (1, 0, 0)],
        "green": [(0, 0, 0), (1, 0, 0)],
        "blue": [(0, 0, 0), (0.5, 0, 1), (1, 1, 1)],
    }
    cmap = cm.LSC("custom", data)
    grad1 = Gradient(cmap)
    grad2 = Gradient(data, "custom")
    assert grad1 == grad2


def test_gradient_14():
    with pytest.raises(AttributeError, match="'Gradient' object has no attribute 'x'"):
        _ = cm.cmaps.matplotlib.miscellaneous.viridis.x


def test_gradient_15():
    grad = Gradient(["#f00", "#00f"])
    assert grad[0] == Color("#f00")
    with pytest.raises(IndexError, match="Invalid index: 3"):
        _ = grad[3]


def test_gradient_16():
    grad = Gradient(["#f00", "#00f"])
    clrs = list(grad)
    assert clrs[0] == Color("#f00")
    assert clrs[1] == Color("#00f")


def test_gradient_17():
    grad1 = Gradient(["#f00", "#00f"])
    grad2 = Gradient(["#00f", "#f00"])
    assert grad1._r == grad2


def test_gradient_18():
    grad1 = Gradient(["#f00", "#00f"])
    grad2 = Gradient(["#00f", "#f00"])
    grad3 = grad1 | grad2
    assert grad3[0].tup == (0.5, 0, 0.5, 1)


def test_gradient_to_div():
    grad1 = Gradient(["#f00", "#00f"]).resize(10)
    try:
        _ = grad1.to_div()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover
    try:
        _ = grad1.to_div(maxn=5)
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover
    try:
        grad1.colors = tuple()
        _ = grad1.to_div()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover


def test_gradient_to_drawing():
    grad1 = Gradient(["#f00", "#00f"]).resize(10)
    try:
        _ = grad1.to_drawing()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover


@pytest.fixture(autouse=True)
def no_show(monkeypatch):
    monkeypatch.setattr(cm.plt, "show", lambda: None)


def test_gradient_to_matplotlib():
    grad1 = Gradient(["#f00", "#00f"]).resize(10)
    try:
        grad1.to_matplotlib()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover


def test_gradient_repr_html_():
    grad1 = Gradient(["#f00", "#00f"]).resize(10)
    try:
        _ = grad1._repr_html_()
        _ = grad1._repr_html_(skip_super=True)
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover


def test_gradient_to_png():
    grad1 = Gradient(["#f00", "#00f"]).resize(10)
    try:
        _ = grad1.to_png()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover


def test_swatch_01():
    grad = Gradient(["red", "blue"])
    swatch1 = cm.Swatch({f"{i}": grad.resize(i) for i in range(3, 10)})
    swatch2 = swatch1.with_max(5)
    assert len(swatch1) == len(list(swatch1))
    assert swatch2.maxn == 5
    swatch2.maps = []
    try:
        _ = swatch1._repr_html_()
        _ = swatch2._repr_html_()
    except Exception as e:  # pragma: no cover
        pytest.fail(f"Unexpected exception: {e}")  # pragma: no cover
    with pytest.raises(ValueError, match="Invalid color input 'int'."):
        _ = cm.Swatch({"one": [1]})


@pytest.mark.parametrize(
    "func_name, input1, expected",
    [
        ("rgba_to_tup", "not going to match", "None"),
        ("rgba_to_tup", "rgb(255, 0, 0)", "(1, 0, 0, 1)"),
        ("rgba_to_tup", "rgba(255, 0, 0, 1)", "(1, 0, 0, 1)"),
        ("rgba_to_tup", "rgba(255, 0, 0, 0.5)", "(1, 0, 0, 0.5)"),
        ("rgba_to_tup", "rgba(255, 0, 0, .5)", "(1, 0, 0, 0.5)"),
        ("rgba_to_tup", "rgb(0, 255, 0)", "(0, 1, 0, 1)"),
        ("rgba_to_tup", "rgba(0, 255, 0, 1)", "(0, 1, 0, 1)"),
        ("rgba_to_tup", "rgba(0, 255, 0, 0.5)", "(0, 1, 0, 0.5)"),
        ("rgba_to_tup", "rgba(0, 255, 0, .5)", "(0, 1, 0, 0.5)"),
        ("rgba_to_tup", "rgb(0, 0, 255)", "(0, 0, 1, 1)"),
        ("rgba_to_tup", "rgba(0, 0, 255, 1)", "(0, 0, 1, 1)"),
        ("rgba_to_tup", "rgba(0, 0, 255, 0.5)", "(0, 0, 1, 0.5)"),
        ("rgba_to_tup", "rgba(0, 0, 255, .5)", "(0, 0, 1, 0.5)"),
        ("rgba_to_tup", "rgba(127, 127, 127, 0.5)", "(127/255, 127/255, 127/255, 0.5)"),
        ("hexstr_to_tup", "not going to match", "None"),
        ("hexstr_to_tup", "#f00", "(1, 0, 0, 1)"),
        ("hexstr_to_tup", "#f00f", "(1, 0, 0, 1)"),
        ("hexstr_to_tup", "#ff0000", "(1, 0, 0, 1)"),
        ("hexstr_to_tup", "#ff0000ff", "(1, 0, 0, 1)"),
        ("hexstr_to_tup", "#ff00007f", "(1, 0, 0, 127/255)"),
        ("hexstr_to_tup", "#0f0", "(0, 1, 0, 1)"),
        ("hexstr_to_tup", "#0f0f", "(0, 1, 0, 1)"),
        ("hexstr_to_tup", "#00ff00", "(0, 1, 0, 1)"),
        ("hexstr_to_tup", "#00ff00ff", "(0, 1, 0, 1)"),
        ("hexstr_to_tup", "#00f", "(0, 0, 1, 1)"),
        ("hexstr_to_tup", "#00ff", "(0, 0, 1, 1)"),
        ("hexstr_to_tup", "#0000ff", "(0, 0, 1, 1)"),
        ("hexstr_to_tup", "#0000ffff", "(0, 0, 1, 1)"),
        ("hexstr_to_tup", "#7f7f00", "(127/255, 127/255, 0, 1)"),
        ("clr_to_tup", "not going to match", "None"),
        ("clr_to_tup", "rgb(255, 0, 0)", "(1, 0, 0, 1)"),
        ("clr_to_tup", "rgba(255, 0, 0, 1)", "(1, 0, 0, 1)"),
        ("clr_to_tup", "rgba(255, 0, 0, 0.5)", "(1, 0, 0, 0.5)"),
        ("clr_to_tup", "rgba(255, 0, 0, .5)", "(1, 0, 0, 0.5)"),
        ("clr_to_tup", "rgb(0, 255, 0)", "(0, 1, 0, 1)"),
        ("clr_to_tup", "rgba(0, 255, 0, 1)", "(0, 1, 0, 1)"),
        ("clr_to_tup", "rgba(0, 255, 0, 0.5)", "(0, 1, 0, 0.5)"),
        ("clr_to_tup", "rgba(0, 255, 0, .5)", "(0, 1, 0, 0.5)"),
        ("clr_to_tup", "rgb(0, 0, 255)", "(0, 0, 1, 1)"),
        ("clr_to_tup", "rgba(0, 0, 255, 1)", "(0, 0, 1, 1)"),
        ("clr_to_tup", "rgba(0, 0, 255, 0.5)", "(0, 0, 1, 0.5)"),
        ("clr_to_tup", "rgba(0, 0, 255, .5)", "(0, 0, 1, 0.5)"),
        ("clr_to_tup", "rgba(127, 127, 127, 0.5)", "(127/255, 127/255, 127/255, 0.5)"),
        ("clr_to_tup", "not going to match", "None"),
        ("clr_to_tup", "#f00", "(1, 0, 0, 1)"),
        ("clr_to_tup", "#f00f", "(1, 0, 0, 1)"),
        ("clr_to_tup", "#ff0000", "(1, 0, 0, 1)"),
        ("clr_to_tup", "#ff0000ff", "(1, 0, 0, 1)"),
        ("clr_to_tup", "#ff00007f", "(1, 0, 0, 127/255)"),
        ("clr_to_tup", "#0f0", "(0, 1, 0, 1)"),
        ("clr_to_tup", "#0f0f", "(0, 1, 0, 1)"),
        ("clr_to_tup", "#00ff00", "(0, 1, 0, 1)"),
        ("clr_to_tup", "#00ff00ff", "(0, 1, 0, 1)"),
        ("clr_to_tup", "#00f", "(0, 0, 1, 1)"),
        ("clr_to_tup", "#00ff", "(0, 0, 1, 1)"),
        ("clr_to_tup", "#0000ff", "(0, 0, 1, 1)"),
        ("clr_to_tup", "#0000ffff", "(0, 0, 1, 1)"),
        ("clr_to_tup", "#7f7f00", "(127/255, 127/255, 0, 1)"),
        ("clr_to_tup", (1, 2, 3), "(1, 2, 3)"),
        ("clr_to_tup", [1, 2, 3, 4, 5], "[1, 2, 3, 4, 5]"),
        ("clr_to_tup", "red", "(1, 0, 0, 1)"),
        ("clr_to_tup", "green", "(0, 128/255, 0, 1)"),
        ("clr_to_tup", "blue", "(0, 0, 1, 1)"),
        ("clr_to_tup", "xkcd:sky blue", "(117/255, 187/255, 253/255, 1)"),
        ("clr_to_tup", {"nonsense": 1}, "None"),
    ],
)
# pylint: disable=eval-used
def test_funcs_01(func_name, input1, expected):
    """Test color functions."""
    func = getattr(cm, func_name)
    if isinstance(expected, str):
        expected = eval(expected)
    assert func(input1) == expected


def test_rgba_to_tup_exception():
    with pytest.raises(ValueError, match="Alpha must be between 0 and 1."):
        cm.rgba_to_tup("rgba(255, 0, 0, 1.5)")

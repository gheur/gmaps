
import ipywidgets as widgets
from traitlets import Unicode, Int, default, List, observe

import gmaps.geotraitlets as geotraitlets
import gmaps.bounds as bounds

from .maps import DEFAULT_CENTER

__all__ = ["Symbol", "Marker", "Markers"]


class Symbol(widgets.Widget):
    """
    Class representing a single symbol.

    Symbols are like markers, but the point is represented by
    an SVG symbol, rather than the default inverted droplet.
    Symbols should be added to the map via the 'Markers'
    widget.
    """
    has_bounds = False
    _view_name = Unicode("SymbolView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("SymbolModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    location = geotraitlets.Point(DEFAULT_CENTER).tag(sync=True)
    fill_color = geotraitlets.ColorAlpha().tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha().tag(sync=True)
    scale = Int(default_value=5, min=0, max=20).tag(sync=True)
    hover_text = Unicode("").tag(sync=True)

    @default("fill_color")
    def _default_fill_color(self):
        return "black"

    @default("stroke_color")
    def _default_stroke_color(self):
        return "black"


class Marker(widgets.Widget):
    """
    Class representing a marker.

    Markers should be added to the map via the 'Markers'
    widget.
    """
    has_bounds = False
    _view_name = Unicode("MarkerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("MarkerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    location = geotraitlets.Point(DEFAULT_CENTER).tag(sync=True)
    label = Unicode("").tag(sync=True)
    hover_text = Unicode("").tag(sync=True)


class Markers(widgets.Widget):
    has_bounds = True
    _view_name = Unicode("MarkerLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("MarkerLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    markers = List(minlen=1).tag(sync=True,  **widgets.widget_serialization)
    data_bounds = List().tag(sync=True)

    @observe("markers")
    def _calc_bounds(self, change):
        markers = change["new"]
        locations = [marker.location for marker in markers]
        latitudes = [location[0] for location in locations]
        longitudes = [location[1] for location in locations]
        min_latitude, max_latitude = bounds.latitude_bounds(latitudes)
        min_longitude, max_longitude = bounds.longitude_bounds(longitudes)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]

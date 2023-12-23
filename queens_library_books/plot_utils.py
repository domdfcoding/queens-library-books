#!/usr/bin/env python3
#
#  plot_utils.py
"""
utilities for Leaflet/Folium.
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Dict, Mapping, Sequence, Tuple

# 3rd party
import folium  # type: ignore[import]
from shapely.geometry import Polygon, mapping  # type: ignore[import]

# this package
from queens_library_books.utils import get_url_for_library

__all__ = ("make_markers", "merge_geometry")


def make_markers(
		library: str,
		book: str,
		book_count: int,
		location: Sequence[float],
		colour: str,
		) -> Tuple[folium.CircleMarker, folium.Marker]:
	"""
	Create markers for a library.

	:param library: The library name.
	:param book: The book name.
	:param book_count: The total number of libraries where this was the most popular book, including this library.
	:param location: The library's coordinates.
	:param color: Marker colour.
	"""

	popup_book_name = book.split(" – ")

	circle_marker = folium.CircleMarker(location=location, radius=5, weight=20, color=colour)

	text_html = f"<div style='display: flex; justify-content: center; align-items: center; font-size: 20pt'>{book_count}</div>"
	popup_html = f"<h3><a href='{get_url_for_library(library)}' target='_blank'>{library}</a></h3><h4>{popup_book_name[0]}</h4><h5>{popup_book_name[1]}</h5>Most popular book at {book_count} libraries"

	text_marker = folium.Marker(
			location=location,
			icon=folium.DivIcon(icon_size=(20, 20), icon_anchor=(10, 20), html=text_html),
			tooltip=f"<b>{library}</b><br>{book}",
			popup=folium.Popup(popup_html, min_width=210, max_width=210),
			)

	return circle_marker, text_marker


def merge_geometry(geojson: Mapping) -> Dict:
	"""
	Combine multiple polygons (for e.g. islands or discontinuous areas).

	:param geojson: Input geoJSON data.

	:returns: geoJSON FeatureCollection
	"""

	geometry = geojson["features"][0]["geometry"]["coordinates"]

	# Combine multiple polygons (for e.g. islands or discontinuous areas)
	polygon_1 = Polygon([(coor[0], coor[1]) for coor in geometry[0][0]])

	for coordinates in geometry[1:]:
		new_polygon = Polygon([(coor[0], coor[1]) for coor in coordinates[0]])
		polygon_1 = polygon_1.union(new_polygon)

	# Polygon to cover the whole world
	polygon_2 = Polygon([[0, 90], [180, 90], [180, -90], [0, -90], [-180, -90], [-180, 0], [-180, 90], [0, 90]])

	new_geometry = mapping(polygon_2.difference(polygon_1))

	new_feature = dict(
			type="Feature",
			id='',
			properties=dict(Name=''),
			geometry=dict(type=new_geometry["type"], coordinates=new_geometry["coordinates"]),
			)

	return dict(type="FeatureCollection", features=[new_feature])

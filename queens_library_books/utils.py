#!/usr/bin/env python3
#
#  utils.py
"""
General utilities.
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
from typing import Dict

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

__all__ = ("get_url_for_library", "load_geojson_for_borough")


def get_url_for_library(library: str) -> str:
	"""
	Returns the URL for the library's page on the Queens Public Library website.

	:param library:
	"""

	library_id = library.lower().replace(' ', '-')
	return f"https://www.queenslibrary.org/about-us/locations/{library_id}"


def load_geojson_for_borough(boundaries_datafile: PathLike, borough_name: str) -> Dict:
	"""
	Get geoJSON for just one borough.

	:param boundaries_datafile: Path to the datafile containing New York borough boundaries.
	:param borough_name:
	"""

	geojson_data = PathPlus(boundaries_datafile).load_json()
	geojson_data["features"] = [
			f for f in geojson_data["features"] if f["properties"]["boro_name"] == borough_name
			]
	return geojson_data

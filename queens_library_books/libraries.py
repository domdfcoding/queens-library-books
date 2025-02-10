#!/usr/bin/env python3
#
#  libraries.py
"""
Functions to parse library locations from Wikipedia.
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
from typing import Dict, Optional, Tuple

# 3rd party
import bs4
import httpx

__all__ = ("get_queens_library_locations", )


def _get_queens_library_street_addresses() -> Dict[str, str]:
	"""
	Download and parse the list of library locations from Wikipedia.

	:returns: A mapping of library name to street address.
	"""

	locations_url = "https://en.wikipedia.org/wiki/List_of_Queens_Public_Library_branches"
	locations_response = httpx.get(locations_url)

	locations_soup = bs4.BeautifulSoup(locations_response.text, "html.parser")
	locations_table = locations_soup.find("table", {"class": "wikitable"})
	assert locations_table is not None

	libraries = {}
	for row in locations_table.find_all("tr")[1:]:  # type: ignore[attr-defined]
		row_elems = row.find_all("td")
		library = row_elems[1].get_text().strip()
		libraries[library] = list(row_elems[3].children)[0].strip()

	return libraries


def _get_coords_from_address(address: str, fallback_settlement: Optional[str] = None) -> Tuple[str, str]:
	"""
	Get coordinates for an address from OpenStreetMap.
	"""

	# mypy seems not to know the correct signature; https://github.com/python/mypy/issues/5311
	address_for_url = address.split('.')[0].translate(
			str.maketrans({'\n': ",+", ' ': '+'}),  # type: ignore[arg-type]
			)
	get_coord_url = f"https://nominatim.openstreetmap.org/search?q={address_for_url}&format=json"
	address_resp = httpx.get(get_coord_url)
	address_data = address_resp.json()
	if not address_data and fallback_settlement is not None:
		address_lines = address.split(", ")
		address_lines[-2] = fallback_settlement
		address_for_url = ", ".join(address_lines).translate(str.maketrans({' ': '+'}))  # type: ignore[arg-type]
		get_coord_url = f"https://nominatim.openstreetmap.org/search?q={address_for_url}&format=json"
		address_resp = httpx.get(get_coord_url)
		address_data = address_resp.json()

	if not address_data:
		raise ValueError("Address not found", address)

	return address_data[0]["lat"], address_data[0]["lon"]


def get_queens_library_locations() -> Dict[str, Tuple[str, Tuple[str, str]]]:
	"""
	Download and parse the list of library locations from Wikipedia.

	:returns: A mapping of library name to street address and coordinates.
	"""

	library_locations = {}

	for library, street_address in _get_queens_library_street_addresses().items():

		lat, lon = _get_coords_from_address(

			# Special case for Wikipedia's data
			street_address.replace("14 Road", "14th Road"),
			fallback_settlement="Queens",
			)

		library_locations[library] = (street_address, (lat, lon))

	return library_locations

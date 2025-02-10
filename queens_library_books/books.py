#!/usr/bin/env python3
#
#  books.py
"""
Functions to parse book data.
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
import bs4
import httpx

__all__ = ("get_queens_popular_books_2023", )


def get_queens_popular_books_2023() -> Dict[str, str]:
	"""
	Download and parse the list of popular books by library.

	:returns: A mapping of library name to book.
	"""

	books_url = "http://connect.queenslibrary.org/12070"
	response = httpx.get(books_url)

	soup = bs4.BeautifulSoup(response.text, "html.parser")
	idm_div = soup.find("div", {"id": "idmSge3"})
	assert idm_div is not None
	by_location_div = idm_div.find("div", {"id": "mce_23"})  # type: ignore[attr-defined]

	books = {}
	for location_p in by_location_div.children:
		location_string = location_p.get_text().strip()
		if not location_string:
			continue

		location, book, *_ = location_string.split('|')
		location = location.strip()
		book = book.strip().replace(" –", '–')
		books[location] = book

	return books

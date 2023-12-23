#!/usr/bin/env python3
#
#  plot.py
"""
Plot the chart.
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
from collections import defaultdict
from operator import itemgetter

# 3rd party
import folium  # type: ignore[import]
from domdf_python_tools.paths import PathPlus

# this package
from queens_library_books.plot_utils import make_markers, merge_geometry
from queens_library_books.utils import load_geojson_for_borough

locations_by_book = defaultdict(list)
library_names = []

for location, book in PathPlus("data/books.json").load_json().items():
	locations_by_book[book].append(location)
	library_names.append(location)

libraries = PathPlus("data/libraries.json").load_json()

# Centre map on Queens
m = folium.Map(location=[40.675, -73.8729094], zoom_start=11)

# Get geoJSON for just Queens
queens_geojson = load_geojson_for_borough("data/Borough Boundaries.geojson", "Queens")

# Make the rest of the world dimmer
style = {"fillColor": "#000000"}
folium.GeoJson(merge_geometry(queens_geojson), style_function=lambda x: style).add_to(m)

# Get a list of popular books (more than one library, in descending order)
book_counts = {book: len(locations) for book, locations in locations_by_book.items()}
books_by_popularity = dict(sorted(book_counts.items(), key=itemgetter(1), reverse=True))
popular_books = [k for k, v in books_by_popularity.items() if v > 1]

colours = [
		# "#003f5c",
		# "#2f4b7c",
		"#665191",  # "#a05195",
		# "#d45087",
		"#f95d6a",  # "#ff7c43",
		"#ffa600",
		"#1f77b4",
		"#ff7f0e",
		"#2ca02c",
		"#d62728",
		"#9467bd",
		"#8c564b",
		"#e377c2",
		"#7f7f7f",
		"#bcbd22",
		"#17becf",
		]

# print(len(popular_books))
# print(len(colours))
# exit()
book_colours = {}
for book in locations_by_book:
	if book in popular_books:
		colour = colours[popular_books.index(book)]
	else:
		colour = "#ffffff"
	book_colours[book] = colour

for library_name in libraries:
	if library_name not in library_names:
		continue

	# print(library_name)
	# print('', libraries[library_name][0])
	# print('', libraries[library_name][1])

	book = [b for b, ls in locations_by_book.items() if library_name in ls][0]

	for marker in make_markers(
			library_name,
			book,
			len(locations_by_book[book]),
			libraries[library_name][1],
			book_colours[book],
			):
		marker.add_to(m)

m.save("books/index.html")

# A "My Clippings.txt" Parser for Kindle

Functions for parsing Kindle clippings.

## Usage 

For an illustrative example of how to use the parser and the utility functions, see `source/example.ipynb`.

> Disclaimer: The functions work for *German* Kindles. If you want it to work for other languages, you have to make changes in the `replace_ger_to_eng_month()` functions in `parser.py`

### Parsing

```
>>> import parser
>>> path_to_clippings = "My Clippings.txt"
>>> clippings = (path_to_clippings_file=path_to_clippings)
```

The variable `clippings` contains all *highlights* and *notes* that are inside your Kindle's `My Clippings.txt` file.

For example, this is a *highlight* clipping:

```
#todo
```

And this is a *note* clipping:

```
#todo
```

### Utility functions

The file `utils.py` includes functions for doing some useful things with the parsed clippings.

* `get_unique_books(parsed_clippings)` returns a list of titles of the books in which you made at least one highlight or note.
* `get_clippings_from_book(book_title, parsed_clippings, clippings_type)` filters the parsed clippings for a specific book and, optionally, for a specific clippings_type (either `None` for all clippings, `"highlight"` for highlights only, or `"note"` for notes only).
* `get_book_progress(parsed_clippings, book_title)` shows you how much percent of the book you have read. Under the hood, the progress percentage is calculated as the position of your last highlight divided by the position of the second last highlight. This function is works if you made a highlight on the last page of your ebook.

### Creating Markdown-Notes from a Book's Clippings

The idea of this project was to automatically generate a formatted markdown `.md` file of the quotes that I highlight on my kindle. 

The function that allow you to do this is `create_markdown_from_clippings()`

* `create_markdown_from_clippings(parsed_clippings, book_title)` creates a `.md` file in your working director that includes all your clippings of a certain `book_title`, formatted in markdown. All *highlight* clippings are formatted as a quote, e.g. "> This is a highlight", and all *note* clippings is formatted as normal text, e.g. "This is a note".

For example, a `My Clippings.txt` file that looks like this:

```
Levels of Life (Barnes, Julian)
- Ihre Markierung auf Seite 28 | bei Position 284-286 | Hinzugefügt am Freitag, 8. Oktober 2021 20:06:02

I think it struck everybody that here we’d come 240,000 miles to see the Moon and it was the Earth that was really worth looking at.
==========
Levels of Life (Barnes, Julian)
- Ihre Markierung auf Seite 31 | bei Position 297-300 | Hinzugefügt am Freitag, 8. Oktober 2021 20:07:53

You put together two people who have not been put together before; and sometimes the world is changed, sometimes not. They may crash and burn, or burn and crash. But sometimes, something new is made, and then the world is changed. Together, in that first exaltation, that first roaring sense of uplift, they are greater than their two separate selves. Together, they see further, and they see more clearly.
==========
```

would create a file named `Levels of Life (Barnes, Julian).md` in a subfolder named `/output/` in your current working directory. That file would look like this:

```
# Levels of Life (Barnes, Julian)

> I think it struck everybody that here we’d come 240,000 miles to see the Moon and it was the Earth that was really worth looking at.

> You put together two people who have not been put together before; and sometimes the world is changed, sometimes not. They may crash and burn, or burn and crash. But sometimes, something new is made, and then the world is changed. Together, in that first exaltation, that first roaring sense of uplift, they are greater than their two separate selves. Together, they see further, and they see more clearly.
```

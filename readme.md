# A "My Clippings.txt" Parser for Kindle

Functions for parsing Kindle clippings and turning them into markdown-formatted documents. 

I use this programm to help me write book summaries like [this](https://www.nilsgandlau.de/posts/levels-of-life.html) or [this](https://www.nilsgandlau.de/posts/attached.html) one on my [personal website](https://www.nilsgandlau.de/).

## Example

Suppose your Kindle's `My Clippings.txt` file looks like this:

![](img/example-input.png)

then the following sequence of functions:

```
>>> import kindle_parser as parser
>>> import utils
>>> path_to_clippings_file = "My Clippings.txt"
>>> parsed_clippings = parser.parse_clippings(path_to_clippings_file)
>>> book_titles = utils.get_unique_books(parsed_clippings)
>>> utils.create_markdown_from_clippings(
      parsed_clippings=parsed_clippings,
      book_title=book_titles[0],
      clipping_type="all",
      output_filename="quotes_levels_of_life.md"
    )
```

would create a markdown-document named `quotes_levels_of_life.md` in a subfolder of your current working directory:

![](img/example-output.png)

## Usage

See `source/example.ipynb` for an example of how to use the code.

> Disclaimer: The functions work for *German* Kindles. If you want it to work for other languages, you have to make changes in the `replace_ger_to_eng_month()` functions in `parser.py`

### How to parse "My Clippings.txt"

```
>>> import kindle_parser as parser
>>> path_to_clippings_file = "My Clippings.txt"
>>> parsed_clippings = parser.parse_clippings(path_to_clippings_file)
```

`parsed_clippings` contains all *highlights* and *notes* that are inside your Kindle's `My Clippings.txt` file.

For example, this is a *highlight* clipping:

```
{'book_title': 'Levels of Life (Barnes, Julian)',
 'clipping_type': 'highlight',
 'text': 'Some soar with art, others with religion; most with love. But when we soar, we can also crash.',
 'pos_start': 348,
 'pos_end': 349,
 'date': datetime.datetime(2021, 10, 8, 20, 16, 13)}
```

And this is a *note* clipping:

```
#todo
```

### Things to do with the parsed clippings

The file `utils.py` includes functions for doing stuff with the parsed clippings.

* `get_unique_books(parsed_clippings)` returns a list of the books for which at least one clipping is available.
* `get_clippings_from_book(book_title, parsed_clippings, clippings_type)` filters the parsed clippings for a specific book and, optionally, for a specific clippings_type. By specifying `clippings_type="all"` you get all clippings, by specifying `clippings_type="highlight"` you only get your highlights, and by specifying `clippings_type="note"` you only get your notes.
* `get_book_progress(parsed_clippings, book_title)` shows you how much percent of the book you have read. Under the hood, the progress percentage is calculated as the position of your last highlight divided by the position of the second last highlight. Hence if you want this function to return your actual progress you need to make a highlight at the very last page of your ebook.

### Creating a markdown document with your clippings

The initial idea of this project was to automatically generate a formatted markdown `.md` file of the quotes that I highlight on my kindle. The formatted markdown document with my favorite quotes of a book can then easily be published on my [personal blog](https://www.nilsgandlau.de).

The function that creates a markdown document from a book's parsed clippings is `create_markdown_from_clippings()`:

`create_markdown_from_clippings(parsed_clippings, book_title, clipping_type, output_filename)` creates a new markdown document with the clippings of one of your books. The arguments:

* `parsed_clippings`: the output of the `parse_clippings()` parser function.
* `book_title`: a string of the book title that you want to generate a markdown document for 
* `clipping_type`: one of `"all"`, `"highlight"`, or `"note"`
* `output_filename`: the name of the markdown file that is generated. Must end with `.md`. For example, `output_filename="book_highlights.md"`


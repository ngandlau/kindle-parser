import os

def get_book_progress(clippings_data, book_title):
    clippings_of_book = get_clippings_from_book(
        book_title=book_title,
        clippings_data=clippings_data,
        clipping_type=None
    )
    max_pos = get_max_position(clippings_of_book)
    second_max_pos = get_second_max_position(clippings_of_book)
    perc_progress = second_max_pos / max_pos
    print(f"Reading progress: {round(perc_progress*100, 2)}%")
    return perc_progress

def get_max_position(clippings_from_book):
    positions = [clipping["pos_end"] for clipping in clippings_from_book if clipping["pos_end"] is not None]
    max_pos = max(positions)
    return max_pos

def get_second_max_position(clippings_from_book):
    positions = [clipping["pos_end"] for clipping in clippings_from_book if clipping["pos_end"] is not None]
    
    if all(x == positions[0] for x in positions):
        return max(positions)
    
    first_max = max(positions)
    second_max = max(positions)
    while first_max == second_max:
        positions.remove(first_max)
        second_max = max(positions)
    return second_max
        
def get_clippings_from_book(book_title, clippings_data, clipping_type=None):
    """
    args:
        book_title: a string of the title of a book
        clippings_data: a list of dictionaries, ie the output of get_clippings()
        clipping_type: Optional: None or "highlight" or "note"
    """
    clippings = []
    for clipping in clippings_data:
        if clipping_type is None:
            if clipping["book_title"] == book_title:
                clippings.append(clipping)
        else:
            if clipping["book_title"] == book_title and clipping["clipping_type"] == clipping_type:
                clippings.append(clipping)
    return clippings

def clippings_to_markdown(book_title, clippings_of_book):
    text = "# " + book_title + "\n\n"
    for clipping in clippings_of_book:
        if clipping["clipping_type"] == "highlight":
            text += "> " + clipping["text"] + "\n\n"
        else:
            text += clipping["text"] + "\n\n"
    return text

def create_markdown_from_clippings(clippings_data, book_title):
    clippings_of_book = get_clippings_from_book(
        book_title=book_title,
        clippings_data=clippings_data,
        clipping_type=None
    )
    try:
        os.mkdir("output")
    except FileExistsError:
        pass
    with open(os.path.join("output", book_title + ".md"), "w", encoding="utf-8") as f:
        text = clippings_to_markdown(
            book_title=book_title,
            clippings_of_book=clippings_of_book
        )
        f.write(text)
    f.close()
    
def get_unique_books(clippings_data):
    book_titles = set([clipping["book_title"] for clipping in clippings_data])
    return list(book_titles)


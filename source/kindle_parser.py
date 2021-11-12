import re
from datetime import datetime
import difflib

def parse_clippings_file(path_to_clippings_file):
    with open(path_to_clippings_file, "r", encoding="utf8") as file:
        txt = file.read()
        parsed_clippings = get_clippings(my_clippings_text=txt)
        return parsed_clippings

def first_n_sentences(string, n):
    first_n_sentences = string.split(".")[:n]
    return first_n_sentences

def get_overlap(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2)) 
    return s1[pos_a:pos_a+size]

def get_clippings(my_clippings_text):
    clippings = my_clippings_text.split("==========")
    clippings = [clean_clipping(x) for x in clippings if is_valid_clipping(x)]
    
    last_clipping_text = None
    parsed_clippings = []
    for clipping in clippings:
        book_title = get_book_title(clipping)
        date = get_date(clipping)
        text = get_text(clipping)

        # check for duplicate highlights
        if last_clipping_text is not None:
            is_duplicate = False
            if last_clipping_text in text or text in last_clipping_text:
                parsed_clippings.pop()

            # # check whether first 2 sentences are equal
            # first_n_sentences_last = first_n_sentences(last_clipping_text, 2)
            # first_n_sentences_curr = first_n_sentences(text, 2)
            # if first_n_sentences_last == first_n_sentences_curr:
            #     is_duplicate = True
            #     parsed_clippings.pop()

            # # check for overlap within string
            # if not is_duplicate:
            #     overlap = get_overlap(text, last_clipping_text)
            #     # remove last highlight if overlap is more than 80%
            #     if len(overlap) > (0.8)*len(text):
            #         is_duplicate = True
            #         parsed_clippings.pop()
        
        last_clipping_text = text

        if is_clipping_highlight(clipping):
            clipping_type = "highlight"
            pos_start = get_position(clipping)["start"]
            pos_end = get_position(clipping)["end"]
        else:
            clipping_type = "note"
            pos_start = None,
            pos_end = None

        parsed_clippings.append({
            "book_title": book_title,
            "clipping_type": clipping_type,
            "text": text,
            "pos_start": pos_start,
            "pos_end": pos_end,
            "date": date
        })
    return parsed_clippings
    
def clean_clipping(clipping):
    clipping = clipping.replace("\ufeff", "")
    clipping = clipping.replace("–", "-")
    clipping = clipping.replace("‘", "'")
    clipping = clipping.replace("’", "'")
    clipping = clipping.replace("”", "\"")
    clipping = clipping.replace("“", "\"")

    if clipping[:1] == "\n":
        clipping = clipping[1:]
    return clipping

def is_valid_clipping(clipping):
    is_valid = True
    if len(clipping) == 1:
        is_valid = False
    if clipping == "\n":
        is_valid = False
    if clipping == "":
        is_valid = False
    return is_valid
    
def get_metadata(clipping):
    metadata = clipping.split("\n\n")[0]
    return metadata
    
def is_clipping_highlight(clipping):
    metadata = get_metadata(clipping)
    x = re.search("Ihre Markierung", metadata)
    if x is not None:
        return True
    else:
        return False
    
def get_text(clipping):
    quote = re.search("\d{2}:\d{2}:\d{2}\\\n\\\n.*", clipping).group(0)
    quote = re.sub("\d{2}:\d{2}:\d{2}\\\n\\\n", "", quote)
    return quote

def get_position(clipping):
    metadata = get_metadata(clipping)
    position = re.search("Position\ \d+-\d+", metadata)
    if position is None:
        # then the clipping doesn't have an end position.
        # E.g. "Position 565" instead of "Position 565-566"
        position = re.search("Position\ \d+", metadata).group(0)
        start_position = re.search("\d+", position).group(0)
        end_position = 0
    else:
        position = position.group(0)
        start_position = re.search("\d+-", position).group(0)[:-1]
        end_position = re.search("-\d+",position).group(0)[1:]
    return {"start": int(start_position), "end": int(end_position)}

def get_date(clipping):
    metadata = get_metadata(clipping)
    date = re.search("\d+\\.\ [a-zA-Z]+\ \d{4}\ \d{2}:\d{2}:\d{2}", metadata)
    date = date.group(0).replace(".", "")
    date = replace_ger_to_eng_month(date)
    date = datetime.strptime(date, "%d %B %Y %H:%M:%S")
    return date

def get_book_title(clipping):
    metadata = get_metadata(clipping)
    title = metadata.split("\n")[0].strip()
    return title

def replace_ger_to_eng_month(x):
    translations = {
        "Januar": "January",
        "Februar": "February",
        "März": "March",
        "April": "April",
        "Mai": "May",
        "Juni": "June",
        "Juli": "July",
        "August": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Dezember": "Dezember"
    }
    for german_month in translations.keys():
        x = x.replace(german_month, translations[german_month])
    return x
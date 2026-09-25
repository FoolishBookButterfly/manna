import json
import re

def open_bible_json():
    with open("data/KJV/KJV_bible.json", "r", encoding="utf-8") as file:
        return json.load(file)

bible = open_bible_json()

def fetch_passage(book_name, chapter_num=1, verse_num=1):

    # return bible[book_name][str(chapter_num)][str(verse_num)]
    for book, chapters in bible.items():
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                if (book == book_name
                    and chapter == str(chapter_num) 
                    and verse == str(verse_num)):
                    return text

print(fetch_passage("Psalm", 119))



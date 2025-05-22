from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import re
import os
import subprocess
import time
import requests
import googletrans

def book_information(files, book):
    #i want to create something that randomises which file is chosen among the listdir
    title = book.get_metadata('DC','title')[0][0]
    author = book.get_metadata('DC','creator')[0][0]

    print(f"Author: {author}\nTitle: {title}")

def book_char_count(book):
    jp_char_pattern = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff66-\uff9f]')
    #takes the regex from kanji,katana,hiragana, halfwidths too

    char_count = 0
    #creates a counter for chars

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        #loops through the whole of the book 
        soup = BeautifulSoup(item.get_content(),'html.parser')
        #uses html parser to read the contents of item(the epub)
        text = soup.get_text()
        #basically gets all text from a html using beautifulsoup
        matches = jp_char_pattern.findall(text)
        #shows all matches of regex in text
        char_count += len(matches)
        #adds the matches to the character count (char_count = char_count + len(matches))
    print(f"total chars: {char_count}")

def book_blurb(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"

    response = requests.get(url)

    if response.status_code == 200:
    #if the response.status_code == 200 then it means 
        data = response.json()
        books = data.get('items')

        if not books:
            print("no books")
            return
        volume_info = books[0].get('volumeInfo', {})
        description = volume_info.get('description', 'no description')
        print(description)

    else:
        print("failed to retrieve data")

    #hard part is we need to take the title variable use that to find the product on amazon.co.jp
    #this will be using beautiful soup to extract a blurb from amazon.co.jp this will print the blurb in japanese (あらすじ)
    #this will then use deepL to translate japanese to english 


def main():

    dir = r''
    os.chdir(dir)
    files = os.listdir(dir)

    for file in files[:1]:
        print(f"\n{file}\n")
        subprocess.run("pbcopy", text=True, input=file)
    
    time.sleep(1)

    print("book has been copied to clipboard! \n")
    chosen_book = input("choose a book")

    book = epub.read_epub(f"{chosen_book}")
    book_information(files, book)
    book_char_count(book)
    book_blurb(f"{chosen_book}")

main()
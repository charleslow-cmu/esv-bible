import os
import sys
import requests
import time
import re

def read_token():
    with open("environment.txt") as f:
        k, v = f.read().strip().split("=")
    return v

def get_throttle_time(text):
    digit = re.findall(r'\d+', text)[0]
    return int(digit)


def get_esv_text(passage):
    params = {
        'q': passage,
        'include-headings': True,
        'include-footnotes': False,
        'include-verse-numbers': True,
        'include-short-copyright': False,
        'include-passage-references': False,
        'indent-paragraphs': 0
    }

    headers = {
        'Authorization': 'Token %s' % API_KEY
    }

    i = 0
    while True:
        try:
            response = requests.get(API_URL, params=params, headers=headers)
            passages = response.json()['passages']
            break
        except:
            if i > 5:
                return "Error"
            else:
                print("Error for passage: {}".format(passage))
                print(response.json())
                throttle_time = get_throttle_time(response.json()['detail'])
                print("Sleeping for {} seconds".format(throttle_time))
                time.sleep(throttle_time)
                i += 1
    return passages[0].strip()


def get_esv_book(book):
    print("===={}====".format(book))
    chapter = 1
    prev_text = ""

    while True:
        passage = book + " " + str(chapter)
        text = get_esv_text(passage)
        if text == prev_text:
            print("No passage: {}".format(passage))
            break
        else:
            print("Downloading passage: {}".format(passage))
            write_text(text, passage)
            prev_text = text  # Store prev text
            chapter += 1


def write_text(text, passage):
    with open("data/{}.txt".format(passage), 'w') as f:
        f.write(text)



if __name__ == "__main__":
    API_KEY = read_token()
    API_URL = 'https://api.esv.org/v3/passage/text/'
    special_books = ["Obadiah", "Philemon", "Jude", "2 John", "3 John"]

    with open("books.txt") as f:
        books = f.read().strip().splitlines()

    for i in range(0, len(books)):
        book = books[i]
        if book in special_books:
            text = get_esv_text(book)
            print("Downloading passage: {}".format(book))
            write_text(text, book)
        else:
            get_esv_book(book)
            pass




import os
import sys
import requests

def read_token():
    with open("environment.txt") as f:
        k, v = f.read().strip().split("=")
    return v

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

    try:
        response = requests.get(API_URL, params=params, headers=headers)
        passages = response.json()['passages']
    except:
        


    return passages[0].strip() if passages else 'Error'


def write_text(text, passage):
    with open("data/{}.txt".format(passage), 'w') as f:
        f.write(text)



if __name__ == "__main__":
    API_KEY = read_token()
    API_URL = 'https://api.esv.org/v3/passage/text/'

    get_esv_text("Exodus 9")

    # with open("books.txt") as f:
    #     books = f.read().strip().splitlines()
    #
    # for i in range(1, 10):
    #     book = books[i]
    #     chapter = 1
    #     prev_text = ""
    #
    #     while True:
    #         passage = book + " " + str(chapter)
    #         text = get_esv_text(passage)
    #         if text == prev_text:
    #             print("No passage: {}".format(passage))
    #             break
    #         else:
    #             print("Downloading passage: {}".format(passage))
    #             write_text(text, passage)
    #             prev_text = text # Store prev text
    #             chapter += 1




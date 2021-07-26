#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright 2021 Frede Hundewadt
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software and
# associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from bs4 import BeautifulSoup
from operator import itemgetter
import argparse
import urllib.request
import urllib.parse
import urllib


# 118.dk
# person søgning : https://www.118.dk/search/go?pageSize=100&page=1&listingType=residential&where=
# firma søgning  : https://www.118.dk/search/go?pageSize=100&page=1&listingType=business&where=
# alle søgning   : https://www.118.dk/search/go?pageSize=100&page=1&listingType=&where=
# ingen grund til at fortælle at dette er et script
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
SEARCH_118_URL = "https://www.118.dk/search/go?pageSize=100&page=1&listingType=residential&where="
SITE = "118.dk"

def parse_url(address):
    strings = list()
    entries = list()
    phones = list()
    contacts = list()
    url = f"{SEARCH_118_URL}{urllib.parse.quote_plus(address)}"
    req = urllib.request.Request(url=url, headers=USER_AGENT)
    with urllib.request.urlopen(req) as res:
        page = res.read()
        soup = BeautifulSoup(page, "html.parser", from_encoding='utf-8')
        for script in soup(["script", "style", "ul", "input", "form", "title", "ins", "h1", "h2", "h4",
                            "fieldset", "iframe", "strong", "img", "head", "meta", "link"]):
            script.extract()
        for string in soup.stripped_strings:
            if string.startswith("Geo") or \
                    string.startswith("FAG") or \
                    string.startswith("< til") or \
                    string.startswith("Tlf") or \
                    string.startswith("118.dk") or \
                    string.startswith("Vi kan") or \
                    string.startswith("Læs mere") or \
                    string.startswith("Copyright") or \
                    string.startswith("close") or \
                    string.startswith("Fjernelse") or \
                    string.startswith("Her kan") or \
                    string.startswith("Husnummer"):
                continue
            if string == "se kort":
                entries.append(tuple(strings))
                strings.clear()
            else:
                strings.append(string)

    for entry in entries:
        ad_protect = str(entry[1])
        if ad_protect.startswith("Reklame"):
            continue
        try:
            same_house = False
            number = entry[2]
            name = entry[0]
            iterate = [x for x in contacts if x["name"] == name]
            for c in iterate:
                if number not in c["phones"]:
                    same_house = True
                    c["phones"] = c["phones"] + [number]

            if not same_house:
                person = {
                    "name": entry[0],
                    "address": entry[1],
                    "phones": [number]
                }
                contacts.append(person)
        except (Exception,):
            continue

    return sorted(contacts, key=itemgetter("address"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--adresse", required=True, type=str, help="vejnavn [nr], postnummer")
    args = parser.parse_args()
    results = parse_url(args.adresse)

    for result in results:
        print(f"Adresse : {result['address']}")
        print(f"   Navn : {result['name']}")
        for number in result["phones"]:
            print(f"    Tlf : {number}")
        print(f"---------------------")

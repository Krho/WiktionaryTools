# -*- coding: utf-8 -*-
import re
import json
import pywikibot
from pywikibot import page

WIKTIONNAIRE = pywikibot.Site('fr', 'wiktionary')
WIKIPEDIA = pywikibot.Site('fr','wikipedia')
WIKIDATA = pywikibot.Site('wikidata', 'wikidata')
source = re.compile("{{source\|[\w|\{\{| |\}|é|.|&]+")
wAuthor = re.compile("{{w\|[\w| ]+}}")
gender = "P21"
nationality ="P27"
birthDate = "P569"
datas = [gender, nationality, birthDate]
authors="authors"
words="words"

cache = json.loads(open("cache.json").read())

def sources(word):
    print word
    cache["words"][word]=[]
    text = page.Page(WIKTIONNAIRE, word).text
    templates = source.findall(text)
    for template in templates:
        #Authors are linked to wikipedia
        wikiAuthors = wAuthor.findall(template)
        for wikiA in wikiAuthors:
            wikiAuthor = wikiA[4:len(wikiA)-2]
            if wikiAuthor not in cache[authors]:
                cache[authors][wikiAuthor] = characteristics(wikiAuthor)
                cache[authors][wikiAuthor][words] = []
            cache[words][word].append(wikiAuthor)
            cache[authors][wikiAuthor][words].append(word)
    with open("cache.json", "w") as file:
        data = json.dumps(cache, indent=2)
        file.write(data)
    return cache

def characteristics(author):
    print "\t"+author
    result={}
    wikiArticle = page.Page(WIKIPEDIA, author)
    if wikiArticle.exists():
        item = wikiArticle.data_item()
        for data in datas:
            if data in item.claims:
                for claim in item.claims[data]:
                    if claim.getTarget() is not None:
                        if data is birthDate:
                            result[data]=claim.getTarget().year
                        else:
                            result[data]=claim.getTarget().id
    return result

print sources(u"encyclopédie")

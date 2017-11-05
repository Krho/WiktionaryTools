# -*- coding: utf-8 -*-
import re
import json
import pywikibot
from pywikibot import page

WIKTIONNAIRE = pywikibot.Site('fr', 'wiktionary')
WIKIPEDIA = pywikibot.Site('fr','wikipedia')
WIKIDATA = pywikibot.Site('wikidata', 'wikidata')
source = re.compile("{{source\|.+}}")
wAuthor = re.compile("{{w\|[^|}]+[|}]")
nomWAuthor = re.compile("{{nom w pc\|([^|}]+)\|([^|}]+)[|}]")
link = re.compile("\[\[[^|\]]+\]\]")
gender = "P21"
nationality ="P27"
birthDate = "P569"
datas = [gender, nationality, birthDate]
authors="authors"
words= u'words'
thesaurusPrefix = u"Thésaurus:"
fr = u"/français"

cache = json.loads(open("cache.json").read())

"""
Functions used to collect data from the wiktionnary
"""

def sources(word):
    print word
    p = page.Page(WIKTIONNAIRE, word)
    if p.exists:
        cache[words][word]=[]
        text = p.text
        templates = source.findall(text)
        for template in templates:
            #Authors are linked to wikipedia
            wikiAuthors = [x[4:len(x)-2] for x in wAuthor.findall(template)]
            wikiAuthors += [x[0]+" "+x[1] for x in nomWAuthor.findall(template)]
            for wikiAuthor in wikiAuthors:
                if wikiAuthor not in cache[authors]:
                    cache[authors][wikiAuthor] = characteristics(wikiAuthor)
                    cache[authors][wikiAuthor][words] = []
                cache[words][word].append(wikiAuthor)
                cache[authors][wikiAuthor][words].append(word)
        return True
    else:
        return False

def write():
    with open("cache.json", "w") as file:
        data = json.dumps(cache, indent=2)
        file.write(data)

def characteristics(author):
    print "\t"+author
    result={}
    wikiArticle = page.Page(WIKIPEDIA, author)
    if wikiArticle.exists():
        while wikiArticle.isRedirectPage():
            wikiArticle = wikiArticle.getRedirectTarget()
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

def harvest(thesaurus):
    p = page.Page(WIKTIONNAIRE, thesaurusPrefix+thesaurus+fr)
    if p.exists and thesaurus not in cache["thesaurus"]:
        print thesaurus.upper()
        cache["thesaurus"][thesaurus]=[]
        text = page.Page(WIKTIONNAIRE, thesaurusPrefix+thesaurus+fr).text
        wikiWords = [x[2:len(x)-2] for x in link.findall(text)]
        for wikiWord in wikiWords:
            if sources(wikiWord):
                cache["thesaurus"][thesaurus].append(wikiWord)
    write()

"""
Functions used to present and analyse data
"""
def analyse(thesaurus):
    print "Analysing "+thesaurus
    result={}
    if thesaurus in cache["thesaurus"]:
        for data in datas:
            result[data]={}
        for word in cache["thesaurus"][thesaurus]:
            for author in cache[words][word]:
                for data in datas:
                    if data in cache[authors][author]:
                        d = cache[authors][author][data]
                        if d in result[data]:
                            result[data][d] += 1
                        else:
                            result[data][d] = 1
    return result

print analyse(u"femme")

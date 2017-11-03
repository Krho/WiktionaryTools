# -*- coding: utf-8 -*-
import re
import json
import pywikibot
from pywikibot import page

import cache
import logger


LOG = logger.logger(debug=True)  # logger in debug mode


WIKTIONNAIRE = pywikibot.Site('fr', 'wiktionary')
WIKIPEDIA = pywikibot.Site('fr', 'wikipedia')
WIKIDATA = pywikibot.Site('wikidata', 'wikidata')
source = re.compile("{{source\|.+}}")
wAuthor = re.compile("{{w\|[^|}]+[|}]")
nomWAuthor = re.compile("{{nom w pc\|([^|}]+)\|([^|}]+)[|}]")
link = re.compile("\[\[[^|\]]+\]\]")
gender = "P21"
nationality = "P27"
birthDate = "P569"
datas = [gender, nationality, birthDate]
authors = "authors"
words = u'words'
thesaurusPrefix = u"Thésaurus:"
fr = u"/français"

CACHE = cache.get()


def sources(word):
    """Find sources information for word."""
    LOG.debug(word)
    p = page.Page(WIKTIONNAIRE, word)
    if p.exists:
        CACHE[words][word] = []
        text = p.text
        templates = source.findall(text)
        for template in templates:
            # Authors are linked to wikipedia
            wikiAuthors = [x[4:len(x) - 2] for x in wAuthor.findall(template)]
            wikiAuthors += [x[0] + " " + x[1]
                            for x in nomWAuthor.findall(template)]
            for wikiAuthor in wikiAuthors:
                if wikiAuthor not in CACHE[authors]:
                    CACHE[authors][wikiAuthor] = characteristics(wikiAuthor)
                    CACHE[authors][wikiAuthor][words] = []
                CACHE[words][word].append(wikiAuthor)
                CACHE[authors][wikiAuthor][words].append(word)
        return True
    else:
        return False


def characteristics(author):
    """Find characteristics for an author on Wikidata."""
    LOG.debug("\t%s", author)
    result = {}
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
                            result[data] = claim.getTarget().year
                        else:
                            result[data] = claim.getTarget().id
    return result


def harvest(thesaurus):
    """Harvest information about a given Thesaurus and save cache"""
    LOG.info("Harvesting: %s", thesaurus)
    p = page.Page(WIKTIONNAIRE, thesaurusPrefix + thesaurus + fr)
    if p.exists and thesaurus not in CACHE["thesaurus"]:
        LOG.debug(thesaurus.upper())
        CACHE["thesaurus"][thesaurus] = []
        text = page.Page(WIKTIONNAIRE, thesaurusPrefix + thesaurus + fr).text
        wikiWords = [x[2:len(x) - 2] for x in link.findall(text)]
        for wikiWord in wikiWords:
            if sources(wikiWord):
                CACHE["thesaurus"][thesaurus].append(wikiWord)
    cache.save(CACHE)


def analyse(thesaurus):
    """Present results on a given thesaurus from the cache file."""
    LOG.info("Analysing: %s", thesaurus)
    result = {}
    if thesaurus in CACHE["thesaurus"]:
        for data in datas:
            result[data] = {}
        for word in CACHE["thesaurus"][thesaurus]:
            for author in CACHE[words][word]:
                for data in datas:
                    if data in CACHE[authors][author]:
                        d = CACHE[authors][author][data]
                        if d in result[data]:
                            result[data][d] += 1
                        else:
                            result[data][d] = 1
    return result

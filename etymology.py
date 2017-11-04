# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands, example, NOLIMIT
from sopel.formatting import underline
from bs4 import BeautifulSoup
import re, requests

WORD_URI = 'https://www.etymonline.com/word/'

def get_definitions(word, html):
    definitions = []
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup.find_all('div', class_=re.compile('^word--')):
        try:
            name = element.find('p', class_=re.compile('^word__name')).text
        except AttributeError as e:
            # probably a h1
            name = element.find('h1', class_=re.compile('^word__name')).text
        definition = element.find('object').text
        definitions.append((name, definition))
    return definitions

@commands('ety')
@example('.ety word or phrase')
def f_etymology(bot, trigger):
    """Look up the etymology of a word"""
    phrase = re.sub('[^a-zA-Z ]', '', trigger.group(2)).strip().lower()
    req = requests.get(WORD_URI + phrase)
    if req.ok:
        results = get_definitions(phrase, req.text)
        if len(results):
            definitions = ". " .join(["%s %s" % (underline(pair[0]), pair[1]) for pair in results])
            bot.say(definitions, trigger.sender, len(definitions)*2)
        else:
            bot.say('Can\'t find the etymology for "%s".' % phrase, trigger.sender)
    else:
        bot.say('Can\'t find the etymology for "%s".' % phrase, trigger.sender)
    return NOLIMIT

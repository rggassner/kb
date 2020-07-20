#!/usr/bin/python3
from selenium import webdriver
import pandas as pd
import random
import re
import json
import time
from selenium.common.exceptions import StaleElementReferenceException
from urllib.parse import urlparse
import unidecode

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2,"download.default_directory": "NUL", "download.prompt_for_download": False}
chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')

browser = webdriver.Chrome(chrome_options=chrome_options)
waitMin=10
waitMax=20
initialURL="http://www.mysite.org/"
expressionDomain=r'^http://www.mysite.org/'
visited=set()
tovisit=set()
wordDB={}
tovisit.add(initialURL)
def extractAllLinks(browser,tovisit,visited):
    for link in browser.find_elements_by_xpath("//a[@href]"):
        eurl=link.get_attribute("href")
        if eurl:
            if re.search(expressionDomain, eurl):
                eurl=eurl.split("#",maxsplit=1)[0]
                if eurl.startswith('tel:') or eurl.startswith('mailto:'):
                    visited.add(eurl)
                if eurl not in visited:
                    tovisit.add(eurl)

def extractAllWords(browser,wordDB):
    for element in browser.find_elements_by_xpath("//*[contains(text(), '')]"):
        for word in element.text.split():
            word = ''.join([i for i in word if i.isalpha()])
            word = unidecode.unidecode(word)
            word = word.lower()
            if word in wordDB:
                wordDB[word] = wordDB[word] + 1
            else:
                wordDB[word] = 1

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
        raise TypeError

while (True):
    try:
        url = random.choice(tuple(tovisit))
        browser.get(url)
        extractAllLinks(browser,tovisit,visited)
        extractAllWords(browser,wordDB)
        visited.add(url)
        with open('words.json', 'w') as outfile:
           result=json.dumps(wordDB,default=set_default)
           outfile.write(result)
        print("visited: {} to visit: {} words: {} url: {}".format(len(visited), len(tovisit), len(wordDB),url))
        tovisit.remove(url)
        time.sleep(random.randint(waitMin,waitMax))
    except StaleElementReferenceException:
        pass

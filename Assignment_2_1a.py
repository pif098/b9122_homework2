#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:47:38 2023

@author: z
"""
#1a
from bs4 import BeautifulSoup
import urllib.request

seed_url = "https://press.un.org/en"

urls = [seed_url]  
seen = [seed_url]  
opened = []  

maxNumUrl = 10  
print("Starting with UN url=" + str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    try:
        curr_url = urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= " + curr_url)
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        
        if soup.find('a', hreflang='en', text='Press Release') and "crisis" in soup.text.lower():
            opened.append(curr_url)

        for tag in soup.find_all('a', href=True):
            childUrl = urllib.parse.urljoin(seed_url, tag['href'])
            if seed_url in childUrl and childUrl not in seen:
                urls.append(childUrl)
                seen.append(childUrl)
    except Exception as ex:
        print("Unable to access= " + curr_url)
        print(ex)
print("List of UN press releases containing the word 'crisis':")
for opened_url in opened:
    print(opened_url)


#1b

EP_BASE_URL = "https://www.europarl.europa.eu/news/en/press-room/page/"

ep_urls = []
for page_number in range(10):
    ep_urls.append(EP_BASE_URL + str(page_number))

ep_seen = []
ep_opened = []

ep_maxNumUrl = 10
print("\nStarting with EP url=" + str(ep_urls))
while len(ep_urls) > 0 and len(ep_opened) < ep_maxNumUrl:
    try:
        curr_ep_url = ep_urls.pop(0)
        req_ep = urllib.request.Request(curr_ep_url, headers={'User-Agent': 'Mozilla/5.0'})
        ep_webpage = urllib.request.urlopen(req_ep).read()
        ep_soup = BeautifulSoup(ep_webpage, 'html.parser')

        if ep_soup.find('span', class_='ep_name', text='Plenary session') and "crisis" in ep_soup.text.lower():
            ep_opened.append(curr_ep_url)

        for tag in ep_soup.find_all('a', href=True):
            ep_childUrl = urllib.parse.urljoin(EP_BASE_URL, tag['href'])
            if EP_BASE_URL in ep_childUrl and ep_childUrl not in ep_seen:
                ep_urls.append(ep_childUrl)
                ep_seen.append(ep_childUrl)

    except Exception as ex:
        print("Unable to access= " + curr_ep_url)
        print(ex)
print("List of EP press releases related to plenary sessions and containing the word 'crisis':")
for ep_url in ep_opened:
    print(ep_url)

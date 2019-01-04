#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

BeautifulSoup does not support XPath expression by default, so we use CSS
the expression here, but you can use https://github.com/scrapy/parsel to write
XPath to extract data as you like

"""
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from six.moves.urllib import parse

START_PAGE = "https://www.fbi.gov/wanted/fugitives"

QUEUE = []

def parse_list_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    links = soup.select('p[class="read-more text-center bottom-total visualClear"]')
    if links:
        next_link = links[0].find('button', href=True)
        next_link = url[:url.find('?')] + next_link
        QUEUE.append(
            (parse_list_page, next_link)
        )

    links = soup.select('li.portal-type-person castle-grid-block-item a')
    for link in links:
        product_url = link.attrs['href']
        result = parse.urlparse(url)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        product_url = parse.urljoin(base_url, product_url)
        QUEUE.append(
            (parse_detail_page, product_url)
        )

def parse_detail_page(url):
    # r = requests.get(url)
    # soup = BeautifulSoup(r.text, "lxml")
    print("processing " + url)

def main():
    """
    Push callback method and url to queue
    """
    QUEUE.append(
        (parse_list_page, START_PAGE)
    )

    while len(QUEUE):
        call_back, url = QUEUE.pop(0)
        call_back(url)

if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main
"""

from pprint import pprint
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

def _get_battle_links():
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://play.pokemonshowdown.com/battles")

    sleep(5)
    driver.find_element_by_xpath("//button[@name='selectFormat']").click()
    sleep(1)
    driver.find_element_by_xpath("//button[@value='gen7vgc2018']").click()
    sleep(1)
    driver.find_element_by_xpath("//input[@name='elofilter']").click()
    sleep(1)

    try:
        soup = BeautifulSoup(driver.page_source)
        links = soup.select('a[href^="/battle-"]')
        return list("https://play.pokemonshowdown.com"+link["href"] for link in links)
    finally:
        driver.close()

if __name__ == '__main__':
    pprint(_get_battle_links())

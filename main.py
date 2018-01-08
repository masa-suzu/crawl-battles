#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main
"""

from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
from driver import DriverWrapper

def scrape_battle_urls(driver, battle_format):
    """
    Scrape urls of battles from https://play.pokemonshowdown.com
    """
    driver.get("https://play.pokemonshowdown.com/battles")
    driver.find_element_by_xpath("//button[@name='selectFormat']").click()
    driver.find_element_by_xpath("//button[@value='%s']" % battle_format).click()
    driver.find_element_by_xpath("//input[@name='elofilter']").click()

    try:
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        links = soup.select('a[href^="/battle-"]')
        return list("https://play.pokemonshowdown.com"+link["href"] for link in links)
    finally:
        driver.close()

def main():
    """
    Main method.
    """

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver = DriverWrapper(driver)

    battle_format = 'gen7vgc2018'

    return scrape_battle_urls(driver, battle_format)

if __name__ == '__main__':
    pprint(main())

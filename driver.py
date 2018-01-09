#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Web Driver
"""

import os
from time import sleep
from contextlib import contextmanager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from bs4 import BeautifulSoup

class DriverWrapper(object):
    """
    Wrapped driver. Insert sleep operation for loading page.
    """
    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, attr):
        orig_attr = self.driver.__getattribute__(attr)
        if callable(orig_attr):
            def _hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent driver from becoming unwrapped
                if result == self.driver:
                    return self
                self.__post(attr)
                return result
            return _hooked
        else:
            return orig_attr

    def __post(self, attr):
        if attr == 'get':
            sleep(10)
        elif attr == 'find_element_by_xpath':
            sleep(2)

    def scrape_battle_urls(self, battle_format):
        """Scrape urls of battles from https://play.pokemonshowdown.com."""
        self.get("https://play.pokemonshowdown.com/battles")
        self.find_element_by_xpath("//button[@name='selectFormat']").click()
        self.find_element_by_xpath("//button[@value='%s']" % battle_format).click()
        self.find_element_by_xpath("//input[@name='elofilter']").click()

        self.find_element_by_xpath("//input[@name='elofilter']")

        soup = BeautifulSoup(self.page_source, "html.parser")
        links = soup.select('a[href^="/battle-"]')
        return list("https://play.pokemonshowdown.com"+link["href"] for link in links)

    def download_battle(self, url):
        """Download battle html. Try 10 times."""
        self.get(url)
        for _ in range(10):
            try:
                element = self.find_element_by_partial_link_text("Download")
                element.click()
                return
            except NoSuchElementException:
                sleep(60)
        sleep(2)

@contextmanager
def create_driver(*, headless=True):
    """Returns DriverWrapper. This driver is closed at the end of generator."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    prefs = {"download.default_directory" : os.getcwd()+'/downloads'}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(chrome_options=options)
    driver = DriverWrapper(driver)
    try:
        yield driver
    finally:
        driver.close()

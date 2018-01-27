#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main
"""

from threading import Thread
import zipfile
import os

from . import driver as Driver
from . import battle as Battle


def download_battle(battle):
    """Return function to download a html battle file."""
    def _():
        with Driver.create_driver() as driver:
            driver.download_battle(battle)
    return _

def download_battles(battle_urls, thread_numbers):
    """Download html files concurrently."""
    def chunked(iterable, block):
        """iterableをblock個ごとのlistに分割する"""
        return [iterable[x:x + block] for x in range(0, len(iterable), block)]

    for chunck in chunked(battle_urls[::-1], thread_numbers):
        threads = []
        for battle in chunck:
            threads.append(Thread(target=download_battle(battle)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

def main(battle_format):
    """
    Main method.
    """
    battles = []

    with Driver.create_driver() as driver:
        battles = driver.scrape_battle_urls(battle_format)

    download_battles(battles, THREAD_NUMBERS)

def archive_htmls(file_name):
    htmls = {html for html in os.listdir('./downloads') if 'html' in html}

    with zipfile.ZipFile('./downloads/%s' %file_name, 'w', zipfile.ZIP_STORED) as compFile:
        for html in list(htmls):
            compFile.write('./downloads/'+ html)

if __name__ == '__main__':

    BATTLE_FORMANT = 'gen7vgc2018'
    THREAD_NUMBERS = 4
    # HEADLESS = True

    main(BATTLE_FORMANT)

    # archive_htmls("{0}_{1:%Y%m%d%H%M}.zip".format(BATTLE_FORMANT, datetime.now()))
    HTMLS = {html for html in os.listdir('./downloads') if 'html' in html}
    for h in HTMLS:
        print(Battle.analyze_log('./downloads/'+ h).serialize())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main
"""

from threading import Thread
from driver import create_driver

def download_battle(battle):
    """Return function to download a html battle file."""
    def _():
        with create_driver(headless=False) as driver:
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
        break

def main():
    """
    Main method.
    """

    battle_format = 'gen7vgc2018'
    thread_numbers = 4
    battles = []

    with create_driver() as driver:
        battles = driver.scrape_battle_urls(battle_format)

    download_battles(battles, thread_numbers)

    return battles

if __name__ == '__main__':
    main()

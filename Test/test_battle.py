#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests of battle
"""

import pprint
from unittest import TestCase, main

from battle import BattleLog
from battle import analyze_log

class TestBattleLog(TestCase):

    def test_analyze_log(self):
        """test if a demo html can be restored."""
        log = analyze_log('test/demo.log.html')
        serialized = log.serialize()
        pprint.pprint(BattleLog.deserialize(serialized))

        self.assertEqual(log.winner, "scandal1")
        self.assertEqual(log.average_rating, 1483)
        self.assertEqual(log.teams[0].player, "scandal1")
        self.assertEqual(log.teams[1].player, "Apocalypse94")
        self.assertEqual(log.teams[0].team,
                         ['Accelgor', 'Celesteela', 'Kingdra',
                          'Sceptile', 'Tapu Koko', 'Politoed'])
        self.assertEqual(log.teams[1].team,
                         ['Landorus-Therian', 'Ludicolo', 'Tapu Fini',
                          'Thundurus', 'Zapdos', 'Metagross'])
        self.assertEqual(log.teams[0].rating, 1511)
        self.assertEqual(log.teams[1].rating, 1455)

if __name__ == '__main__':
    main()

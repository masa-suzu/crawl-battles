#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Battle log
"""

import json
from bs4 import BeautifulSoup

class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args':self.args})

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

def analyze_log(path_to_html):
    try:
        with open(path_to_html, 'rb') as html:

            # Ignore multi bytes charactors.
            # html may contains "☆" and "→".
            soup = BeautifulSoup(html.read().decode('ascii', 'ignore'), "html5lib")
            chat = soup.find_all(class_='chat')
            teams = [item.find('em').string
                     for item in chat if '\'s team' in str(item)]
            teams = [t.strip() for t in teams]

            winner = [item.string
                      .replace("won the battle!", "")
                      for item in soup.find_all(class_='battle-history') if ' won the' in str(item)]
            winner = [w.strip() for w in winner]

            # from :  ["Wiampliwarriors'1351", "Rattigan34'1339"]
            # to   : [["Wiampliwarriors", 1351"], ["Rattigan34", "1339"]]
            players = [item.contents[0].replace('s rating: ', "").strip().split('\'')
                       for item in chat if 's rating' in str(item.contents)]
            # from    : [["Wiampliwarriors","1351"],["Rattigan34","1339"]]
            # ratings : ["1351", "1339"]
            # players : ["Wiampliwarriors", "Rattigan34"]
            ratings = [players[0][-1], players[1][-1]]
            players = [players[0][0], players[1][0]]

            log = BattleLog(teams, players, winner[0], ratings)
            return log
    except IndexError:
        return BattleLog([" / ", " / "], ["_NOBADY_", "_NOBADY_"], ["_NOBADY_"], [0, 0])

class BattleLog(Deserializable):
    """Log of a battle"""

    def __init__(self, teams, players, winner, ratings):
        super().__init__(teams, players, winner, ratings)


        self.teams = [
            Team(players[0], teams[0], ratings[0]),
            Team(players[1], teams[1], ratings[1])]
        self.winner = winner
        self.average_rating = sum([int(rating) for rating in ratings])/len(ratings)

    def __repr__(self):
        _repr = str({'winner': self.winner}) + "\r\n"
        _repr += str({'average rating': self.average_rating}) + "\r\n"
        _repr += str(self.teams[0]) + "\r\n"
        _repr += str(self.teams[1])
        return _repr

class Team(object):
    def __init__(self, player, team, rating):
        self.team = [p.strip() for p in sorted(team.split("/"))]
        self.player = player
        self.rating = int(rating)

    def __repr__(self):
        repr = {'player': self.player,
                'team'  : self.team,
                'rating': self.rating}
        return str(repr)

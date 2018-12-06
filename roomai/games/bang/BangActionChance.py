#!/bin/python

from roomai.games.common import AbstractActionChance
from roomai.games.bang import Card
from roomai.games.bang import CharactorCard
from roomai.games.bang import RoleCard

class BangActionChanceType:
    role = "role"
    charactor = "charactor"
    card = "card"

class BangActionChance(AbstractActionChance):
    def __init__(self, card):

        if isinstance(card, Card):

        elif isinstance(card, CharactorCard):

        elif isinstance(card, RoleCard):

        else:
            raise TypeError("card is not Card, CharactorCard or RoleCard")

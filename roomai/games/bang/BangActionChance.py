#!/bin/python

from roomai.games.common import AbstractActionChance

class BangActionChanceRole(AbstractActionChance):
    def __init__(self):
        self.__role__ = ""


    def __get_role__(self): return self.__role__
    role = property(__get_role__, doc="")


class BangActionChanceCharactor(AbstractActionChance):
    def __init__(self):
        self.__charactor__ = ""


class BangActionChanceCard(AbstractActionChance):
    def __init__(self, key):
        self.__card__ =

    def __get_card__(self): return self.__card__

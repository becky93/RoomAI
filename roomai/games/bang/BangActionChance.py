#!/bin/python

from roomai.games.common import AbstractActionChance

class BangActionChanceRole(AbstractActionChance):
    def __init__(self, rolecard):
        self.__role__ = rolecard

    def __get_role__(self): return self.__role__
    role = property(__get_role__, doc="role card")


class BangActionChanceCharactor(AbstractActionChance):
    def __init__(self, charactorcard):
        self.__charactor__ = charactorcard

    def __get_charactor__(self):    return self.__charactor__
    charactor = property(__get_charactor__, doc="charactor card")

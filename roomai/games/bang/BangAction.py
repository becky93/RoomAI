#!/bin/python
#coding:utf-8

from roomai.games.common import AbstractAction

class BangActionCard(AbstractAction):

    def __init__(self):
        self.__card__ = ""
        self.__source__ = ""
        self.__first_target__ = ""
        self.__second_target__ = ""

    @classmethod
    def lookup(self, key):
        raise NotImplementedError

    def __get_card__(self): return self.__card__
    card = property(__get_card__, doc="the normalcard used in this action")

    def __get_source__(self): return self.__source__
    source = property(__get_source__, doc="the id of the player, who issues this action")

    def __get_first_target__(self): return self.__first_target__
    first_target = property(__get_first_target__,doc = "the first target of this action")

    def __get_second_target__(self): return self.__second_target__
    second_target = property(__get_second_target__, doc = "the second target of this action")


class BangActionSkill(AbstractAction):
    def __init__(self):
        self.__skill__ = ""
        self.__from__ = ""
        self.__first_target__ = ""
        self.__second_target__ = ""

    @classmethod
    def lookup(self, key):
        raise NotImplementedError

    def __get_skill__(self): return self.__skill__

    skill = property(__get_skill__, doc="the normalcard used in this action")

    def __get_source__(self): return self.__source__

    source = property(__get_source__, doc="the id of the player, who issues this action")

    def __get_first_target__(self): return self.__first_target__

    first_target = property(__get_first_target__, doc="the first target of this action")

    def __get_second_target__(self): return self.__second_target__

    second_target = property(__get_second_target__, doc="the second target of this action")
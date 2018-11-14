#!/bin/python

from roomai.games.common import AbstractStatePrivate

class BangStatePrivate(AbstractStatePrivate):
    def __init__(self):
        self.__library__ = []


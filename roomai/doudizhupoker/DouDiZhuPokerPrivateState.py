#!/bin/python
import os
import roomai.common
from roomai.doudizhupoker.DouDiZhuPokerAction import DouDiZhuActionElement
from roomai.doudizhupoker.DouDiZhuPokerHandCards import DouDiZhuPokerHandCards
import copy

class DouDiZhuPokerPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        self.__unused_cards__ = DouDiZhuPokerHandCards("")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPokerPrivateState()

        if self.__unused_cards__ is not None:
            newinstance.__unused_cards__ = self.__unused_cards__.__deepcopy__()
        return newinstance

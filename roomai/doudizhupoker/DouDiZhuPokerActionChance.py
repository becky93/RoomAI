#!/bin/python
import os
import roomai.common
import copy


class DouDiZhuPokerActionChance(roomai.common.AbstractActionChance):
    '''
     The DouDiZhuPoker chance action, which is used by the chance palyer. The action contains a key\n
    >> import roomai.doudizhupoker\n
    >> action = roomai.doudizhupoker.SevenKingAction.lookup("5") \n
    >> ## We strongly recommend you to get an action with the lookup function.\n
    >> ## The lookup function inputs a string as the key. The key string needn't be sorted\n
    >> action.key \n
    "5"\n
    '''

    def __init__(self, key):
        self.__key__ = key


    def __get_key__(self):  return self.__key__
    key = property(__get_key__, doc="The key of DouDiZhuPoker action. For example, key = \"3\"")

    @classmethod
    def lookup(cls, key):
        return AllChanceActions["".join(sorted(key))]

    def __deepcopy__(self, memodict={}, newinstance = None):
        return self.lookup(self.key)



############## read data ################
AllChanceActions = dict()
for key in ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2', 'r', 'R']:
    AllChanceActions[key] = DouDiZhuPokerActionChance(key = key)




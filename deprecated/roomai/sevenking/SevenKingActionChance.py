#!/bin/python
import roomai.common
import roomai.sevenking
from roomai.sevenking import AllSevenKingPatterns

from functools import cmp_to_key

class SevenKingActionChance(roomai.common.AbstractActionChance):
    '''
    The SevenKing action. The SevenKing action contains some cards. Examples of usages:\n
    >> import roomai.sevenking\n
    >> action = roomai.sevenking.SevenKingAction.lookup("A_Spade,A_Heart") \n
    >> ## We strongly recommend you to get an action with the lookup function.\n
    >> action.key \n
    "A_Heart, A_Spade"\n
    >> action.cards[0].point\n
    "A"\n
    >> action.cards[0].suit\n
    "Heart"\n
    >> action.pattern\n
    p_2 # There are 2 cards in this action\n
    '''

    def __init__(self, key):
        super(SevenKingActionChance, self).__init__(key)
        self.__key__ = key
        self.__card__ = roomai.common.PokerCard.lookup(key)

    def __get_key__(self):
        return self.__key__

    key = property(__get_key__, doc="The key of this action. For example, the key is \"A_Heart\".")

    def __get_card__(self):
        return self.__card__

    card = property(__get_card__,
                    doc="The card of this action. For example, the card is roomai.common.PokerCard.lookup(\"A_Heart\")")

    @classmethod
    def lookup(cls, key):
        '''
        lookup an action with this specified key

        :param key: The specified key
        :return: The action
        '''
        if key not in AllSevenKingActionChances:
            AllSevenKingActionChances[key] = SevenKingActionChance(key)
        return AllSevenKingActionChances[key]

    def __deepcopy__(self, memodict={}, newinstance=None):
        return SevenKingActionChance.lookup(self.key)


AllSevenKingActionChances = dict()

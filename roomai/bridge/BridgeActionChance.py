#!/bin/python
import roomai.common
import roomai.bridge.BridgeUtils

class BridgeActionChance(roomai.common.AbstractActionChance):
    '''
    The action used by the chance player. The chance action is used for determining the cards the players encounter. 
    Example of usages:\n
    >> import roomai.bridge\n
    >> action = roomai.bridge.KuhnPokerActionChance.lookup("A_Heart")\n
    >> action.key \n
    "A_Heart"\n
    >> action.card.point\n
    "A"\n
    >> action.card.suit\n
    "Heart"\n
    '''

    def __init__(self, key):
        if key not in roomai.bridge.BridgeUtils.AllBridgePlayingPokerCards:
            raise ValueError("The key for BridgeActionChance must be one poker card's key,  in %s"%(",".join(roomai.bridge.BridgeUtils.AllBridgePlayingPokerCards.keys())))

        super(BridgeActionChance, self).__init__(key)
        self.__key__  = key
        self.__card__ = roomai.bridge.BridgePlayingPokerCard.lookup(key)

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the BridgeActionChance action, for example, \"0,1\"")

    def __get_card__(self):
        return self.__card__
    card = property(__get_card__, doc="The poker card will appear for the player.")

    @classmethod
    def lookup(cls, key):
        if key not in AllBridgeActionChances:
            AllBridgeActionChances[key] = BridgeActionChance(key)
        return AllBridgeActionChances[key]

    def __deepcopy__(self, memodict={}, newinstance=None):
        return AllBridgeActionChances.lookup(self.key)

AllBridgeActionChances = dict()
for card in roomai.bridge.BridgeUtils.AllBridgePlayingPokerCards:
    AllBridgeActionChances[card] = BridgeActionChance(card)

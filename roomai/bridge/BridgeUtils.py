#!/bin/python
import roomai.common

point_str_to_rank  = {'A':12, 'K':11, 'Q':10, 'J':9, '10':8, '9':7, '8':6, '7':5, '6':4, '5':3, '4':2, '3':1, '2':0}
point_rank_to_str  = {0:'2', 1:'3', 2:'4',  3:'5', 4:'6',  5:'7',  6:'8',   7:'9', 8:'10',  9:'J',   10:'Q',   11:'K',   12:'A'}
suit_str_to_rank   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3}
suit_rank_to_str   = {0:'Spade', 1: 'Heart', 2: 'Diamond', 3:'Club'}

class BridgePokerCard(roomai.common.PokerCard):
    '''
     A poker card used in Bridge\n
     The suit ranks in the common poker card(roomai.common.PokerCard) and the Bridge poker card(roomai.bridge.BridgePokerCard) are different: \n
     The common poker card: 'Spade': 0, 'Heart':1, 'Diamond':2, 'Club':3
     The Bridge poker card:'Spade': 0, 'Heart': 1, 'Diamond': 2, 'Clud':3
     '''

    def __init__(self, point, suit=None):
        point1 = 0
        suit1 = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1 = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1 = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.__point_str__ = point_rank_to_str[point1]
        self.__suit_str__ = suit_rank_to_str[suit1]
        self.__point_rank__ = point1
        self.__suit_rank__ = suit1
        self.__key__ = "%s_%s" % (self.__point_str__, self.__suit_str__)

    def __deepcopy__(self, memodict={}, newinstance=None):
        return AllBridgePokerCards[self.key]

    @classmethod
    def lookup(cls, key):
        return AllBridgePokerCards[key]


AllBridgePokerCards = dict()
for point_str in point_str_to_rank:
    for suit_str in suit_str_to_rank:
        AllBridgePokerCards["%s_%s" % (point_str, suit_str)] = BridgePokerCard("%s_%s" % (point_str, suit_str))
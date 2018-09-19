import os
import roomai.common
from roomai.doudizhupoker.DouDiZhuPokerAction import DouDiZhuPokerUtil
import copy


AllDouDiZhuPokerHandCards = dict()

class DouDiZhuPokerHandCards:
    '''
    The hand cards in the DouDiZhuPoker game.

    '''

    @classmethod
    def lookup(cls, key):
        if key not in AllDouDiZhuPokerHandCards:
            AllDouDiZhuPokerHandCards[key] = DouDiZhuPokerHandCards(key)
        return AllDouDiZhuPokerHandCards[key]


    def __init__(self, cardstr):
        self.__card_pointrank_count__ = [0 for i in range(DouDiZhuPokerUtil.number_of_pokercards)]
        for c in cardstr:
            idx = DouDiZhuPokerUtil.str_to_rank[c]
            if idx < 0 or idx >= len(self.__card_pointrank_count__):
                xxx = 0
            self.__card_pointrank_count__[idx] += 1
            if idx >= DouDiZhuPokerUtil.number_of_pokercards:
                raise Exception("%s is invalid for a handcard" % (cardstr))

        self.__num_cards__ = sum(self.card_pointrank_count)
        self.__count2num__ = [0 for i in range(5)]
        for count in self.__card_pointrank_count__:
            self.__count2num__[count] += 1

        strs = []
        for h in range(len(self.__card_pointrank_count__)):
            for count in range(self.__card_pointrank_count__[h]):
                strs.append(DouDiZhuPokerUtil.rank_to_str[h])
        strs.sort()
        self.__key__ = "".join(strs)

    def __get_card_pointrank_count__(self):
        return tuple(self.__card_pointrank_count__)

    card_pointrank_count = property(__get_card_pointrank_count__,
                                    doc="The card_pointrank_count is an array of counts for different card point\n" +
                                        "cardpoint_to_rank  = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, 'T':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, 'r':13, 'R':14}.\n" +
                                        "If key = \"33rR\", card_pointrank_count = [2,0,...,0,1,1], len(card_pointrank_count) = 15")

    def __get_num_cards__(self):
        return self.__num_cards__

    num_cards = property(__get_num_cards__,
                         doc="The number of cards in HandCards. For example, key = \"33rR\", num_card = 4")

    def __get_key__(self):
        return self.__key__

    key = property(__get_key__, doc="The key of HandCards. For example, key = \"33rR\". ")

    def __get_count2num__(self):
        return tuple(self.__count2num__)

    count2num = property(__get_count2num__, doc=
    "The count2num is an array of the number of the different counts.\n" +
    "For example, key = \"333rR\", count2num = [0,2,0,1,0]. count2num[1] = 2 denotes that two cards (r and R) appear onces. count2num[3] = 1 that one card(3) appears three times ")

    def __compute_key__(self):
        strs = []
        for h in range(len(self.__card_pointrank_count__)):
            for count in range(self.__card_pointrank_count__[h]):
                strs.append(DouDiZhuPokerUtil.rank_to_str[h])
        strs.sort()
        return "".join(strs)

    def add_cards(self, cards_str):
        return self.lookup("".join(sorted(self.key + cards_str)))

    def remove_cards(self, cards_str):
        card_pointrank_count_list = list(self.card_pointrank_count)
        for c in cards_str:
            pointrank = DouDiZhuPokerUtil.str_to_rank[c]
            card_pointrank_count_list[pointrank] -=1
        str = ""
        for i in range(len(card_pointrank_count_list)):
            for j in range(card_pointrank_count_list[i]):
                str += DouDiZhuPokerUtil.rank_to_str[i]
        return self.lookup("".join(sorted(str)))


    def remove_cards_of_action(self, action):
        str = action.key
        if str == 'x' or str == 'b':
            return
        return self.remove_cards(str)

    def __deepcopy__(self, memodict={}, newinstance=None):
        return self.lookup(self.key)
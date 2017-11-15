#!/bin/python
import roomai.common

class BridgePublicState(roomai.common.AbstractPublicState):
    '''
    The public state of Bridge
    '''
    def __init__(self):
        super(BridgePublicState, self).__init__()
        self.__stage__                    = 0
        self.__candidate_trump__          = None
        self.__trump__                    = None
        self.__candidate_dealerid__       = 0
        self.__dealerid__                 = 0
        self.__cards_on_table__           = []
        self.__real_turn__                = 0
        self.__win_count_sofar__          = [0 for i in range(4)]

    def __get_stage__(self):    return self.__stage__
    stage = property(__get_stage__, doc = " There are two stages: bidding and playing. stage = 0 means the bidding stage, and stage = 1 means the playing biddings stage")

    def __get_candidate_trump__(self): return self.__candidate_trump__
    candidate_trump = property(__get_candidate_trump__, doc="")

    def __get_trump__(self):    return self.__trump__
    trump = property(__get_trump__, doc="")

    def __get_candidate_dealerid__(self):   return self.__candidate_dealerid__
    candidate_dealerid = property(__get_candidate_dealerid__, doc="")

    def __get_dealerid__(self): return self.__dealerid__
    dealerid = property(__get_dealerid__, doc = "")

    def __get_cards_on_table__(self):   return self.__cards_on_table__
    cards_on_table = property(__get_cards_on_table__, doc = "")

    def __get_real_turn__(self):    return self.__real_turn__
    real_turn = property(__get_real_turn__, doc = "")

    def __get_win_count_sofar__(self):    return self.__win_count_sofar__
    win_count_sofar = property(__get_win_count_sofar__, doc = "")

class BridgePersonState(roomai.common.AbstractPersonState):
    '''
    The person state of Bridge
    '''
    def __init__(self):
        super(BridgePersonState, self).__init__()
        self.__hand_cards_dict__ = dict

    def __get_hand_cards_dict__(self):   return roomai.common.FrozenDict(self.__hand_cards_dict__)
    hand_cards_dict = property(__get_hand_cards_dict__, doc = "The hand cards in the corresponding player. For example, \n"
                                                    "hand_cards_dict = {\"A_Heart\":roomai.bridge.BridgePokerCard.lookup(\"A_Heart\"), \"A_Spade\":roomai.bridge.BridgePokerCard.lookup(\"A_Spade\")}")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = BridgePersonState
        newinstance.__hand_cards_dict__ = dict(self.__hand_cards_dict__)
        return newinstance

class BridgePrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of Bridge
    '''
    def __init__(self):
        super(BridgePrivateState, self).__init__()
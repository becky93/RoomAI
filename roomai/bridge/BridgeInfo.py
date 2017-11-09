#!/bin/python
import roomai.common

class BridgePublicState(roomai.common.AbstractPublicState):
    '''
    The public state of Bridge
    '''
    def __init__(self):
        super(BridgePublicState, self).__init__()
        self.__stage__              = 0
        self.__candidate_trump__    = None
        self.__trump__              = None
        self.__candidate_dealerid__ = 0
        self.__dealerid__           = 0

    def __get_stage__(self):    return self.__stage__
    stage = property(__get_stage__, doc = " There are two stages: bidding and playing. stage = 0 means the bidding stage, and stage = 1 means the playing biddings stage")

    def __get_candidate_trump__(self): return self.__candidate_trump__
    candidate_trump = property(__get_candidate_trump__, doc="")

    def __get_trump__(self):    return self.__trump__
    trump = property(__get_trump__, doc="")

    def __get_candidate_dealerid__(self):   return self.__candidate_dealerid__
    candidate_dealerid = property(__get_candidate_dealerid__(), doc="")

    def __get_dealerid__(self): return self.__dealerid__
    dealerid = property(__get_dealerid__, doc = "")

class BridgePersonState(roomai.common.AbstractPersonState):
    '''
    The person state of Bridge
    '''
    def __init__(self):
        super(BridgePersonState, self).__init__()
        self.__hand_cards__ = []

    def __get_hand_cards__(self):   return tuple(self.__hand_cards__)
    hand_cards = property(__get_hand_cards__, doc = "The hand cards in the corresponding player. For example, \n"
                                                    "hand_cards = [roomai.bridge.BridgePokerCard.lookup(\"A_Heart\"), roomai.bridge.BridgePokerCard.lookup(\"A_Spade\")]")


class BridgePrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of Bridge
    '''
    def __init__(self):
        super(BridgePrivateState, self).__init__()
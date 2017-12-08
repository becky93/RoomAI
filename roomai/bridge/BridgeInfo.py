#!/bin/python
import roomai.common

class BridgePublicState(roomai.common.AbstractPublicState):
    '''
    The public state of Bridge
    '''
    def __init__(self):
        super(BridgePublicState, self).__init__()
        self.__stage__                                      = "bidding"

        self.__bidding_candidate_contract_point__           = None
        self.__bidding_candidate_contract_suit__            = None
        self.__bidding_magnification__                      = 1
        self.__bidding_last_bidder__                        = None
        self.__bidding_action_history__                     = []

        self.__playing_is_vulnerable__                      = [False for i in range(4)]
        self.__playing_contract_point__                     = None
        self.__playing_contract_suit__                      = None
        self.__playing_magnification__                      = 1
        self.__playing_dealerid__                           = None
        self.__playing_cards_on_table__                     = []
        self.__playing_real_turn__                          = None
        self.__playing_win_tricks_sofar__                   = [0 for i in range(4)]

    def __get_stage__(self):    return self.__stage__
    stage = property(__get_stage__, doc = " There are two stages: \"bidding\" and \"playing\"")

    ################## bidding stage #####################
    def __get_bidding_candidate_contract_suit__(self): return self.__bidding_candidate_contract_suit__
    bidding_candidate_contract_suit = property(__get_bidding_candidate_contract_suit__, doc="")

    def __get_bidding_candidate_contract_point__(self):    return self.__bidding_candidate_contract_point__
    bidding_candidate_contract_point = property(__get_bidding_candidate_contract_point__, doc="")

    def __get_bidding_magnification__(self):    return self.__bidding_magnification__
    bidding_magnification = property(__get_bidding_magnification__, doc = "In the bidding stage, normally, the magnification = 1. The \"double\" action makes magnification = 2, and the \"redouble\" makes magnification = 4")

    def __get_bidding_last_bidder__(self):   return self.__bidding_last_bidder__
    bidding_last_bidder = property(__get_bidding_last_bidder__, doc="In the bidding stage, the last playerid who lastly takes the \"bid\" action. The bidding_last_bidder is one of [roomai.bridge.Direction.north,roomai.bridge.Direction.east, roomai.bridge.Direction.south,roomai.bridge.Direction.west]. \n"
                                                                    "For example, the bidding_last_bidder = roomai.bridge.Direction.west")

    def __get_bidding_action_history__(self):   return tuple(self.__bidding_action_history__)
    bidding_action_history = property(__get_bidding_action_history__, doc = "The actions taken by different players. For example, bidding_action_history = [roomai.bridge.BridgeAction.lookup(\"bidding_bid_A_heart\"), roomai.bridge.BridgeAction.lookup(\"bidding_pass\"),roomai.bridge.BridgeAction.lookup(\"bidding_pass\")]")

    ########################## playing stage ####################
    def __get_playing_contract_point__(self):    return self.__playing_contract_point__
    playing_contract_point = property(__get_playing_contract_point__, doc="")

    def __get_playing_contract_suit__(self):    return self.__playing_contract_suit__
    playing_contract_suit = property(__get_playing_contract_suit__, doc="")

    def __get_playing_dealerid__(self): return self.__playing_dealerid__
    playing_dealerid = property(__get_playing_dealerid__, doc = "")

    def __get_playing_cards_on_table__(self):   return tuple(self.__playing_cards_on_table__)
    playing_cards_on_table = property(__get_playing_cards_on_table__, doc = "")

    def __get_playing_real_turn__(self):    return self.__playing_real_turn__
    playing_real_turn = property(__get_playing_real_turn__, doc = "")

    def __get_playing_win_tricks_sofar__(self):    return self.__playing_win_tricks_sofar__
    playing_win_tricks_sofar = property(__get_playing_win_tricks_sofar__, doc = "")

    def __get_playing_magnification__(self):    return self.__playing_magnification__
    playing_magnification = property(__get_playing_magnification__, doc ="")

    def __get_playing_is_vulnerable__(self): return self.__playing_is_vulnerable__
    playing_is_vulnerable = property(__get_playing_is_vulnerable__, doc = "")

class BridgePersonState(roomai.common.AbstractPersonState):
    '''
    The person state of Bridge
    '''
    def __init__(self):
        super(BridgePersonState, self).__init__()
        self.__hand_cards_dict__ = dict()

    def __get_hand_cards_dict__(self):   return roomai.common.FrozenDict(self.__hand_cards_dict__)
    hand_cards_dict = property(__get_hand_cards_dict__, doc = "The hand cards in the corresponding player. \n"
                                                              "For example, hand_cards_dict = {\"A_Heart\":roomai.bridge.BridgePokerCard.lookup(\"A_Heart\"), \"A_Spade\":roomai.bridge.BridgePokerCard.lookup(\"A_Spade\")}")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = BridgePersonState()
        newinstance.__hand_cards_dict__ = dict(self.__hand_cards_dict__)
        return newinstance

class BridgePrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of Bridge
    '''
    def __init__(self):
        super(BridgePrivateState, self).__init__()
#!/bin/python
import roomai.common

class BridgeAction(roomai.common.AbstractAction):
    '''
    The action of Bridge. There are two stages:1) bidding and 2) playing. \n
    In the bidding stages, players \n
    In the playing stages, players \n
    The example of the Bridge action's usages:\n
    >>action = roomai.bridge.BridgeAction.lookup("bidding_A_Heart")\n
    ## We strongly recommend you to use the lookup fuction to get an action \n
    >>action.key \n
    "bidding_bid_A_Heart"\n
    >>action.stage \n
    0
    # 0 means bidding, 1 means playing
    >>action.card.key \n
    "A_Heart"\n
    >>action.card.point \n
    "A"\n
    >>action.card.suit  \n
    "Heart"\n
    >>action.card.point_rank \n
    12\n
    >>action.card.suit_rank \n
    1
    '''

    def __init__(self, stage, option, bridgepokercard):
        super(BridgeAction, self).__init__()
        self.__stage__  = stage
        self.__option__ = option
        self.__card__   = bridgepokercard

        if self.__stage__ == 0:
            if self.__option__ == "bid":
                self.__key__ = "bidding_" + self.__option__+"_" + bridgepokercard.key
            else:
                self.__key__ = "bidding_" + self.__option__
        elif self.__stage__ == 1:
            self.__key__ = "playing_" + bridgepokercard.key
        else:
            raise ValueError("The stage param must be 0 or 1.")


    def __get_key__(self): return self.__key__
    key = property(__get_key__, doc="The key of the Bridge action. For example, \n"
                                     ">>action = roomai.bridge.BridgeAction.lookup(\"bidding_bid_A_Heart\")\n"
                                     ">>action.key\n"
                                    "\"bidding_bid_A_Heart\"\n"
                                    "## bidding means the bidding stage, bid means the bid option, A_Heart means the bidding card")

    def __get_stage__(self): return self.__stage__
    stage = property(__get_stage__, doc = "The stage of Bridge. For example, \n"
                                          ">>action = room.bridge_BridgeAction.lookup(\"playing_A_Heart\")\n"
                                          ">>action.stage\n"
                                          "0 # 0 means the bidding stage and 1 means the playing stage")

    def __get_option__(self):   return self.__option__
    option = property(__get_option__, doc = "When stage == 0 (the bidding stage), the option is one of \"bid\",\"double\",\"redouble\" and \"pass\".\n"
                                            "When stage == 1 (the playing stage), the option is always None")

    def __get_card__(self): return self.__card__
    card = property(__get_card__, doc="The card in this Bridge action. For example, \n"
                                      ">>action = roomai.bridge.BridgeAction.lookup(\"playing_A_Heart\")\n"
                                      ">>action.card.key \n"
                                      "\"A_Heart\"\n"
                                      ">>action.card.point \n"
                                      "\"A\"\n"
                                      ">>action.card.suit  \n"
                                      "\"Heart\"\n"
                                      ">>action.card.point_rank \n"
                                      "12\n"
                                      ">>action.card.suit_rank \n"
                                      "1")


    def __deepcopy__(self, memodict={}, newinstance = None):
        return AllBridgeActions[self.key]

    def lookup(self, key):
        '''
        lookup an action with the key
        
        :param key: the key of the targeted action
        :return: the action with this key
        '''
        if key not in AllBridgeActions:
            AllBridgeActions[key] = BridgeAction(key)
        return AllBridgeActions[key]


AllBridgeActions = dict()
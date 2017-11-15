#!/bin/python
import roomai.common
import roomai.bridge

class BridgeAction(roomai.common.AbstractAction):
    '''
    The action of Bridge. There are two stages:1) bidding and 2) playing. \n
    In the bidding stages, players \n
    In the playing stages, players \n
    The example of the Bridge action's usages:\n
    >>action = roomai.bridge.BridgeAction.lookup("bidding_A_Heart")\n
    ## We strongly recommend you to use the lookup fuction to get an action \n
    >>action.key \n
    "bidding_A_Heart"\n
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

    def __init__(self, stage, bridgepokercard):

        if stage == 0:
            key = "bidding_" + bridgepokercard.key
        elif stage == 1:
            key = "playing_" + bridgepokercard.key
        else:
            raise ValueError("The stage param must be 0 or 1.")

        super(BridgeAction, self).__init__(key=key)

        self.__stage__ = stage
        self.__card__  = bridgepokercard



    def __get_key__(self): return self.__key__
    key = property(__get_key__, doc="The key of the Bridge action. For example, \n"
                                     ">>action = roomai.bridge.BridgeAction.lookup(\"bidding_A_Heart\")\n"
                                     ">>action.key\n"
                                    "\"bidding_A_Heart\"")

    def __get_stage__(self): return self.__stage__
    stage = property(__get_stage__, doc = "The stage of Bridge. For example, \n"
                                          ">>action = room.bridge_BridgeAction.lookup(\"playing_A_Heart\")\n"
                                          ">>action.stage\n"
                                          "0 # 0 means the bidding stage and 1 means the playing stage")

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

    @classmethod
    def lookup(self, key):
        '''
        lookup an action with the key
        
        :param key: the key of the targeted action
        :return: the action with this key
        '''
        if key not in AllBridgeActions:
            stage = 0
            card  = ""
            if "bidding" in key:
                stage = 0
                card  = roomai.bridge.BridgePokerCard.lookup(key.replace("bidding_",""))
            elif "playing" in key:
                stage = 1
                card  = roomai.bridge.BridgePokerCard.lookup(key.replace("playing_",""))
            else:
                raise ValueError("%s is an invalid key"%(key))

            AllBridgeActions[key] = BridgeAction(stage, card)
        return AllBridgeActions[key]


AllBridgeActions = dict()
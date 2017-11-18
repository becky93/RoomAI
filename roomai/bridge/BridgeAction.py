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

    def __init__(self, stage, bidding_option, bidding_point, bidding_suit, playing_pokercard):
        self.__stage__  = stage
        self.__bidding_option__      = bidding_option
        self.__bidding_point__       = bidding_point
        self.__bidding_suit__        = bidding_suit
        self.__playing_pokercard__   = playing_pokercard

        key = None
        if self.__stage__ == "bidding":
            if self.__bidding_option__ == "bid":
                key= "bidding_" + self.__bidding_option__+"_" + str(self.__bidding_point__) + "_" + str(self.__bidding_suit__)
            else:
                key = "bidding_" + self.__bidding_option__
        elif self.__stage__ == "playing":
            key = "playing_" + self.__playing_pokercard__.key
        else:
            raise ValueError("The stage param must be \"bidding\" or \"playing\"")

        super(BridgeAction, self).__init__(key=key)


    def __get_key__(self): return self.__key__
    key = property(__get_key__, doc="The key of the Bridge action. For example, \n"
                                     ">>action = roomai.bridge.BridgeAction.lookup(\"bidding_bid_1_Heart\")\n"
                                     ">>action.key\n"
                                    "\"bidding_bid_A_Heart\"\n"
                                    "## bidding means the bidding stage, bid means the bid option, 1 means the 1 card point, Heart means the card suit")

    def __get_stage__(self): return self.__stage__
    stage = property(__get_stage__, doc = "The stage of Bridge. For example, \n"
                                          ">>action = room.bridge_BridgeAction.lookup(\"playing_A_Heart\")\n"
                                          ">>action.stage\n"
                                          "\"playing\"")

    def __get_bidding_option__(self):   return self.__bidding_option__
    bidding_option = property(__get_bidding_option__, doc = "When stage = \"bidding\", the bidding_option is one of \"bid\",\"double\",\"redouble\" and \"pass\".\n"
                                                            "When stage = \"playing\", the bidding_option is always None")

    def __get_bidding_point__(self):   return self.__bidding_point__
    bidding_point = property(__get_bidding_option__, doc = "When stage = \"bidding\" and bidding_option = \"bid\", the bidding_point is one of 1,2,3,4,5,6 and 7.\n"
                                                           "When stage = \"bidding\" and bidding_option != \"bid\",the bidding_option is always None\n"
                                                           "When stage = \"playing\", the bidding_point is always None")

    def __get_bidding_suit__(self):   return self.__bidding_suit__
    bidding_suit = property(__get_bidding_option__, doc = "When stage = \"bidding\" and bidding_option = \"bid\", the bidding_suit is one of \"NotTrump\",\"Spade\",\"Heart\", \"Diamond\" and \"Club\".\n"
                                                          "When stage = \"bidding\" and bidding_option != \"bid\", the bidding_suit is always None\n"
                                                          "when stage == \"playing\", the bidding_suit is always None")

    def __get_playing_card__(self): return self.playing_card
    playing_card = property(__get_playing_card__, doc="When stage == \"bidding\", the playing_card always be None\n"
                                            "When stage = \"playing\", the playing_card is the card in this Bridge action. For example, \n"
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
            stage = "bidding"
            bidding_option =  None
            bidding_point  =  None
            bidding_suit   =  None
            playing_card   =  None

            if "bidding" in key:
                stage  = "bidding"
                lines  = key.split("_")
                bidding_option = lines[1]
                if bidding_point == "bid":
                    bidding_point  = lines[2]
                    bidding_suit   = lines[3]
                else:
                    card  = None
            elif "playing" in key:
                stage          = "playing"
                playing_card   = roomai.bridge.BridgeBidPokerCard.lookup(key.replace("playing_", ""))
            else:
                raise ValueError("%s is an invalid key"%(key))

            AllBridgeActions[key] = BridgeAction(stage, bidding_option, bidding_point, bidding_suit, playing_card)
        return AllBridgeActions[key]


AllBridgeActions = dict()
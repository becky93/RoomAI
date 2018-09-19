#!/bin/python
import roomai.common
import roomai.bridge.BridgeUtils

class BridgePrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of Bridge
    '''
    def __init__(self):
        super(BridgePrivateState, self).__init__()
        self.__unseen_cards__ = set(roomai.bridge.BridgeUtils.AllBridgePlayingPokerCards.keys())
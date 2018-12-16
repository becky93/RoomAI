#!/bin/python
import roomai.games.common

class KuhnPokerPrivateState(roomai.games.common.AbstractStatePrivate):
    '''
    The private state class of KuhnPoker
    '''
    def __deepcopy__(self, memodict={}):
        return AKuhnPokerPrivateState
AKuhnPokerPrivateState = KuhnPokerPrivateState()
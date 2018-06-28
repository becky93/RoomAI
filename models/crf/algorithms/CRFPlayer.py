#!/bin/python
import roomai.common
import random
import copy

class CRFPlayer(roomai.common.AbstractPlayer):
    def gen_state(self,info):
        raise NotImplementedError("Not Implemented Yet")
    def update_averge_strategies(self, state, actions, targets):
        raise NotImplementedError("Not Implemented Yet")
    def get_averge_strategies(self, state, actions):
        raise NotImplementedError("Not Implemented Yet")
    def update_current_regrets(self, state, actions, targets):
        raise NotImplementedError("Not Implemented Yet")
    def get_current_regrets(self, state, actions):
        raise NotImplementedError("Not Implemented Yet")



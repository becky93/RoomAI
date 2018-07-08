#!/bin/python
import roomai.common
import random
import copy

class CRFPlayer(roomai.common.AbstractPlayer):
    def update_averge_strategies(self, info, actions, targets):
        raise NotImplementedError("Not Implemented Yet")

    def get_averge_strategies(self, info, actions):
        raise NotImplementedError("Not Implemented Yet")

    def update_counterfactual_values(self, info, actions, targets):
        raise NotImplementedError("Not Implemented Yet")

    def get_counterfactual_values(self, info, actions):
        raise NotImplementedError("Not Implemented Yet")



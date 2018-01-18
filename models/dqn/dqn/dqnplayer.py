#!/bin/python
import roomai
import roomai.common

class DqnPlayer(roomai.common.AbstractPlayer):
    def __init__(self, model):
        self.dqn_model = model

    def receive_info(self, info):
        self.info = info

    def take_action(self):
        return self.dqn_model.take_action(self.info)

    def reset(self):
        pass




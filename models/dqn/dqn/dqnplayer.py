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

    def terminal_info_feat(self):
        raise NotImplementedError("Not implemented yet")

    def terminal_action_feat(self):
        raise NotImplementedError("Not implemented yet")

    def gen_info_feat(self, info):
        raise NotImplementedError("Not implemented yet")

    def gen_action_feat(self, info, action):
        raise NotImplementedError("Not implemented yet")

    def update_model(self, experiences):
        raise NotImplemented("Not implemented yet")

    def take_action(self, info):
        raise NotImplementedError("Not implemented yet")



#!/bin/python
import roomai
import roomai.common

class DQNModel:
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




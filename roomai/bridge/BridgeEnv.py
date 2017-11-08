#!/bin/python
import roomai.common
import random

class BridgeEnv(roomai.common.AbstractEnv):
    def init(self, params =dict()):
        super(BridgeEnv, self).__init__(dict)

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 4)

        self.public_state  = roomai.bridge.BridgePublicState()
        self.person_states = [roomai.bridge.BridgePersonState() for i in range(4)]
        self.private_state = roomai.bridge.BridgePrivate()

    def forward(self, action):

        if self.public_state.stage == 0: ## the bidding stage
            pass
        elif self.public_state.stage == 1: ## the playing stage
            pass
        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))


        self.__gen_history__()
        return self.__gen_infos__()

    @classmethod
    def available_actions(self, public_state, person_state):
        if self.public_state.stage == 0: ## the bidding stage
            pass
        elif self.public_state.stage == 1: ## the playing stage
            pass
        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))



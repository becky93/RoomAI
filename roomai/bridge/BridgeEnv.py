#!/bin/python
import roomai.common
import roomai.bridge
import random


class BridgeEnv(roomai.common.AbstractEnv):
    def init(self, params =dict()):
        super(BridgeEnv, self).__init__(dict)

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 4)

        self.public_state  = roomai.bridge.BridgePublicState()
        self.public_state.__stage__ = 0

        self.person_states = [roomai.bridge.BridgePersonState() for i in range(4)]
        len = len(roomai.bridge.AllBridgePokerCards) / 4
        for i in range(4):
            self.person_states[i].__hand_cards__ = roomai.bridge.AllBridgePokerCards[i*len:(i+1)*len]

        self.private_state = roomai.bridge.BridgePrivate()

    def forward(self, action):
        pu  = self.public_state
        pes = self.person_states
        pr  = self.private_state
        if self.is_action_valid(action, pu, pes[pu.turn]):
            raise ValueError("%s is invalid action"%(action.key))
        pes[pu.turn].__available_actions__ = dict()

        if self.public_state.stage == 0: ## the bidding stage
            pass

        elif self.public_state.stage == 1: ## the playing stage
            pass

        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))


        self.__gen_history__()
        return self.__gen_infos__()

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        return action.key in person_state.available_actions

    @classmethod
    def available_actions(self, public_state, person_state):
        if public_state.stage == 0: ## the bidding stage
            available_actions = dict()
            if public_state.candidate_trump is None:
                for card in roomai.bridge.AllBridgePokerCards:
                    key = "bidding_%s"%(card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            else:
                for card in roomai.bridge.AllBridgePokerCards:
                    if card.compare(card, public_state.candidate_trump) > 0:
                        key = "bidding_%s" % (card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            return available_actions

        elif public_state.stage == 1: ## the playing stage
            available_actions = dict()
            if public_state.cards_on_table == []:
                for card in person_state.hand_cards:
                    key = "playing_%s"%(card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            else:
                for card in person_state.hand_cards:
                    if card.suit == public_state.cards_on_table[0].suit:
                        key = "playing_%s" % (card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
                if len(available_actions) == 0:
                    for card in person_state.hand_cards:
                        key = "playing_%s" % (card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            return available_actions

        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))



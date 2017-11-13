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
            self.person_states[i].__hand_cards_dict__ = dict()
            for card in roomai.bridge.AllBridgePokerCards[i*len:(i+1)*len]:
                self.person_states[i].__hand_cards_dict__[card.key] = card

        self.private_state = roomai.bridge.BridgePrivate()

    def forward(self, action):
        pu  = self.public_state
        pes = self.person_states
        pr  = self.private_state
        if self.is_action_valid(action, pu, pes[pu.turn]):
            raise ValueError("%s is invalid action"%(action.key))
        pes[pu.turn].__available_actions__ = dict()

        if pu.stage == 0: ## the bidding stage
            pu.cards_on_table.append(action.card)
            if len(pu.cards_on_table) == 1:
                pu.__candidate_dealerid__  = pu.turn
                pu.__candidate_trump__     = action.card
            if len(pu.cards_on_table) == 2 or len(pu.cards_on_table) == 3:
                if roomai.bridge.BridgePokerCard.compare(action.card, pu.candidate_trump) > 0:
                    pu.__candidate_dealerid__ = pu.turn
                    pu.__candidate_trump__    = action.card
            if len(pu.cards_on_table) == 4:
                if roomai.bridge.BridgePokerCard.compare(action.card, pu.candidate_trump) > 0:
                    pu.__candidate_dealerid__ = pu.turn
                    pu.__candidate_trump__    = action.card
                pu.__stage__          = 0
                pu.__cards_on_table__ = []
                pu.__turn__           = pu.candidate_dealerid
                pu.__real_turn__      = pu.turn
                pu.__dealerid__       = pu.candidate_dealerid
                pu.__trump__          = pu.candidate_trump

        elif pu.stage == 1: ## the playing stage
            pu.cards_on_table.append(action.card)
            self.__remove_card_from_hand_cards__(pes[pu.real_turn], action.card)

            if len(pu.cards_on_table) == 4:
                playerid1,playerid2 = self.__compute_winner__()
                pu.__win_count_sofar__[playerid1] += 1
                pu.__win_count_sofar__[playerid2] += 1
                if len(pes[pu.real_turn].hand_cards) == 0:
                    pu.__is_terminal__ = True
                    if pu.win_count_sofar[pu.dealerid] > pu.win_count_sofar[(pu.dealerid + 1)%4] + pu.trump.point_rank:
                        pu.__scores__ = [-1,-1,-1,-1]
                        pu.__scores__[pu.dealerid] = 1
                        pu.__scores__[(pu.dealerid+2)%4] = 1
                    else:
                        pu.__scores__ = [1,1,1,1]
                        pu.__scores__[pu.dealerid] = -1
                        pu.__scores__[(pu.dealerid+2)%4] = -1


        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))


        self.__gen_history__()
        return self.__gen_infos__()

    def __remove_card_from_hand_cards__(self, person_state, card):
        del person_state.__hand_cards_dict__[card.key]

    def __compare_card_with_trump__(self, card1, card2, trump):
        if card1.suit == trump.suit and card2.suit == trump.suit:
            return roomai.bridge.BridgePokerCard.compare(card1,card2)
        elif card1.suit == trump.suit and card2.suit != trump.suit:
            return 1
        elif card1.suit != trump.suit and card2.suit == trump.suit:
            return -1
        else:
            return roomai.bridge.BridgePokerCard.compare(card1, card2)

    def __compute_winner__(self, pu):
        pass


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
            raise ValueError("The public_state.stage = %d is invalid. The public_state.stage = 0 means the bidding stage, The public_state.stage = 1 means the playing stage"%(self.public_state.stage))



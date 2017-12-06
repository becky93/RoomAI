#!/bin/python
import roomai.common
import roomai.bridge
import random


class BridgeEnv(roomai.common.AbstractEnv):
    '''
    The Bridge game environment
    '''


    def init(self, params = dict()):

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 4)

        if "allcards" in params:
            self.__params__["allcards"] = list(params["allcards"])
        else:
            self.__params__["allcards"] = list(roomai.bridge.AllBridgePokerCards.values())
            random.shuffle(self.__params__["allcards"])

        if "vulnerable" in params:
            self.__params__["vulnerable"] = list(params["vulnerable"])
        else:
            self.__params__["vulnerable"] = [False for i in range(4)]


        self.public_state                        = roomai.bridge.BridgePublicState()
        self.public_state.__stage__              = "bidding"
        self.public_state.__turn__               = self.__params__["start_turn"]
        self.public_state.__playing_is_vulnerable__ = list(self.__params__["vulnerable"])

        self.person_states = [roomai.bridge.BridgePersonState() for i in range(4)]
        num = int(len(roomai.bridge.AllBridgePokerCards) / 4)
        for i in range(4):
            self.person_states[i].__hand_cards_dict__ = dict()
            for card in self.__params__["allcards"][i*num:(i+1)*num]:
                self.person_states[i].__hand_cards_dict__[card.key] = card
        self.person_states[self.public_state.turn].__available_actions__ \
            = self.available_actions(self.public_state, self.person_states[self.public_state.turn])


        self.private_state = roomai.bridge.BridgePrivateState()

        self.__gen_history__()
        return self.__gen_infos__(), self.public_state, self.person_states, self.private_state

    def forward(self, action):
        '''
        The Bridge game go forward with this action
        
        :param action: 
        :return: 
        '''

        pu  = self.public_state
        pes = self.person_states
        pr  = self.private_state
        if self.is_action_valid(action, pu, pes[pu.turn]) == False:
            raise ValueError("%s is invalid action"%(action.key))
        pes[pu.turn].__available_actions__ = dict()

        if pu.stage == "bidding": ## the bidding stage
            pu.__bidding_action_history__.append(action)
            if len(pu.bidding_action_history) == 4:
                flag = True
                for i in range(4):
                    flag = flag and (pu.bidding_action_history[i].bidding_option == "pass")
                if flag == True:
                    pu.__is_terminal__ = True
                    pu.__scores__      = [0,0,0,0]
                    self.__gen_history__()
                    return self.__gen_infos__(), self.public_state, self.person_states, self.private_state

            if action.bidding_option == "pass":
                if len(pu.bidding_action_history) > 3 \
                    and pu.bidding_action_history[-2].bidding_option == "pass"\
                    and pu.bidding_action_history[-3].bidding_option == "pass":
                        self.__bidding_to_playing__(action)
                else:
                    self.__bidding_process_pass__(action)
            elif action.bidding_option == "bid":
                self.__bidding_process_bid__(action)
            elif action.bidding_option == "double":
                self.__bidding_process_double__(action)
            elif action.bidding_option == "redouble":
                self.__bidding_process_redouble__(action)
            else:
                raise  ValueError("In the bidding stage, the action's bidding_option must be one of \"pass\",\"bid\",\"double\" and \"redouble\". But a \"%s\" action is found"%(action.key))


        elif pu.stage == "playing": ## the playing stage
            pu.__playing_cards_on_table__.append(action.playing_card)
            self.__remove_card_from_hand_cards__(pes[pu.playing_real_turn], action.playing_card)

            if len(pu.playing_cards_on_table) == 4:
                playerid1,playerid2 = self.__whois_winner_per_pier__(pu)
                pu.__playing_win_tricks_sofar__[playerid1] += 1
                pu.__playing_win_tricks_sofar__[playerid2] += 1
                pu.__playing_cards_on_table__ = []
                if len(pes[pu.playing_real_turn].hand_cards_dict) == 0:
                    pu.__is_terminal__ = True
                    self.__compute_score__()
                else:
                    pes[pu.turn].__available_actions__ = BridgeEnv.available_actions(public_state= pu, person_state=pes[pu.playing_real_turn])
            else:
                pu.__playing_real_turn__ = (pu.__playing_real_turn__ + 1) % 4
                if pu.playing_real_turn == pu.playing_dealerid:
                    pu.__turn__ = (pu.playing_real_turn + 2) % 4
                else:
                    pu.__turn__ = pu.playing_real_turn
                pes[pu.turn].__available_actions__ = BridgeEnv.available_actions(public_state=pu,person_state=pes[pu.playing_real_turn])



        else:
            raise ValueError("The public_state.stage = %d is invalid"%(self.public_state.stage))


        self.__gen_history__()
        return self.__gen_infos__(), self.public_state,self.person_states, self.private_state

    def __remove_card_from_hand_cards__(self, person_state, card):
        del person_state.__hand_cards_dict__[card.key]

    def __compare_card_with_contract_suit__(self, card1, card2, contract_suit):
        if card1.suit == contract_suit and card2.suit == contract_suit:
            return roomai.bridge.BridgePokerCard.compare(card1, card2)
        elif card1.suit == contract_suit and card2.suit != contract_suit:
            return 1
        elif card1.suit != contract_suit and card2.suit == contract_suit:
            return -1
        else:
            return roomai.bridge.BridgePokerCard.compare(card1, card2)

    def __compute_score__(self):
        pu = self.public_state
        pu.__scores__ = [0, 0, 0, 0]
        playing_point_rank = roomai.bridge.contract_point_to_rank[pu.playing_contract_point]

        if pu.playing_win_tricks_sofar[pu.playing_dealerid] - pu.playing_win_tricks_sofar[(pu.playing_dealerid+1)%4] >= 6 + playing_point_rank:

            ####
            excessive_tricks = pu.playing_win_tricks_sofar[pu.playing_dealerid] - pu.playing_win_tricks_sofar[(pu.playing_dealerid+1)%4] - 6 - playing_point_rank
            tricks_score     = 0
            if pu.playing_contract_suit == "NotTrump":
                tricks_score = (excessive_tricks * 30 + 10) * pu.playing_magnification
            elif pu.playing_contract_suit == "Spade" or pu.playing_contract_suit == "Heart":
                tricks_score = excessive_tricks * 30 * pu.playing_magnification
            elif pu.playing_contract_suit == 'Diamond' or pu.playing_contract_suit == 'Club':
                tricks_score = excessive_tricks * 20
            else:
                raise ValueError("%s is not valid playing_contract_suit (NotTrump, Spade, Heart, Diamond, Club)"%(pu.playing_contract_suit))
            pu.__scores__[pu.playing_dealerid] = tricks_score
            pu.__scores__[(pu.playing_dealerid + 2)%4] = tricks_score

            ####
            case_type = 1
            if tricks_score < 100:
                case_type = 1
            else:
                case_type = 2
            if playing_point_rank == 6:
                case_type = 3
            if playing_point_rank == 7:
                case_type = 4
            additive_score = 0
            if pu.playing_is_vulnerable[pu.playing_dealerid] == True:
                if case_type == 1:
                    additive_score = 50
                elif case_type == 2:
                    additive_score = 500
                elif case_type == 3:
                    additive_score = 750
                elif case_type == 4:
                    additive_score = 1500
            else:
                if case_type == 1:
                    additive_score = 50
                elif case_type == 2:
                    additive_score = 300
                elif case_type == 3:
                    additive_score = 500
                elif case_type == 4:
                    additive_score = 1000
            pu.__scores__[pu.playing_dealerid] += additive_score
            pu.__scores__[(pu.playing_dealerid + 2) % 4] += additive_score

            #####
            additive_score1 = 0
            if pu.playing_magnification > 1:
                if pu.playing_is_vulnerable[pu.playing_dealerid] == True:
                    additive_score1 = excessive_tricks * pu.playing_magnification
                else:
                    additive_score1 = excessive_tricks * (pu.playing_magnification-1)
                if pu.playing_magnification == 1:
                    additive_score1 += 50
                elif pu.playing_magnification == 2:
                    additive_score1 += 100
                pu.__scores__[pu.playing_dealerid] += additive_score1
                pu.__scores__[(pu.playing_dealerid + 2) % 4] += additive_score1


        else:
            penalty_trick = -(pu.playing_win_tricks_sofar[pu.playing_dealerid] - pu.playing_win_tricks_sofar[(pu.playing_dealerid+1)%4] - 6 - playing_point_rank
        )
            penalty_score = 0
            if pu.playing_is_vulnerable[(pu.playing_dealerid + 1)%4] == True:
                penalty_score = penalty_trick * 100 * pu.playing_magnification
            else:
                penalty_score = penalty_trick * 50 * pu.playing_magnification

            pu.__scores__[(pu.playing_dealerid+1)%4] += penalty_score
            pu.__scores__[(pu.playing_dealerid+3)%4] += penalty_score



    def __whois_winner_per_pier__(self, pu):
        max_id   = 0
        max_card = pu.playing_cards_on_table[0]
        for i in range(1,4):
            if self.__compare_card_with_contract_suit__(max_card, pu.playing_cards_on_table[i], pu.playing_contract_suit):
                max_id   = i
                max_card = pu.playing_cards_on_table[i]

        return max_id, (max_id + 2)%4

    def __bidding_process_pass__(self, action):
        pu = self.public_state

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_double__(self, action):
        pu = self.public_state
        pu.__bidding_magnification__ = 2

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_redouble__(self, action):
        pu = self.public_state
        pu.__bidding_magnification__ = 4

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_process_bid__(self, action):
        pu = self.public_state
        pu.__bidding_candidate_contract_point__ = action.bidding_contract_point
        pu.__bidding_candidate_contract_suit__ = action.bidding_contract_suit
        pu.__bidding_last_bidder__ = pu.turn
        pu.__bidding_magnification__ = 1

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = (pu.turn + 1) % 4

        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])

    def __bidding_to_playing__(self, action):
        pu = self.public_state
        pu.__stage__                  = "playing"
        pu.__playing_contract_point__ = pu.bidding_candidate_contract_point
        pu.__playing_contract_suit__  = pu.bidding_candidate_contract_suit

        start_turn  = self.__params__["start_turn"]
        last_bidder = pu.bidding_last_bidder
        for i in range(len(pu.bidding_action_history)):
            if (i+start_turn)%4 == last_bidder or (i + start_turn + 2) % 4 == last_bidder:
                if pu.bidding_action_history[i].bidding_option == "bid" \
                        and pu.bidding_action_history[i].bidding_contract_suit == pu.playing_contract_suit:
                    pu.__playing_dealerid__ = i
                    break

        pu.__previous_id__ = pu.turn
        pu.__previous_action__ = action
        pu.__turn__ = pu.playing_dealerid
        pu.__playing_real_turn__ = pu.playing_dealerid
        self.person_states[pu.turn].__available_actions__ = self.available_actions(pu,self.person_states[pu.turn])


    @classmethod
    def __available_contract__(self, pu, point, suit):
        if point not in roomai.bridge.contract_point_to_rank:
            raise  ValueError("The contract point must be one of (%s)"%(",".join(list(roomai.bridge.contract_point_to_rank.keys()))))
        if suit not in  roomai.bridge.contract_suit_to_rank:
            raise  ValueError("The contract suit must be one of (%s)"%(",".join(list(roomai.bridge.contract_suit_to_rank.keys()))))
        suit_rank  = roomai.bridge.contract_suit_to_rank[suit]
        point_rank = roomai.bridge.contract_point_to_rank[point]

        if pu.bidding_candidate_contract_point is None:
            return True
        elif point_rank > roomai.bridge.contract_point_to_rank[pu.bidding_candidate_contract_point]:
            return True
        elif point_rank == roomai.bridge.contract_point_to_rank[pu.bidding_candidate_contract_point]:
            if suit_rank > roomai.bridge.contract_suit_to_rank[pu.bidding_candidate_contract_suit]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        return action.key in person_state.available_actions

    @classmethod
    def available_actions(cls, public_state, person_state):
        if public_state.stage == "bidding": ## the bidding stage
            available_actions = dict()
            for point in roomai.bridge.contract_point_to_rank:
                for suit in roomai.bridge.contract_suit_to_rank:
                    if BridgeEnv.__available_contract__(public_state, point, suit) == True:
                        key = "bidding_bid_%s_%s"%(point, suit)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            available_actions["bidding_pass"] = roomai.bridge.BridgeAction.lookup("bidding_pass")

            if len(public_state.__bidding_action_history__) >= 1:
                pre_action  = public_state.__bidding_action_history__[-1]
                if pre_action.bidding_option == "bid":
                    key = "bidding_double"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

                if pre_action.bidding_option == "double":
                    key = "bidding_redouble"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            if len(public_state.__bidding_action_history__) >= 3:
                pre_action1 = public_state.__bidding_action_history__[-1]
                pre_action2 = public_state.__bidding_action_history__[-2]
                pre_action3 = public_state.__bidding_action_history__[-3]
                if pre_action3.bidding_option == "bid" and pre_action2.bidding_option == "pass" and pre_action1.bidding_option == "pass":
                    key = "bidding_double"
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            return available_actions


        elif public_state.stage == "playing": ## the playing stage
            available_actions = dict()
            if public_state.playing_cards_on_table == tuple([]) or public_state.playing_cards_on_table is None:
                for card in list(person_state.hand_cards_dict.values()):
                    key = "playing_%s"%(card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)
            else:
                for card in person_state.hand_cards_dict.values():
                    if len(public_state.playing_cards_on_table) == 0:
                        x = 0
                    if card.suit == public_state.playing_cards_on_table[0].suit:
                        key = "playing_%s" % (card.key)
                        available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            if len(available_actions) == 0:
                for card in person_state.hand_cards_dict.values():
                    key = "playing_%s" % (card.key)
                    available_actions[key] = roomai.bridge.BridgeAction.lookup(key)

            return available_actions

        else:
            raise ValueError("The public_state.stage = %s is invalid. The public_state.stage must be one of [\"bidding\",\"playing\"]"%(public_state.stage))



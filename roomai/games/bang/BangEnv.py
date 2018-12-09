#!/bin/python
import roomai
import random


import roomai
from roomai.games.common import AbstractEnv
from roomai.games.bang   import BangActionChance
from roomai.games.bang   import BangStatePublic
from roomai.games.bang   import BangStatePrivate
from roomai.games.bang   import BangStatePerson
from roomai.games.bang   import PublicPersonInfo
from roomai.games.bang   import CharactorCardsDict

class BangEnv(AbstractEnv):


    def init(self, params = dict()):
        '''
        Initialize the TexasHoldem game environment with the initialization params.\n
        The initialization is a dict with only an option: \n
        param_num_normal_players: how many players are in the game, the option must be in {2, 4, 5}, default 5. An example of the initialization param is {"param_num_normal_players":2} \n
        
        :param params: the initialization params
        :return: infos, public_state, person_states, private_state
        '''


        logger         = roomai.get_logger()
        public_state   = BangStatePublic()
        private_state  = BangStatePrivate()

        if "param_num_normal_players" in params:
            public_state.__param_num_normal_players__ = params["param_num_normal_players"]
        else:
            public_state.__param_num_normal_players__ = 5

        if public_state.param_num_normal_players not in [2,4,5]:
            logger.fatal("The number of normal players must be in [2,4,5]")
            raise ValueError("The number of normal players must be in [2,4,5]")

        public_state.__public_person_infos__ = [PublicPersonInfo() for i in range(public_state.__param_num_normal_players__)]
        for i in range(public_state.__param_num_normal_players__):
            public_state.__public_person_infos__[i].__num_hand_cards__ = 0
            public_state.__public_person_infos__[i].__charactor_card__ = None
            public_state.__public_person_infos__[i].__equipment_cards__ = []

        person_states = [BangStatePerson() for i in range(public_state.param_num_normal_players+1)]

        self.__public_state_history__.append(public_state)
        self.__private_state_history__.append(private_state)
        for i in range(public_state.param_num_normal_players):
            self.__person_states_history__[i].append(person_states[i])
            self.__person_states_history__[i][0].__id__         = i
            self.__person_states_history__[i][0].__hand_cards__ = []
            self.__person_states_history__[i][0].__role__       = ""
        self.__person_states_history__[public_state.__param_num_normal_players__][0].__available_actions__ = self.available_actions()
        

        self.__gen_infos__()


    def forward(self):
        pass


    def available_actions(self):
        '''
        Generate all valid actions given the public state and the person state

        :return: all valid actions
        '''
        logger = roomai.get_logger()
        ## charactorcard
        if self.__public_state_history__[-1].__public_person_infos__[-1].__charactor_card__ is None:
            available_actions = dict()
            tmp_set = set()
            for i in range(len(self.__public_state_history__[-1].__public_person_infos__)):
                if self.__public_state_history__[-1].__public_person_infos__[i].__charactor_card__ is not None:
                    tmp_set.add(self.__public_state_history__[-1].__public_person_infos__[i].__charactor_card__.key)

            for key in CharactorCardsDict:
                if key not in tmp_set:
                    available_actions[key] = BangActionChance.lookup(key)
            return available_actions

        ## rolecard
        if self.__public_state_history__[-1].__public_person_infos__[-1].__role_card__ is None:
            available_actions = dict()
            tmp_set = set()
            if self.__public_state_history__[-1].__param_num_normal_players__ == 2:
                return available_actions

            elif self.__public_state_history__[-1].__param_num_normal_players__ == 4:
                return available_actions

            elif self.__public_state_history__[-1].__param_num_normal_players__ == 5:
                return available_actions

            else:
                logger.fatal("param_num_normal_players not in [2,4,5]")
                raise ValueError("param_num_normal_players not in [2,4,5]")
            

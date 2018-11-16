#!/bin/python
import roomai
import random

from roomai.games.bang import BangStatePublic

class BangEnv():

    def init(self, params = dict()):
        '''
        Initialize the TexasHoldem game environment with the initialization params.\n
        The initialization is a dict with some options\n
        
        1. param_num_normal_players: how many players are in the game, the option must be in {2, 4, 5}, default 5\n
        2. param_start_turn: The param_start_turn is the id of a normal player, who is the first to take an action \n

        
        An example of the initialization param is {"param_num_normal_players":2}

        :param params: the initialization params
        :return: infos, public_state, person_states, private_state
        '''

        logger = roomai.get_logger()
        public_state = BangStatePublic()
        self.__public_state_history__.append(public_state)

        if "param_num_normal_players" in params:
            public_state.__param_num_normal_players__ = params["param_num_normal_players"]
        else:
            public_state.__param_num_normal_players__ = 3

        if "param_start_turn" in params:
            public_state.__param_start_turn__ = params["param_start_turn"]
        else:
            public_state.__param_start_turn__ = int(random.random() * public_state.param_num_normal_players)




    def forward(self):

    def available_actions(self):
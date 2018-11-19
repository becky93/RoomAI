#!/bin/python
import random
import math
import copy
import roomai.kuhnpoker.KuhnPokerActionChance
import roomai.kuhnpoker.KuhnPokerAction
import roomai.games.common
logger = roomai.get_logger()



class KuhnPokerEnv(roomai.games.common.AbstractEnv):
    '''
    The KuhnPoker game environment
    '''

    #@override
    def init(self, params=dict()):
        '''
        Initialize the KuhnPoker game environment.The params is the initialization params with the following params:\n
        1. param_start_turn: The param_start_turn is the id of a normal player, who is the first to take an action. In KuhnPoker, param_start_turn must be 0 or 1.
        
        :param params: the initialization params, for example, params={"param_start_turn":1}
        :return: infos, public_state, person_states, private_state 
        '''


        private_state = roomai.kuhnpoker.KuhnPokerPrivateState()
        public_state  = roomai.kuhnpoker.KuhnPokerPublicState()
        person_states = [roomai.kuhnpoker.KuhnPokerPersonState() for i in range(3)]

        if "param_start_turn" in params:
            public_state.__param_start_turn__ = params["start_turn"]
        else:
            public_state.__param_start_turn__ = int(random.random() * 2)
        if public_state.__param_start_turn__ not in [0,1]:
            raise ValueError("The param_start_turn (%d) must be in [0,1]"%(self.public_state.__param_start_turn__))

        if "param_num_normal_players" in params:
            logger.warning(
                "KuhnPoker is a game of two players and the number of players always be 2. Ingores the \"num_normal_players\" option")
        public_state.__param_num_normal_players__= 2

        self.__public_state_history__.append(public_state)
        self.__private_state_history__.append(private_state)
        for i in range(public_state.param_num_normal_players + 1):
            self.__person_states_history__[i].append(person_states[i])
            self.__person_states_history__[i][0].__id__ = i
            self.__person_states_history__[i][0].__hand_cards__ = []


        public_state.__turn__             = 2
        public_state.__first__            = self.public_state.__param_start_turn__
        public_state.__epoch__            = 0
        public_state.__action_history__   = []
        public_state.__is_terminal__      = False
        public_state.__scores__           = None
        person_states[0].__id__           = 0
        person_states[0].__number__       = -1
        person_states[1].__id__           = 1
        person_states[1].__number__       = -1
        person_states[2].__id__           = 2
        person_states[2].__number__       = -1

        self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnChanceActions

        self.__gen_state_history_list__()
        infos = self.__gen_infos__()

        
        return  infos, self.__public_state_history__, self.__person_states_history__, self.__private_state_history__

    #@override
    def forward(self, action):
        """
        The KuhnPoker game environment steps with the action taken by the current player

        :param action
        :returns:infos, public_state, person_states, private_state
        """

        private_state = copy.deepcopy(self.__private_state_history__[-1])
        public_state  = copy.deepcopy(self.__public_state_history__[-1])
        person_states = [copy.deepcopy(self.__person_states_history__[i][-1]) for i in range(3)]

        self.__public_state_history__.append(public_state)
        self.__private_state_history__.append(private_state)
        for i in range(public_state.param_num_normal_players + 1):
            self.__person_states_history__[i].append(person_states[i])
            self.__person_states_history__[i][0].__id__ = i
            self.__person_states_history__[i][0].__hand_cards__ = []

        self.__playerid_action_history__.append(public_state.turn, action)

        ####### forward with the chance action ##########
        if isinstance(action, roomai.kuhnpoker.KuhnPokerActionChance) == True:
            person_states[0][-1].__number__ = action.number_for_player0
            person_states[1][-1].__number__ = action.number_for_player1
            person_states[public_state.turn].__available_actions__ = dict()
            public_state.__turn__ = public_state.__param_start_turn__
            person_states[public_state.turn].__available_actions__ = self.available_actions()

            self.__gen_state_history_list__()
            return self.__gen_infos__(), self.__public_state_history__, self.__person_states_history__, self.__private_state_history__, self.__playerid_action_history__


        self.person_states[self.public_state.turn].__available_actions__ = dict()
        self.public_state.__action_history__.append((self.public_state.turn,action))
        #self.public_state.__epoch__                                     += 1
        self.public_state.__turn__                                       = (self.public_state.turn+1)%2


        if len(self.public_state.action_history) == 1: #1 chance
            pass
        elif len(self.public_state.action_history) == 1+1: #1 normal + 1 chance
            self.public_state.__is_terminal__ = False
            self.public_state.__scores__      = []
            self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnActions

            self.__gen_state_history_list__()
            infos = self.__gen_infos__()
            return infos, self.public_state, self.person_states, self.private_state

        elif len(self.public_state.action_history) == 2+1: # 2 normal + 1 chance
            scores = self.__evalute_two_round__()
            if scores is not None:
                self.public_state.__is_terminal__ = True
                self.public_state.__scores__      = scores

                self.__gen_state_history_list__()
                infos = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state
            else:
                self.public_state.__is_terminal__ = False
                self.public_state.__scores__      = []
                self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnActions

                self.__gen_state_history_list__()
                infos   = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state

        elif len(self.public_state.action_history) == 3 + 1: # 3 normal action + 1 chance
            self.public_state.__is_terminal__ = True
            self.public_state.__scores__     = self.__evalute_three_round__()

            self.__gen_state_history_list__()
            infos = self.__gen_infos__()
            return infos,self.public_state, self.person_states, self.private_state

        else:
            raise Exception("KuhnPoker has 4 items in action_history (3 normal actions + 1 chance action)")


    #@Overide
    @classmethod
    def compete(cls, env, players):
        '''
        Use the game environment to hold a compete_silent for the players

        :param env: The game environment
        :param players: The players
        :return: scores for the players
        '''

        if len(players) != 3:
            raise  ValueError("The len(players) in Kuhn is 3 (2 normal players and 1 chance player).")


        infos, public_state, person_state, private_state = env.init()
        for i in range(len(players)):
            players[i].receive_info(infos[i])

        while public_state.is_terminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()
            infos,public_state, person_state, private_state = env.forward(action)
            for i in range(len(players)):
                players[i].receive_info(infos[i])

        return public_state.scores

    @classmethod
    def available_actions(self, public_state, person_state):
        '''
        :param public_state: the public state of this game 
        :param person_state: the person state corresponding to the current player
        :return: 
        '''

        return roomai.kuhnpoker.AllKuhnActions

    def __higher_number_player__(self):
        if self.person_states[0].number > self.person_states[1].number:
            return 0
        else:
            return 1

    def __evalute_two_round__(self):
        win    = self.__higher_number_player__()
        first  = self.public_state.first
        scores = [0, 0];
        actions = [id_action[1] for id_action in self.public_state.action_history]

        if actions[0] == "check" and \
           actions[1] == "bet":
            return None
        
        if actions[0] == actions[1] and \
           actions[0] == "check":
            scores[win]   = 1;
            scores[1-win] = -1
            return scores;

        if actions[0] == "bet" and \
           actions[1] == "check":
            scores[first]   = 1;
            scores[1-first] = -1
            return scores;

        if actions[0] == actions[1] and \
           actions[0] == "bet":
            scores[win]   = 2
            scores[1-win] = -2
            return scores;


    def __evalute_three_round__(self):
        first   = self.public_state.first 
        win     = self.__higher_number_player__()
        scores  = [0, 0]

        if self.public_state.action_history[2][1].key == "check":
            scores[1 - first] = 1;
            scores[first]     = -1
        else:
            scores[win]   = 2;
            scores[1-win] = -2
        return scores;
       
    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = KuhnPokerEnv()
        newinstance = super(KuhnPokerEnv, self).__deepcopy__(newinstance=newinstance)
        return newinstance
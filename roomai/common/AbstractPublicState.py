#!/bin/python
#coding=utf8

import roomai
import roomai.common
logger = roomai.get_logger()



######################################################################### Basic Concepts #####################################################
class AbstractPublicState(object):
    '''
    The abstract class of the public state. The information in the public state is public to every player.\n
    The attributes with param prefix is the parameters set by the init function of enviroment.
    '''
    def __init__(self):
# # <<<<<<< HEAD
#         self.__turn__            = None
#         self.__action_history__  = []
#         self.__action_list__ = []
#         self.__is_terminal__     = False
#         self.__scores__          = None
# =======
        self.__turn__               = None

        ## parameters
        self.__param_start_turn__            = 0
        self.__param_num_normal_players__    = 2
        self.__param_backward_enable__       = True

        self.__action_history__     = []

        self.__is_terminal__        = False
        self.__scores__             = None

    def __get_param_start_turn__(self):   return self.__param_start_turn__
    param_start_turn = property(__get_param_start_turn__, doc="The param_start_turn is the id of a normal player, who is the first to take an action.For example, param_start_turn = 0")

    def __get_param_num_normal_players__(self):   return self.__param_num_normal_players__
    param_num_normal_players = property(__get_param_num_normal_players__,
                                  doc="The number of normal players (different from the chance player).The default is 2.\n"
                                      "In some games, the number of normal players is constant, for exmple, doudizhu.\n"
                                      "In the other games, the number of normal players is variable, for example, texas hold em.\n")

    def __get_param_backward_enable__(self):  return self.__param_backward_enable__
    param_backward_enable = property(__get_param_backward_enable__, doc="If you need call the backward function of the enviroment, please set it to True. Default False.")
# >>>>>>> upstream/master

    def __get_turn__(self): return self.__turn__
    turn = property(__get_turn__, doc = "The players[turn] is expected to take an action.")

    def __get_action_list__(self): return self.__action_list__
    action_list = property(__get_action_list__, doc="actions player have taken")

    def __get_action_history__(self):   return tuple(self.__action_history__)
    action_history = property(__get_action_history__, doc = "The action_history so far. For example, action_history = [(0, roomai.kuhnpoker.KuhnAction.lookup(\"check\"),(1,roomai.kuhnpoker.KuhnAction.lookup(\"bet\")].\n"
                                                            "The format of the item in action_history is (person_id, action)")

    def __get_is_terminal__(self):   return  self.__is_terminal__
    is_terminal = property(__get_is_terminal__,doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,2,-1].\n"
                                                     "is_terminal = False, the scores is None.")

    def __get_scores__(self):
        if self.__scores__ is None:
            return None
        return tuple(self.__scores__)
    scores = property(__get_scores__, doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,3,-2].\n"
                                            "is_terminal = False, the scores is None.")


    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractPublicState()

        newinstance.__turn__           = self.__turn__
        newinstance.__action_history__ = list(self.__action_history__)
        newinstance.__is_terminal__    = self.is_terminal
        if self.scores is None:
            newinstance.__scores__ = None
        else:
            newinstance.__scores__ = [score for score in self.scores]
        return newinstance
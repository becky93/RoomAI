#!/bin/python
import unittest
import random
from roomai.common import *
from roomai.doudizhupoker import DouDiZhuPokerEnv
from roomai_models.crf.algorithms import CRFPlayer
from roomai_models.crf.algorithms import CRFOutSampling

class CRFPlayerExample(CRFPlayer):
    def reset(self):
        pass
    def receive_info(self, info):
        self.actions = list(info.person_state.available_actions.values())
    def take_action(self):
        len  = len(self.actions)
        rand = self.actions[int(random.random() * len)]
        return self.actions[rand]
    def update_averge_strategies(self, info, actions, targets):
        print("update_averge_strategies")
    def get_averge_strategies(self, info, actions):
        return [1.0 / len(actions) for i in range(len(actions))]
    def update_counterfactual_regrets(self, info, actions, targets):
        print("update_counterfactual_regrets")
    def get_counterfactual_regrets(self, info, actions):
        return [1.0/ len(actions) for i in range(len(actions))]

class CRFPlayerTester(unittest.TestCase):
    def testCRFOutSampling(self):
        env = DouDiZhuPokerEnv()
        player = CRFPlayerExample()
        crf = CRFOutSampling()
        crf.dfs(current_player_idx=0,env = env, player=player,reach_probs=[1.0,1.0,1.0],action = None,deep = 0)


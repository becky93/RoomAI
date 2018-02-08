import unittest
from models.dqn.dqnalgorithm import DqnAlgorithm
import random
import roomai
import roomai.sevenking
from models.dqn.dqnalgorithm import DqnPlayer
from models.dqn.sevenking import SevenKingModel_ThreePlayers

class ExamplePlayer(DqnPlayer):
    def terminal_info_feat(self):
        return [1]

    def terminal_action_feat(self):
        return [0]

    def gen_info_feat(self, info):
        return [1]

    def gen_action_feat(self, info, action):
        return [0]

    def update_model(self, experiences):
        print ("update_model")

    def reset(self):
        pass
    def receive_info(self, info):
        self.info = info
    def take_action(self):
        info = self.info
        action_list = list(info.person_state.available_actions.values())
        idx         = int(random.random() * len(action_list))
        return action_list[idx]

import roomai.common


class DQNTester(unittest.TestCase):
    def setUp(self):
        import logging
        roomai.set_loglevel(logging.DEBUG)
    def test_dqn(self):
        import roomai.sevenking
        env   = roomai.sevenking.SevenKingEnv()
        player = ExamplePlayer()
        dqn   = DqnAlgorithm()
        opponents = [roomai.common.RandomPlayer() for i in range(2)]
        dqn.train(env=env, players = [player] + opponents + [roomai.common.RandomPlayerChance()], params={})
        dqn.eval(env=env, players = [player] + opponents + [roomai.common.RandomPlayerChance()], params={})

    def test_sevenking_dqn(self):
        import logging
        roomai.set_loglevel(logging.DEBUG)
        env = roomai.sevenking.SevenKingEnv()
        player = SevenKingModel_ThreePlayers()
        algo = DqnAlgorithm()
        opponents = [roomai.common.RandomPlayer() for i in range(2)]
        algo.train(env=env, players = [player] + opponents + [roomai.common.RandomPlayerChance()], params={"num_normal_players": 3, "num_iters":5})
        opponents = [roomai.common.RandomPlayer() for i in range(2)]
        scores = algo.eval(players = [player] + opponents + [roomai.common.RandomPlayerChance()], env=env)
        print(scores)


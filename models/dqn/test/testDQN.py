import unittest
from dqn import DqnAlgorithm
from dqn import DqnModel
import random
import roomai
import roomai.sevenking
import dqn
from sevenking import SevenKingModel_ThreePlayers

class ExampleModel(DqnModel):
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

    def take_action(self, info):
        action_list = list(info.person_state.available_actions.values())
        idx         = int(random.random() * len(action_list))
        return action_list[idx]




class DQNTester(unittest.TestCase):
    def test_dqn(self):
        import roomai.sevenking
        env   = roomai.sevenking.SevenKingEnv()
        model = ExampleModel()
        dqn   = DqnAlgorithm()
        opponents = [roomai.common.RandomPlayer() for i in range(2)]
        dqn.train(model=model,env=env,params={})
        dqn.eval(model = model, env=env, opponents = opponents, params={})

    def test_sevenking_dqn(self):
        env = roomai.sevenking.SevenKingEnv()
        model = SevenKingModel_ThreePlayers()
        algo = dqn.DqnAlgorithm()
        algo.train(env=env, model=model, params={"num_normal_players": 3})

        opponents = [roomai.common.RandomPlayer() for i in range(2)]
        scores = algo.eval(model=model, env=env, opponents=opponents)
        print(scores)

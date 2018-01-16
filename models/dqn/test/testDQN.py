import unittest
from dqn import DQN


class ExampleModel(dqn.DQNModel):
    def terminal_info_feat(self):
        return [1]

    def terminal_action_feat(self):
        return [0]

    def gen_info_feat(self, info):
        return [1]

    def gen_action_feat(self, action):
        return [0]

    def update_model(self, experiences):
        print ("update_model")

    def take_action(self, info):
        return list(info.person_state.available_actions.values())[0]




class DQNTester(unittest.TestCase):
    def test_dqn(self):
        import roomai.sevenking
        env   = roomai.sevenking.SevenKingEnv()
        model = ExampleModel()
        dqn   = DQN()
        dqn.train(model=model,env=env,params={})
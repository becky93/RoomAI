import unittest
import algorithm


class ExampleModel(algorithm.DQNModel):
    def terminal_state_feat(self):
        return [1]

    def terminal_action_feat(self):
        return [0]

    def gen_state_feat(self, info):
        return [1]

    def gen_action_feat(self, action):
        return [0]

    def update_model(self, experiences):
        print ("update_model")

    def predict_q(self,state_feat, action_feat):
        return 0



class DQNTester(unittest.TestCase):
    def test_dqn(self):
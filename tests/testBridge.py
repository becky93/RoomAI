#!/bin/python
import unittest
import roomai.bridge

class BridgeTester(unittest.TestCase):
    def testInit(self):
        env = roomai.bridge.BridgeEnv()
        env.init()

    def testForward(self):
        env = roomai.bridge.BridgeEnv()
        infos, public_state, person_states, private_state = env.init()
        xxx = 0
        self.assertEqual(len(infos),4)
        for i in range(4):
            self.assertEqual(len(person_states[i].hand_cards_dict.keys()), 52 / 4)
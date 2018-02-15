#!bin/python
import roomai.common
import roomai.kuhn
import unittest

class EnvCopyTester(unittest.TestCase):

    def testEnvCopy(self):
        env =roomai.kuhn.KuhnPokerEnv()
        env.__deepcopy__()
        env.init()
        env.__deepcopy__()
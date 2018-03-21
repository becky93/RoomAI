#!bin/python
import roomai.common
import roomai.kuhn
import unittest

class EnvCopyTester(unittest.TestCase):

    def testEnvCopy(self):
        env =roomai.kuhn.KuhnPokerEnv()
        newenv = env.__deepcopy__()
        newenv.init()
        newnewenv = newenv.__deepcopy__()
        newnewenv.forward(roomai.kuhn.KuhnPokerAction.lookup("bet"))
        print ("fuck")


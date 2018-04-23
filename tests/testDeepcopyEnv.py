#!bin/python
import roomai.common
import roomai.kuhnpoker
import unittest

class EnvCopyTester(unittest.TestCase):

    def testEnvCopy(self):
        env =roomai.kuhnpoker.KuhnPokerEnv()
        newenv = env.__deepcopy__()
        newenv.init()
        newnewenv = newenv.__deepcopy__()
        newnewenv.forward(roomai.kuhnpoker.KuhnPokerAction.lookup("bet"))
        print ("fuck")


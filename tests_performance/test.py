#!/bin/python
import roomai.common
import models.dqn.dqnalgorithm
import roomai.sevenking
import logging
#roomai.set_loglevel(logging.DEBUG)

env     = roomai.sevenking.SevenKingEnv()
players = [roomai.common.RandomPlayer() for i in range(3)] + [roomai.common.RandomPlayerChance()]
dqn     = models.dqn.dqnalgorithm.DqnAlgorithm()
dqn.eval(env = env, players = players)
dqn.eval(env = env, players = players)
dqn.eval(env = env, players = players)
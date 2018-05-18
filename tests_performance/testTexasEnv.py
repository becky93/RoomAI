#!/bin/python

import roomai.common
import roomai.texasholdem
import roomai

if __name__ == "__main__":
    import time
    start = time.time()

    random_players = [roomai.common.RandomPlayer() for i in range(3)]
    env = roomai.texasholdem.TexasHoldemEnv()
    for i in range(5):
        env.compete(env, random_players)
    end = time.time()
    print (end-start)

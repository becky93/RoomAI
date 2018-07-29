#!/bin/python
from roomai.kuhnpoker import *;
import random
import roomai
import roomai.common

class KuhnPokerExamplePlayer(roomai.common.AbstractPlayer):
    def receive_info(self, info):
        if info.person_state.available_actions is not None:
            self.available_actions = info.person_state.available_actions

    def take_action(self):
        values = self.available_actions.values()
        return list(values)[int(random.random() * len(values))]

    def reset(self):
        pass

if __name__ == "__main__":
    players = [KuhnPokerExamplePlayer() for i in range(2)] + [roomai.common.RandomPlayerChance()]
    # RandomChancePlayer is the chance player with the uniform distribution over every output
    env = KuhnPokerEnv()
    scores = KuhnPokerEnv.compete(env, players)
    print(scores)
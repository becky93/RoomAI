import random
import pdb

# import algorithms 

import sys
sys.path.append("E:/roomAI/RoomAI")

from models.crm.algorithms import CRMPlayer
from roomai.sevenking import SevenKingInfo
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingUtils
from roomai.sevenking import SevenKingAction


class SevenKingPlayer(CRMPlayer):

    def __init__(self):

        self.state = []
        self.regrets = dict()
        self.strategies = dict()

    def gen_state(self, info):
        hand_cards = info.person_state.hand_cards
        history = info.public_state.action_list
        hand_cards_keys = []
        for i in range(len(hand_cards)):
            hand_cards_keys.append(hand_cards[i].key)
        return "%s_%s" % ("_".join(hand_cards_keys), "".join(history))

    def update_strategies(self, state, actions, targets):
        for i in xrange(len(actions)):
            state_action = "%s_%s" % (state, actions[i].key)
            self.strategies[state_action] = targets[i]

    def get_strategies(self, state, actions):
        probs = [1.0 for i in range(len(actions))]
        for i in range(len(actions)):
            state_action = "%s_%s" % (state, actions[i].key)
            if state_action not in self.strategies:
                probs[i] = 0.0
            else:
                probs[i] = self.strategies[state_action]
        return probs

    def update_regrets(self, state, actions, targets):
        for i in range(len(actions)):
            state_action = "%s_%s"%(state, actions[i].key)
            self.regrets[state_action] = targets[i]

    def get_regrets(self, state, actions):
        regrets = [0 for i in range(len(actions))]

        for key in actions:
            state_action = "%s_%s" % (state, key)
            if state_action not in self.regrets:
                regrets[i] = 0
            else:
                regrets[i] = self.regrets[state_action]
        return regrets


def CRMTrain(env, player, probs, action = None, depth = 0):

    infos         = None
    public_state  = None
    person_states = None
    private_state = None

    utility = 0

    num_players = len(probs)

    # initialization
    if depth == 0:
        infos, public_state, person_states, private_state = env.init({"record_history":True, "num_players":num_players})
    else:
        infos, public_state, person_states, private_state = env.forward(action)

    if public_state.is_terminal == True:
        utility = public_state.scores[public_state.turn]

    else:
        state = player.gen_state(infos[public_state.turn])
        available_actions = env.available_actions(public_state, person_states[public_state.turn])
        num_available_actions = len(available_actions)

        regrets = player.get_regrets(state, available_actions)

        # regret matching
        cur_strategies = [0 for i in range(num_available_actions)]
        normalizing_sum = 0
        for i in xrange(num_available_actions):
            normalizing_sum += max(regrets[i], 0)
        for i in xrange(num_available_actions):
            if normalizing_sum > 0:
                cur_strategies[i] = max(regrets[i], 0) / normalizing_sum
            else:
                cur_strategies[i] = 1.0 / num_available_actions

        util = [0 for i in range(num_available_actions)]
        strategy_util = 0

        sorted_actions = sorted(available_actions.items(), key=lambda e:e[0])
        for i in xrange(num_available_actions):
            temp_probs = [0 for i_temp in range(num_players)]
            temp_probs[public_state.turn] = probs[public_state.turn]
            for j in xrange(num_players):
                if j != public_state.turn:
                    temp_probs[j] = probs[j] * cur_strategies[i]
            util[i] = -CRMTrain(env, player, temp_probs, available_actions[sorted_actions[i][0]], depth+1)
            strategy_util += cur_strategies[i] * util[i]

        new_regrets = [0 for i in range(num_available_actions)]
        new_strategies = [0 for i in range(num_available_actions)]

        strategies = player.get_strategies(state, available_actions)

        # update regrets and strategies
        for i in xrange(num_available_actions):
            prob = 1
            for j in xrange(num_players):
                if j != public_state.turn:
                    prob *= probs[j]
            new_regrets[i] = regrets[i] + prob * (util[i] - strategy_util)
            new_strategies[i] = strategies[i] + probs[public_state.turn] * cur_strategies[i]

        player.update_regrets(state, available_actions, new_regrets)
        player.update_strategies(state, available_actions, new_strategies)
        utility = strategy_util

    if depth != 0:
        env.backward()

    return utility


def Train(params = dict()):
    # initialization
    env = SevenKingEnv()
    player = SevenKingPlayer()

    num_players = 0

    if "num_players" in params:
        num_players = params["num_players"]
    else:
        num_players = 2

    if "num_iter" in params:
        num_iter = params["num_iter"]
    else:
        num_iter = 1000

    probs = [1.0 for i in range(num_players)]

    for i in xrange(num_iter):
        CRMTrain(env, player, probs)

    return player


if __name__ == '__main__':
    params = dict()
    params["num_players"] = 2
    params["num_iter"] = 1000

    player = Train(params)
    print player.regrets
    print player.strategies

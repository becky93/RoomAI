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
        self.exploration = 0.3

    def gen_state(self, info):
        hand_cards = info.person_state.hand_cards
        history = info.public_state.action_list
        hand_cards_keys = []
        for i in range(len(hand_cards)):
            hand_cards_keys.append(hand_cards[i].key)

        # while '' in history:
        #     history.remove('')

        return "%s_%s" % ("_".join(hand_cards_keys), "".join(history))

    def update_strategies(self, state, actions, targets):
        for key in actions:
            state_action = "%s_%s" % (state, key)
            self.strategies[state_action] = targets[state_action]

    def get_strategies(self, state, actions):
        strategy = dict()
        for key in actions:
            state_action = "%s_%s" % (state, key)
            if state_action not in self.strategies:
                strategy[state_action] = 0.0
            else:
                strategy[state_action] = self.strategies[state_action]
        return strategy

    def update_regrets(self, state, actions, targets):
        for key in actions:
            state_action = "%s_%s"%(state, key)
            self.regrets[state_action] = targets[state_action]

    def get_regrets(self, state, actions):
        regrets = dict()

        for key in actions:
            state_action = "%s_%s" % (state, key)
            if state_action not in self.regrets:
                regrets[state_action] = 0
            else:
                regrets[state_action] = self.regrets[state_action]
        return regrets

    def random_action(self, actions):

        idx = int(random.random() * len(actions))
        return list(actions.keys())[idx], 1.0 / len(actions)


    def sample_action(self, state, actions, cur_strategies):

        val = random.random()
        total = 0
        for key in actions:
            new_key = state + '_' + key
            total += cur_strategies[new_key]
            if total > 0 and val < total:
                return key, cur_strategies[new_key]

    def receive_info(self, info):
        self.states = self.gen_state(info)
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        cur_strategies = self.get_strategies(self.states, self.available_actions)

        print self.states
        print cur_strategies

        new_state = ''

        val = random.random()
        total = 0
        for key in cur_strategies:
            total += cur_strategies[key]
            if total > 0 and val < total:
                new_state = key

        if new_state != '' and new_state[-1] != '_':
            action = new_state.split("_")[-1]
            return SevenKingAction.lookup(action)
        else:
            idx = int(random.random() * len(self.available_actions))
            return list(self.available_actions.values())[idx]

    def reset(self):
        pass


def CRMTrain(env, cur_turn, player, probs, action=None, depth=0):

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
        utility = public_state.scores[cur_turn]

    else:
        this_turn = public_state.turn
        state = player.gen_state(infos[this_turn])
        # available_actions = env.available_actions(public_state, person_states[this_turn])
        available_actions = person_states[this_turn].available_actions

        regrets = player.get_regrets(state, available_actions)

        # regret matching
        cur_strategies = dict()
        normalizing_sum = 0
        for key in regrets:
            normalizing_sum += max(regrets[key], 0)
        for key in regrets:
            if normalizing_sum > 0:
                cur_strategies[key] = max(regrets[key], 0) / normalizing_sum
            else:
                cur_strategies[key] = 1.0 / len(available_actions)

        util = dict()
        strategy_util = 0

        for key in available_actions:
            temp_probs = [0 for i_temp in range(num_players)]
            temp_probs[this_turn] = probs[this_turn]
            new_key = "%s_%s" % (state, key)
            for j in xrange(num_players):
                if j != this_turn:
                    temp_probs[j] = probs[j] * cur_strategies[new_key]
            util[new_key] = -CRMTrain(env, this_turn, player, temp_probs, available_actions[key], depth+1)
            strategy_util += cur_strategies[new_key] * util[new_key]

        new_regrets = dict()
        new_strategies = dict()


        strategies = player.get_strategies(state, available_actions)
        # update regrets and strategies
        for key in available_actions:
            prob = 1
            new_key = "%s_%s" % (state, key)
            for j in xrange(num_players):
                if j != this_turn:
                    prob *= probs[j]
            new_regrets[new_key] = regrets[new_key] + prob * (util[new_key] - strategy_util)
            new_strategies[new_key] = strategies[new_key] + probs[this_turn] * cur_strategies[new_key]

        player.update_regrets(state, available_actions, new_regrets)
        player.update_strategies(state, available_actions, new_strategies)

        utility = strategy_util

    if depth != 0:
        env.backward()

    return utility

def OutcomeSamplingCRM(env, cur_turn, player, num_players, sampleProb, action=None, depth=0):
    infos = None
    public_state = None
    person_states = None
    private_state = None

    utility = 0

    # num_players = len(probs)

    # initialization
    if depth == 0:
        infos, public_state, person_states, private_state = env.init({"record_history": True, "num_players": num_players})
    else:
        infos, public_state, person_states, private_state = env.forward(action)

    if public_state.is_terminal == True:
        utility = public_state.scores[cur_turn]

    else:
        this_turn = public_state.turn
        state = player.gen_state(infos[this_turn])

        available_actions = person_states[this_turn].available_actions

        regrets = player.get_regrets(state, available_actions)

        # regret matching
        cur_strategies = dict()
        normalizing_sum = 0
        for key in regrets:
            normalizing_sum += max(regrets[key], 0)
        for key in regrets:
            if normalizing_sum > 0:
                cur_strategies[key] = max(regrets[key], 0) / normalizing_sum
            else:
                cur_strategies[key] = 1.0 / len(available_actions)

        # sampling
        if random.random() < player.exploration:
            action_key, action_prob = player.random_action(available_actions)
        else:
            action_key, action_prob = player.sample_action(state, available_actions, cur_strategies)

        new_key = "%s_%s" % (state, action_key)

        this_prob = player.exploration * (1.0 / len(available_actions)) + (1.0 - player.exploration) * action_prob
        util, isTerminal = OutcomeSamplingCRM(env, this_turn, player, num_players, sampleProb*this_prob, available_actions[action_key], depth+1)

        strategy_util = action_prob * util / sampleProb

        strategies = player.get_strategies(state, available_actions)
        # update regrets and strategies
        if isTerminal:
            player.regrets[new_key] = strategy_util * (1 - cur_strategies[new_key])
        else:
            player.regrets[new_key] = -strategy_util * cur_strategies[new_key]

        player.strategies[new_key] = strategies[new_key] + sampleProb * this_prob * cur_strategies[new_key]

        utility = util

    if depth != 0:
        env.backward()

    return utility, public_state.is_terminal


def Train(params = dict()):
    # initialization
    env = SevenKingEnv()
    player = SevenKingPlayer()

    num_players = 0

    if "num_players" in params:
        num_players = params["num_players"]
    else:
        num_players = 5

    if "num_iter" in params:
        num_iter = params["num_iter"]
    else:
        num_iter = 10000

    probs = [1.0 for i in range(num_players)]

    for i in xrange(num_iter):
        for p in xrange(num_players):
            # CRMTrain(env, p, player, probs)
            OutcomeSamplingCRM(env, p, player, num_players, 1)

    return player


if __name__ == '__main__':
    params = dict()
    params["num_players"] = 2
    params["num_iter"] = 1000

    player = Train(params)
    print player.regrets
    print player.strategies

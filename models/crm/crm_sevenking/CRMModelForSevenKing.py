import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import random
import pdb
import math
import sys

sys.path.append("E:/roomAI/RoomAI")

import crash_on_ipy
from models.crm.algorithms.crm import CRMPlayer
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingUtils
from roomai.sevenking import SevenKingAction

'''
class LSTMRNN(object):
    def __init__(self, n_steps, input_size, output_size, cell_size, batch_size):
        self.n_steps = n_steps
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size
        self.batch_size = batch_size
        with tf.name_scope('inputs'):
            self.xs = tf.placeholder(tf.float32, [None, n_steps, input_size], name='xs')
            self.ys = tf.placeholder(tf.float32, [None, n_steps, output_size], name='ys')
        with tf.variable_scope('in_hidden'):
            self.add_input_layer()
        with tf.variable_scope('LSTM_cell'):
            self.add_cell()
        with tf.variable_scope('out_hidden'):
            self.add_output_layer()
        with tf.name_scope('cost'):
            self.compute_cost()
        with tf.name_scope('train'):
            self.train_op = tf.train.AdamOptimizer(LR).minimize(self.cost)

    def add_input_layer(self, ):
        l_in_x = tf.reshape(self.xs, [-1, self.input_size], name='2_2D')  # (batch*n_step, in_size)
        # Ws (in_size, cell_size)
        Ws_in = self._weight_variable([self.input_size, self.cell_size])
        # bs (cell_size, )
        bs_in = self._bias_variable([self.cell_size, ])
        # l_in_y = (batch * n_steps, cell_size)
        with tf.name_scope('Wx_plus_b'):
            l_in_y = tf.matmul(l_in_x, Ws_in) + bs_in
        # reshape l_in_y ==> (batch, n_steps, cell_size)
        self.l_in_y = tf.reshape(l_in_y, [-1, self.n_steps, self.cell_size], name='2_3D')

    def add_cell(self):
        lstm_cell = tf.contrib.rnn.BasicLSTMCell(self.cell_size, forget_bias=1.0, state_is_tuple=True)
        with tf.name_scope('initial_state'):
            self.cell_init_state = lstm_cell.zero_state(self.batch_size, dtype=tf.float32)
        self.cell_outputs, self.cell_final_state = tf.nn.dynamic_rnn(
            lstm_cell, self.l_in_y, initial_state=self.cell_init_state, time_major=False)

    def add_output_layer(self):
        # shape = (batch * steps, cell_size)
        l_out_x = tf.reshape(self.cell_outputs, [-1, self.cell_size], name='2_2D')
        Ws_out = self._weight_variable([self.cell_size, self.output_size])
        bs_out = self._bias_variable([self.output_size, ])
        # shape = (batch * steps, output_size)
        with tf.name_scope('Wx_plus_b'):
            self.pred = tf.matmul(l_out_x, Ws_out) + bs_out

    def compute_cost(self):
        logits = [tf.reshape(self.pred, [-1], name='reshape_pred')]
        targets = [tf.reshape(self.ys, [-1], name='reshape_target')]
        weights = [tf.ones([self.batch_size * self.n_steps], dtype=tf.float32)]
        losses = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            logits,
            targets,
            weights,
            average_across_timesteps=True,
            softmax_loss_function=self.ms_error,
            name='losses'
        )
        with tf.name_scope('average_cost'):
            self.cost = tf.div(
                tf.reduce_sum(losses, name='losses_sum'),
                self.batch_size,
                name='average_cost')
            tf.summary.scalar('cost', self.cost)

    def ms_error(self, labels, logits):
        return tf.square(tf.subtract(labels, logits))

    def _weight_variable(self, shape, name='weights'):
        initializer = tf.random_normal_initializer(mean=0., stddev=1., )
        return tf.get_variable(shape=shape, initializer=initializer, name=name)

    def _bias_variable(self, shape, name='biases'):
        initializer = tf.constant_initializer(0.1)
        return tf.get_variable(name=name, shape=shape, initializer=initializer)
'''

class RNNModel():
    def __init__(self, BATCH_START=0, BATCH_SIZE=60, TIME_STEPS=1, INPUT_SIZE=54, OUTPUT_SIZE=1, CELL_SIZE=1, LR=0.0001):
        self.BATCH_START = BATCH_START
        self.BATCH_SIZE = BATCH_SIZE
        self.TIME_STEPS = TIME_STEPS
        self.INPUT_SIZE = INPUT_SIZE
        self.OUTPUT_SIZE = OUTPUT_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.LR = LR

        self.xs = tf.placeholder(tf.float32, [None, self.TIME_STEPS, self.INPUT_SIZE])
        self.ys = tf.placeholder(tf.float32, [None, self.TIME_STEPS, self.OUTPUT_SIZE])

        self.weights = {
            'in': tf.Variable(tf.random_normal([self.INPUT_SIZE, self.CELL_SIZE], 0, 0.01)),
            'out': tf.Variable(tf.random_normal([self.CELL_SIZE, self.OUTPUT_SIZE], 0, 0.01))
        }

        self.biases = {
            'in': tf.Variable(tf.constant(0.1, shape=[self.CELL_SIZE])),
            'out': tf.Variable(tf.constant(0.1, shape=[self.OUTPUT_SIZE]))
        }

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def RNN(self, x, weights, biases):
        x = tf.unstack(x, self.TIME_STEPS, 1)
        lstm_cell = rnn.BasicLSTMCell(self.CELL_SIZE, forget_bias=1.0)
        outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
        return tf.matmul(outputs[-1], weights['out']) + biases['out']

    def model(self):
        self.output = self.RNN(self.xs, self.weights, self.biases)
        self.output_reshape = tf.reshape(self.output, [-1, self.TIME_STEPS, self.OUTPUT_SIZE])
        self.cost = tf.losses.mean_squared_error(labels=self.ys, predictions=self.output_reshape)
        self.train = tf.train.AdamOptimizer(self.LR).minimize(self.cost)
        self.check = tf.add_check_numerics_ops()

    def train(self, seq, res):
        k = 0
        while (k + self.BATCH_SIZE) < len(res):

            batch_x = seq[k:k + self.BATCH_SIZE]
            batch_y = res[k:k + self.BATCH_SIZE]

            batch_x = batch_x.reshape(-1, self.TIME_STEPS, self.INPUT_SIZE)
            batch_y = batch_y.reshape(-1, self.TIME_STEPS, self.OUTPUT_SIZE)
            k = k + self.BATCH_SIZE

            _, _, pred, costs, w_t, b_t = sess.run([self.train, self.check, self.output_reshape, self.cost, self.weights['out'], self.biases['out']],
                                                   feed_dict={self.xs: batch_x, self.ys: batch_y})

            if math.isnan(costs):
                pdb.set_trace()

            if i % 100 == 0:
                print('cost: ', round(costs, 4))

        outputs = self.sess.run(self.output, feed_dict={self.xs: seq.reshape(-1, self.TIME_STEPS, self.INPUT_SIZE),
                                                   self.ys: res.reshape(-1, self.TIME_STEPS, self.OUTPUT_SIZE)})

    def save_model(self, path):
        saver = tf.train.Saver()
        save_path = saver.save(self.sess, path)


class SevenKingPlayer(CRMPlayer):

    def __init__(self):

        self.regrets = dict()
        self.strategies = dict()
        self.exploration = 0.3
        self.action_history = None
        self.available_actions = None

        # about RNN
        self.rnn_model = RNNModel()

    def gen_state(self, info):
        hand_cards = info.person_state.hand_cards
        history = info.public_state.action_list
        hand_cards_keys = []
        for i in range(len(hand_cards)):
            hand_cards_keys.append(hand_cards[i].key)

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
                strategy[state_action] = 1.0 / len(actions)
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

        max_key = None
        max_prob = 0.0

        for key in actions:
            new_key = state + '_' + key
            if cur_strategies[new_key] >= max_prob:
                max_prob = cur_strategies[new_key]
                max_key = key

        return max_key, max_prob

    def receive_info(self, info):
        self.action_history = info.public_state.action_list
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        action_list = []
        regret_list = []

        for action in self.action_history:
            action_list.append(input_trans(action))

        for action in self.available_actions:
            this_action = action_list
            this_action.append(input_trans(action))
            result = self.rnn_model.sess.run(regret_list[action], feed_dict={self.rnn_model.xs: this_action})

        cur_strategies = dict()
        normalizing_sum = 0
        for key in regret_list:
            normalizing_sum += max(regret_list[key], 0)
        for key in regret_list:
            if normalizing_sum > 0:
                cur_strategies[key] = max(regret_list[key], 0) / normalizing_sum
            else:
                cur_strategies[key] = 1.0 / len(self.available_actions)

        val = random.random()
        total = 0

        new_state = ''

        for key in cur_strategies:
            total += cur_strategies[key]
            if total > 0 and val < total:
                new_state = key

        if new_state != '':
            return SevenKingAction.lookup(new_state)
        else:
            idx = int(random.random() * len(self.available_actions))
            return list(self.available_actions.values())[idx]

    def reset(self):
        pass


def input_trans(key_list):
    str_to_rank = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12}
    res = [0] * 54
    kvs = key_list.split(",")

    for kv_i in kvs:
        kv = kv_i.split("_")
        if kv[0] is not "r" and kv[0] is not "R":
            point = str_to_rank[kv[0]]
            suit = SevenKingUtils.suit_str_to_rank[kv[1]]
            res[53 - point*4 - suit] = 1
        elif kv[0] == "r":
            res[1] = 1
        elif kv[0] == "R":
            res[0] = 1

    return res


def OutcomeSamplingCRM(env, cur_turn, player, probs, sampleProb, action_list, regret_list, action=None, depth=0):
    infos = None
    public_state = None
    person_states = None
    private_state = None

    utility = 0

    num_players = len(probs)

    # initialization
    if depth == 0:
        infos, public_state, person_states, private_state = env.init({"record_history": True, "num_players": num_players})
    else:
        infos, public_state, person_states, private_state = env.forward(action)

    terminal_state = False

    if public_state.is_terminal == True:
        utility = public_state.scores[cur_turn]
        terminal_state = True

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

        temp_probs = [0 for i_temp in range(num_players)]
        temp_probs[this_turn] = probs[this_turn] * cur_strategies[new_key]
        for j in range(num_players):
            if j != this_turn:
                temp_probs[j] = probs[j]

        if action_key == "":
            action_list.append([0] * 54)
        else:
            action_list.append(input_trans(action_key))

        regret_list.append(0.0)
        util, isTerminal = OutcomeSamplingCRM(env, this_turn, player, temp_probs, sampleProb*action_prob, action_list, regret_list, available_actions[action_key], depth+1)

        temp_prob = 1.0
        for j in range(num_players):
            if j != this_turn:
                temp_prob *= probs[j]

        # strategy_util = cur_strategies[new_key] * temp_prob * util / sampleProb
        # strategy_util = temp_prob * util
        strategy_util = util / cur_strategies[new_key]
        # strategy_util = available_actions[action_key] * temp_prob * util

        strategies = player.get_strategies(state, available_actions)

        # update regrets and strategies
        if isTerminal:
            player.regrets[new_key] = regrets[new_key] + temp_prob * strategy_util * (1 - cur_strategies[new_key])
        else:
            player.regrets[new_key] = regrets[new_key] - temp_prob * strategy_util * cur_strategies[new_key]

        regret_list[depth] = player.regrets[new_key]

        if player.regrets[new_key] > 1.0 or player.regrets[new_key] < -1.0:
            pdb.set_trace()

        player.strategies[new_key] = strategies[new_key] + probs[this_turn] * cur_strategies[new_key]

        utility = util

    if depth != 0:
        env.backward()

    return utility, terminal_state


def Train(player, env, params = dict()):
    # initialization

    num_players = 0

    if "num_players" in params:
        num_players = params["num_players"]
    else:
        num_players = 2

    probs = [1.0 for i in range(num_players)]
    action_list = []
    regret_list = []

    for p in range(num_players):
        OutcomeSamplingCRM(env, p, player, probs, 1, action_list, regret_list)

    return np.array(action_list), np.array(regret_list)


if __name__ == '__main__':
    # model = LSTMRNN(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE)
    env = SevenKingEnv()
    player = SevenKingPlayer()
    for i in range(200000):

        seq, res = Train(player, env)
        # pdb.set_trace()

        player.rnn_model.train(seq, res)



        '''
            if k == BATCH_SIZE:
                feed_dict = {
                    model.xs: batch_x,
                    model.ys: batch_y,
                }
            else:
                feed_dict = {
                    model.xs: batch_x,
                    model.ys: batch_y,
                    model.cell_init_state: state
                }

            # print(feed_dict)

            _, cost, state, pred = sess.run(
                [model.train_op, model.cost, model.cell_final_state, model.pred],
                feed_dict=feed_dict)

            if math.isnan(cost):
                pdb.set_trace()

            if i % 100 == 0:
                print('cost: ', round(cost, 4))
        '''
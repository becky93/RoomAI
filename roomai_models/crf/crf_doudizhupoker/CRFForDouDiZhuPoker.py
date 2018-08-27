#!/bin/python
import random

from roomai_models.crf.algorithms import CRFPlayer
import roomai.doudizhupoker
import numpy as np
from roomai.doudizhupoker import DouDiZhuPokerHandCards
from roomai.doudizhupoker import DouDiZhuPokerAction
from roomai.doudizhupoker import DouDiZhuPokerEnv
import tensorflow as tf



class CRFForDouDiZhuPokerPlayer(CRFPlayer):

    def __init__(self,model_address = None, params = dict()):
        ### prepare for feature generate ###############
        self.pattern_to_idx = dict()
        self.patterns_list = list(roomai.doudizhupoker.AllPatterns.keys())
        self.patterns_list.sort()
        for p in self.patterns_list:
            self.pattern_to_idx[p] = len(self.pattern_to_idx)

        self.card_to_idx = dict()
        for i in range(3, 10):
            self.card_to_idx[str(i)] = i - 3
        self.card_to_idx["T"] = len(self.card_to_idx)
        self.card_to_idx["J"] = len(self.card_to_idx)
        self.card_to_idx["Q"] = len(self.card_to_idx)
        self.card_to_idx["K"] = len(self.card_to_idx)
        self.card_to_idx["A"] = len(self.card_to_idx)
        self.card_to_idx["2"] = len(self.card_to_idx)
        self.card_to_idx["r"] = len(self.card_to_idx)
        self.card_to_idx['R'] = len(self.card_to_idx)

        self.num_pattern = len(roomai.doudizhupoker.AllPatterns)
        self.num_card = 15


        self.env1 = roomai.doudizhupoker.DouDiZhuPokerEnv()
        self.env1.init({"param_start_turn": 0})
        self.env1.forward(DouDiZhuPokerAction.lookup("b"))
        self.env1.forward(DouDiZhuPokerAction.lookup("x"))
        self.infos1, self.public_state1, self.person_states1, self.private_state1 = self.env1.forward(DouDiZhuPokerAction.lookup("x"))

        self.dim = 6

        ### model ################
        self.learning_rate = 0.001
        if "learning_rate" in params:
            self.learning_rate = params["learning_rate"]

        self.weight_decay = 0.004
        if "weight_decay" in params:
            self.weight_decay = params["weight_decay"]

        self.gamma = 0.9
        if "gamma" in params:
            self.gamma = params["gamma"]

        self.model_address = model_address
        self.graph = tf.Graph()

        with self.graph.as_default() as graph:

            self.strategy_info_action_feats = tf.placeholder(tf.float32, [None, self.num_pattern, self.num_card, self.dim])
            self.strategy_targets           = tf.placeholder(tf.float32, [None,1])

            self.regret_info_action_feats   = tf.placeholder(tf.float32, [None, self.num_pattern, self.num_card, self.dim])
            self.regret_targets             = tf.placeholder(tf.float32, [None,1])


            ############################################## strategy model ###############################################
            ### layer1
            strategy_conv1_weight = tf.get_variable('strategy_conv1w', shape=[3, 3, self.dim, 16],
                                                initializer=tf.contrib.layers.xavier_initializer())
            strategy_conv1 = tf.nn.conv2d(self.strategy_info_action_feats, filter=strategy_conv1_weight, strides=[1, 1, 1, 1], padding='SAME')
            strategy_bias1 = tf.nn.relu(strategy_conv1 + tf.get_variable('strategy_conv1b', shape=[16],
                                                  initializer=tf.contrib.layers.xavier_initializer()))
            strategy_pool1 = tf.nn.max_pool(strategy_bias1, ksize=[1, 2, 2, 1],
                                          strides=[1, 2, 2, 1], padding='SAME')

            ### layer2
            strategy_conv2_weight = tf.get_variable('strategy_conv1w', shape=[3, 3, 16, 32],
                                                initializer=tf.contrib.layers.xavier_initializer())
            strategy_conv2 = tf.nn.conv2d(strategy_pool1, filter=strategy_conv2_weight, strides=[1, 1, 1, 1], padding='SAME')
            strategy_bias2 = tf.nn.relu(strategy_conv2 + tf.get_variable('strategy_conv1b', shape=[32],
                                                  initializer=tf.contrib.layers.xavier_initializer()))
            strategy_pool2 = tf.nn.max_pool(strategy_bias2, ksize=[1, 2, 2, 1],
                                          strides=[1, 2, 2, 1], padding='SAME')

            ### DNN layer1
            strategy_dim0        = 256
            strategy_dnn0        = tf.reshape(strategy_pool2,[-1,strategy_dim0])
            strategy_dnn0_weight = self.__variable_with_weight_decay__(name="strategy_dnn_layer0_w",
                                                                       shape=[strategy_dnn0.get_shape()[1], 512],
                                                                       wd=self.weight_decay)
            strategy_dnn0_bias   = tf.get_variable("strategy_dnn_layer0_b", shape=[512], initializer=tf.contrib.layers.xavier_initializer())
            strategy_dnn1        = tf.nn.relu(tf.matmul(strategy_dnn0, strategy_dnn0_weight) + strategy_dnn0_bias)

            ### DNN layer2
            strategy_dnn1_weight = self.__variable_with_weight_decay__(name="strategy_dnn_layer1_w",
                                                                       shape=[512, 256],
                                                                       wd=self.weight_decay)
            strategy_dnn1_bias = tf.get_variable("strategy_dnn_layer1_b", shape=[256],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            strategy_dnn2 = tf.nn.relu(tf.matmul(strategy_dnn1, strategy_dnn1_weight) + strategy_dnn1_bias)

            ### DNN layer3
            strategy_dnn2_weight = self.__variable_with_weight_decay__(name="strategy_dnn_layer2_w",
                                                                       shape=[256, 1],
                                                                       wd=self.weight_decay)
            strategy_dnn3 = tf.nn.relu(tf.matmul(strategy_dnn1, strategy_dnn1_weight))

            ### strategy_train
            self.strategy      = tf.nn.softmax(tf.reshape(strategy_dnn3,shape = [-1]))
            self.strategy_loss = tf.nn.softmax_cross_entropy_with_logits(labels=self.strategy_targets,logits=self.strategy)
            self.strategy_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
            self.strategy_train_op = self.strategy_optimizer.minimize(self.strategy_loss)

            ############################################## regret model ###############################################
            ### layer1
            regret_conv1_weight = tf.get_variable('regret_conv1w', shape=[3, 3, self.dim, 16],
                                                    initializer=tf.contrib.layers.xavier_initializer())
            regret_conv1 = tf.nn.conv2d(self.regret_info_action_feats, filter=regret_conv1_weight,
                                          strides=[1, 1, 1, 1], padding='SAME')
            regret_bias1 = tf.nn.relu(regret_conv1 + tf.get_variable('regret_conv1b', shape=[16],
                                                                         initializer=tf.contrib.layers.xavier_initializer()))
            regret_pool1 = tf.nn.max_pool(regret_bias1, ksize=[1, 2, 2, 1],
                                            strides=[1, 2, 2, 1], padding='SAME')

            ### layer2
            regret_conv2_weight = tf.get_variable('regret_conv1w', shape=[3, 3, 16, 32],
                                                    initializer=tf.contrib.layers.xavier_initializer())
            regret_conv2 = tf.nn.conv2d(regret_pool1, filter=regret_conv2_weight, strides=[1, 1, 1, 1],
                                          padding='SAME')
            regret_bias2 = tf.nn.relu(regret_conv2 + tf.get_variable('regret_conv1b', shape=[32],
                                                                         initializer=tf.contrib.layers.xavier_initializer()))
            regret_pool2 = tf.nn.max_pool(regret_bias2, ksize=[1, 2, 2, 1],
                                            strides=[1, 2, 2, 1], padding='SAME')

            ### DNN layer1
            regret_dim0 = 256
            regret_dnn0 = tf.reshape(regret_pool2, [-1, regret_dim0])
            regret_dnn0_weight = self.__variable_with_weight_decay__(name="regret_dnn_layer0_w",
                                                                       shape=[regret_dnn0.get_shape()[1], 512],
                                                                       wd=self.weight_decay)
            regret_dnn0_bias = tf.get_variable("regret_dnn_layer0_b", shape=[512],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            regret_dnn1 = tf.nn.relu(tf.matmul(regret_dnn0, regret_dnn0_weight) + regret_dnn0_bias)

            ### DNN layer2
            regret_dnn1_weight = self.__variable_with_weight_decay__(name="regret_dnn_layer1_w",
                                                                       shape=[512, 256],
                                                                       wd=self.weight_decay)
            regret_dnn1_bias = tf.get_variable("regret_dnn_layer1_b", shape=[256],
                                                 initializer=tf.contrib.layers.xavier_initializer())
            regret_dnn2 = tf.nn.relu(tf.matmul(regret_dnn1, regret_dnn1_weight) + regret_dnn1_bias)

            ### DNN layer3
            regret_dnn2_weight = self.__variable_with_weight_decay__(name="regret_dnn_layer2_w",
                                                                       shape=[256, 1],
                                                                       wd=self.weight_decay)
            regret_dnn3 = tf.matmul(regret_dnn2, regret_dnn2_weight)

            ### regret_train
            self.regret      = tf.reshape(regret_dnn3,shape=[-1])
            self.regret_loss = tf.reduce_mean(
                (regret_dnn2 - self.regret_targets) * (regret_dnn2 - self.regret_targets))
            self.regret_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
            self.regret_train_op = self.regret_optimizer.minimize(self.regret_loss)

            self.init = tf.global_variables_initializer()
            self.sess = tf.Session()
            self.sess.run(self.init)
            self.saver = tf.train.Saver(tf.global_variables())

    def __variable_on_cpu__(self,name, shape, initializer):
        """Helper to create a Variable stored on CPU memory.
        Args:
        name: name of the variable
        shape: list of ints
        initializer: initializer for Variable
        Returns:
        Variable Tensor
        """
        with tf.device('/cpu:0'):
            dtype = tf.float32
            var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
        return var

    def __variable_with_weight_decay__(self,name, shape,  wd, stddev = 0.01,):
        """Helper to create an initialized Variable with weight decay.
          Note that the Variable is initialized with a truncated normal distribution.
        A weight decay is added only if one is specified.
        Args:
            name: name of the variable
            shape: list of ints
            stddev: standard deviation of a truncated Gaussian
            wd: add L2Loss weight decay multiplied by this float. If None, weight
            decay is not added for this Variable.
        Returns:
         Variable Tensor
        """
        dtype = tf.float32
        var = self.__variable_on_cpu__(
            name,
            shape,
            tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))
        if wd is not None:
            weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
            tf.add_to_collection('losses', weight_decay)
        return var


    def update_averge_strategies(self, info, actions, targets):
        strategy_info_action_feats = self.gen_info_actions_feat(info, actions)
        self.sess.run(self.strategy_train_op, feed_dict = {self.strategy_info_action_feats:strategy_info_action_feats,
                                                           self.strategy_targets:targets})

    def get_averge_strategies(self, info, actions):
        strategy_info_action_feats = self.gen_info_actions_feat(info, actions)
        return self.sess.run(self.strategy, feed_dict={self.strategy_info_action_feats: strategy_info_action_feats})

    def update_counterfactual_regrets(self, info, actions, targets):
        regret_info_action_feats = self.gen_info_actions_feat(info, actions)
        self.sess.run(self.strategy_train_op, feed_dict = {self.regret_info_action_feats:regret_info_action_feats,
                                                           self.regret_targets:targets})

    def get_counterfactual_regrets(self, info, actions):
        regret_info_action_feats = self.gen_info_actions_feat(info, actions)
        return  self.sess.run(self.regret, feed_dict = {self.regret_info_action_feats:regret_info_action_feats})


    ############################# generate feature #####################
    def available_actions(self, hand_cards_str):
        person_state = self.person_states1[0].__deepcopy__()
        person_state.__hand_cards__ = DouDiZhuPokerHandCards.lookup(hand_cards_str)
        return DouDiZhuPokerEnv.available_actions(self.public_state1, self.person_states1[0])

    def next_hand_cards_str(self, hand_cards_str, action_str):
        hand_cards = DouDiZhuPokerHandCards.lookup(hand_cards_str)
        return hand_cards.remove_cards_of_action(action_str).key

    def gen_info_feat(self, info):
        struct_feat = np.zeros((self.num_pattern, self.num_card))
        for action in info.person_state.available_actions:
            row_id = self.pattern_to_idx[action.pattern[0]]
            col_id = action.maxMasterPoint
            struct_feat[row_id, col_id] += 1.0
        return struct_feat


    def gen_info_actions_feat(self, info, actions):
        x                        = np.zeros((len(actions), self.num_pattern, self.num_card, self.dim))
        current_info_feat        = self.gen_info_feat(info)
        history_action_feats     = [np.zeros((self.num_pattern, self.num_card)) for i in range(3)]

        for idx_action in range(info.public_state.action_history):
            idx             = idx_action[0]
            currrent_idx    = info.person_state.id
            action          = idx_action[1]
            history_action_feats[(idx + 3 -currrent_idx) % 3] += self.gen_action_feat(action)

        for i in range(len(actions)):
            act = actions[i]
            act_feat = self.gen_action_feat(act)

            next_hand_cards_str_key  = self.next_hand_cards_str(info.person_state.hand_cards.key)
            next_hand_cards_feat = self.gen_actions_feat(self.available_actions(next_hand_cards_str_key, "x"))

            x[i, :, :, 0] = current_info_feat
            x[i, :, :, 1] = history_action_feats[0]
            x[i, :, :, 2] = history_action_feats[1]
            x[i, :, :, 3] = history_action_feats[2]
            x[i, :, :, 4] = act_feat
            x[i, :, :, 5] = next_hand_cards_feat

        return x


    ########################## functional ########################
    def receive_info(self, info):
        self.state             = self.gen_state(info)
        self.available_actions = info.person_state.available_actions.values()

    def take_action(self):
        probs = self.get_strategies(self.state, self.available_actions)
        sum1  = sum(probs)
        for i in range(len(self.available_actions)):
            probs[i] /= sum

        r    = random.random()
        sum1 = 0
        for i in range(len(probs)):
            sum1 += probs[i]
            if sum1 > r:
                return self.available_actions[i]

        return self.available_actions[len(self.available_actions)-1]


    def reset(self):
        pass





if __name__ == "__main__":
    env     = DouDiZhuPokerEnv
    player  = CRFForDouDiZhuPokerPlayer()
    import roomai_models.crf.algorithms
    algo    = roomai_models.crf.algorithms.CRFOutSampling
    for i in range(10000):
        algo.dfs(env = env, player=player, p0 = 1, p1 = 1, deep = 0)

    print (player.regrets)
    print (player.strategies)
    player.is_train = False

    import roomai.common
    player_random = roomai.common.RandomPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in range(10000):
        scores = DouDiZhuPokerEnv.compete(env,[player, player_random])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in range(len(sum_scores)):
        sum_scores[i] /= num
    print (sum_scores)






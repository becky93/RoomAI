import models.dqn.dqnalgorithm
import roomai
import roomai.sevenking
import roomai.common
import tensorflow as tf
import numpy as np

import shutil

def remove_path(path):
    shutil.rmtree(path)

class DQN_SevenKing_ThreePlayers(models.dqn.dqnalgorithm.DqnPlayer):
    def __init__(self, model_address = None, params = dict()):
        self.num_point  = 15
        self.num_suit   = 5 ## small king and three king
        self.info_dim   = 8
        self.action_dim = 4

        self.learning_rate = 0.001
        if "learning_rate" in params:
            self.learning_rate = params["learning_rate"]

        self.weight_decay = 0.004
        if "weight_decay" in params:
            self.weight_decay = params["weight_decay"]

        self.gamma      = 0.9
        if "gamma" in params:
            self.gamma = params["gamma"]

        self.model_address = model_address
        self.graph         = tf.Graph()

        with self.graph.as_default() as graph:
            self.info_feats           = tf.placeholder(tf.float32, [None, self.num_point, self.num_suit, self.info_dim])
            self.action_feats         = tf.placeholder(tf.float32, [None, self.num_point, self.num_suit, self.action_dim])
            self.reward_plus_gamma_q  = tf.placeholder(tf.float32, [None])

            ############################################## info feat ###############################################
            info_conv1_weight = tf.get_variable('info_conv1w', shape=[3, 3, self.info_dim, 16],
                                                initializer=tf.contrib.layers.xavier_initializer())
            info_conv1_bias = tf.get_variable('info_conv1b', shape=[16],
                                              initializer=tf.contrib.layers.xavier_initializer())
            info_conv1 = tf.nn.conv2d(self.info_feats, filter=info_conv1_weight, strides=[1, 1, 1, 1], padding='SAME')

            info_h_conv1 = tf.nn.relu(info_conv1 + info_conv1_bias)
            info_h_conv2 = tf.nn.max_pool(info_h_conv1, ksize=[1, 2, 2, 1],
                                          strides=[1, 2, 2, 1], padding='SAME')

            info_conv2_weight = tf.get_variable('info_conv2w', shape=[3, 3, 16, 32],
                                                initializer=tf.contrib.layers.xavier_initializer())
            info_conv2_bias = tf.get_variable('info_conv2b', shape=[32],
                                              initializer=tf.contrib.layers.xavier_initializer())
            info_conv2 = tf.nn.conv2d(info_h_conv2, filter=info_conv2_weight, strides=[1, 1, 1, 1], padding='SAME')

            info_h_conv3 = tf.nn.relu(info_conv2 + info_conv2_bias)
            info_h_conv3 = tf.nn.max_pool(info_h_conv3, ksize=[1, 2, 2, 1],
                                          strides=[1, 2, 2, 1], padding='SAME')
            info_h_conv3_flat = tf.reshape(info_h_conv3, [-1, 256])


            info_vector_weight =  self.__variable_with_weight_decay__(name = 'info_conv_vector_weight', shape = [info_h_conv3_flat.get_shape()[1].value, 512],wd = self.weight_decay)
            info_vector_bias   =  tf.get_variable('info_conv_vector_bias', shape=[512], initializer = tf.contrib.layers.xavier_initializer())
            info_vector_feat   =  tf.matmul(info_h_conv3_flat, info_vector_weight) + info_vector_bias

            ################################################# action feat ############################################
            action_conv1_weight = tf.get_variable('action_conv1w', shape=[3, 3, self.action_dim, 16],
                                                  initializer=tf.contrib.layers.xavier_initializer())
            action_conv1_bias = tf.get_variable('action_conv1b', shape=[16],
                                                initializer=tf.contrib.layers.xavier_initializer())
            action_conv1 = tf.nn.conv2d(self.action_feats, filter=action_conv1_weight, strides=[1, 1, 1, 1],
                                        padding='SAME')

            action_h_conv1 = tf.nn.relu(action_conv1 + action_conv1_bias)
            action_h_conv2 = tf.nn.max_pool(action_h_conv1, ksize=[1, 2, 2, 1],
                                            strides=[1, 2, 2, 1], padding='SAME')

            action_conv2_weight = tf.get_variable('action_conv2w', shape=[3, 3, 16, 32],
                                                  initializer=tf.contrib.layers.xavier_initializer())
            action_conv2_bias = tf.get_variable('action_conv2b', shape=[32],
                                                initializer=tf.contrib.layers.xavier_initializer())
            action_conv2 = tf.nn.conv2d(action_h_conv2, filter=action_conv2_weight, strides=[1, 1, 1, 1],
                                        padding='SAME')

            action_h_conv3 = tf.nn.relu(action_conv2 + action_conv2_bias)
            action_h_conv3 = tf.nn.max_pool(action_h_conv3, ksize=[1, 2, 2, 1],
                                            strides=[1, 2, 2, 1], padding='SAME')
            action_h_conv3_flat = tf.reshape(action_h_conv3, [-1, 256])

            action_vector_weight = self.__variable_with_weight_decay__('action_conv_vector_weight',
                                                                       shape=[action_h_conv3_flat.get_shape()[1].value,
                                                                              512],
                                                                       wd=self.weight_decay)
            action_vector_bias = tf.get_variable('action_conv_vector_bias', shape=[512],
                                               initializer=tf.contrib.layers.xavier_initializer())
            action_vector_feat = tf.matmul(action_h_conv3_flat, action_vector_weight) + action_vector_bias

            ### DNN
            dnn_x           = tf.nn.relu(tf.concat([info_vector_feat, action_vector_feat], axis=1))
            dnn_weight      = self.__variable_with_weight_decay__('dnn_weight',shape=[dnn_x.get_shape()[1].value,256],wd = self.weight_decay)
            dnn_weight_bias = tf.get_variable('dnn_bias', shape=[256], initializer=tf.contrib.layers.xavier_initializer())
            dnn_x1          = tf.nn.relu(tf.matmul(dnn_x, dnn_weight) + dnn_weight_bias)
            dnn_weight1     = self.__variable_with_weight_decay__('dnn_weight1',
                                                             shape=[dnn_x1.get_shape()[1].value, 1],
                                                             wd=self.weight_decay)
            dnn_x2          = tf.matmul(dnn_x1, dnn_weight1)
            self.q          = tf.reduce_mean(dnn_x2,axis = 1)
            self.loss       = tf.reduce_mean((self.q - self.reward_plus_gamma_q) * (self.q - self.reward_plus_gamma_q))
            self.optimizer  = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
            self.train_op   = self.optimizer.minimize(self.loss)

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

    def gen_action_feat(self, info, action):
        action_feat = np.zeros((self.num_point, self.num_suit, self.action_dim))
        for card in action.cards:
            if info.public_state.stage == 0:
                action_feat[card.point_rank, card.suit_rank, 0] += 1
            else:
                action_feat[card.point_rank, card.suit_rank, 1] += 1
        return action_feat

    def gen_info_feat(self, info):
        logger = roomai.get_logger()
        hand_cards = info.person_state.hand_cards
        info_feat = np.zeros((self.num_point, self.num_suit, self.info_dim))

        current_id = info.person_state.id
        previous_id = (current_id + 3 - 1) % 3
        next_id = (current_id + 1) % 3

        if info.public_state.stage == 0:
            for card in hand_cards:
                info_feat[card.point_rank, card.suit_rank, 0] += 1

            for person_action in info.public_state.action_history:
                person_id = person_action[0]
                action    = person_action[1]
                for card in action.cards:
                    if person_id == current_id:
                        info_feat[card.point_rank, card.suit_rank, 1] += 1
                    elif person_id == previous_id:
                        info_feat[card.point_rank, card.suit_rank, 2] += 1
                    elif person_id == next_id:
                        info_feat[card.point_rank, card.suit_rank, 3] += 1
                    elif person_id == 3:
                        logger.debug("SevenKingModel finds the chance player-action pair in public_state.action_history")

        else:
            for card in hand_cards:
                info_feat[card.point_rank, card.suit_rank, 4] += 1

            for person_action in info.public_state.action_history:
                person_id = person_action[0]
                action    = person_action[1]
                for card in action.cards:
                    if person_id == current_id:
                        info_feat[card.point_rank, card.suit_rank, 5] += 1
                    elif person_id == previous_id:
                        info_feat[card.point_rank, card.suit_rank, 6] += 1
                    elif person_id == next_id:
                        info_feat[card.point_rank, card.suit_rank, 7] += 1
                    elif person_id == 3:
                        logger.debug("SevenKingModel finds the chance player-action pair in public_state.action_history")


        return info_feat

    def terminal_info_feat(self):
        info_feat = np.zeros((self.num_point, self.num_suit, self.info_dim))
        return info_feat

    def terminal_action_feat(self):
        action_feat = np.zeros((self.num_point, self.num_suit, self.action_dim))
        return action_feat

    def update_model(self, experiences):
        logger = roomai.get_logger()
        reward_plus_gamma_q = []
        info_feats          = []
        action_feats        = []
        logger = roomai.get_logger()

        for experience in experiences:
            next_action_feats = [action_feat for action_feat in experience.next_available_action_feats]
            next_info_feats   = [experience.next_info_feat for i in range(len(experience.next_available_action_feats))]
            q                 = self.sess.run(self.q, feed_dict = { self.info_feats:next_info_feats,
                                                                    self.action_feats:next_action_feats})

            reward_plus_gamma_q.append(experience.reward + self.gamma * np.max(q))
            info_feats.append(experience.info_feat)
            action_feats.append(experience.action_feat)



        _, loss,q = self.sess.run((self.train_op,self.loss, self.q), feed_dict = { self.info_feats:info_feats,
                                                   self.action_feats:action_feats,
                                                   self.reward_plus_gamma_q:reward_plus_gamma_q})
        #logger.debug ("reward_plus_gamma_q = %s"%(reward_plus_gamma_q.__str__()))
        #logger.debug ("loss = %f"%(loss))
        #logger.debug ("q = %s"%(q.__str__()))

    ################################ player functions ###################
    def receive_info(self,info):
        self.info = info

    def take_action(self):
        info = self.info
        action_feats = []
        action_lists = list(info.person_state.available_actions.values())
        for action in action_lists:
            action_feats.append(self.gen_action_feat(info, action))

        info_feat = self.gen_info_feat(info)
        info_feats = []
        info_feats = [info_feat for i in range(len(action_lists))]

        q = self.sess.run(self.q, feed_dict={self.info_feats: info_feats, self.action_feats: action_feats})
        idx = np.argmax(q)
        return action_lists[idx]

    def reset(self):
        pass


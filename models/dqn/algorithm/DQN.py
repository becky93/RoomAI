#!/bin/python

import random
import roomai.common
from algorithm import Experience
from algorithm import DQNModel
from algorithm import DQNPlayer


class DQN:
    def __init__(self, params = dict()):
        self.memory_p                = 0
        self.memories                = []
        self.uncompleted_experiences = dict()


    def gen_experience(self, model, turn, info, action, reward):

        res = None
        if turn in self.uncompleted_experiences:
            res                             = self.uncompleted_experiences[turn]
            res.next_info_feat              = model.gen_info_feat(info)
            res.next_available_action_feats = []
            for action in list(info.person_state.available_actions.values()):
                res.next_available_action_feats.append(model.gen_action_feat(action))


        self.uncompleted_experiences[turn] = Experience(  turn = turn,
                                                          info_feat = model.gen_info_feat(info),
                                                          action_feat = model.gen_info_feat(action),
                                                          reward = reward,
                                                          next_info_feat= None,
                                                          next_available_action_feats = None)
        return res

    def add_experience_to_memories(self, experience, params):
        max_memory_size = 10000
        if "max_memory_size" in params:
            max_memory_size = params["max_memory_size"]
        if experience is not None:
            if len(self.memories) < max_memory_size:
                self.memories.append(experience)
            else:
                self.memories[self.memory_p] = experience
                self.memory_p = (self.memory_p + 1) % max_memory_size


    def eval(self, model, env, params = dict(), opponents = None):
        model_player = DQNPlayer(model=model)

        scores       = None
        players      = None
        if opponents is not None:
            players = [model_player]+ [opponent for opponent in opponents]
            scores  = [0 for i in range(len(opponents)+1)]

        for iter1 in range(500):
            infos, public_state, _, _ = env.init(params)

            if players is None:
                players = [model_player] + [roomai.common.RandomPlayer() for i in range(len(infos-1))]
                scores = [0 for i in range(len(infos))]

            for i in range(len(infos)):
                players[i].reset()
                players[i].receive_info(infos)

            while public_state.is_terminal != True:
                action = players[public_state.turn]
                infos, public_state, _, _ = env.forward(action=action)
                for i in range(len(infos)):
                    players[i].receive_info(infos)

            score = public_state.scores
            for i in range(len(score)):
                scores[i] += score[i]

        for i in range(len(scores)):
            scores[i] /= 500

        return  scores


    def train(self, model, env, params = dict()):

        num_iters = 100000
        if "num_iters" in params:
            num_iters = params["num_iters"]
        batch_size = 100
        if "batch_size" in params:
            batch_size = params["batch_size"]


        for i in range(num_iters):
            infos, public_state, _, _   = env.init(params)
            action                      = model.take_action(infos[public_state.turn])
            experience                  = self.gen_experience(model, public_state.turn, infos[public_state.turn], action, reward=0)
            self.add_experience_to_memories(experience, params)


            while public_state.is_terminal == False:
                infos, public_state,_, _ = env.forward(action)
                action                   = model.take_action(infos[public_state.turn])
                experience               = self.gen_experience(model,turn = public_state.turn, info = infos[public_state.turn], action = action, reward=0)
                self.add_experience_to_memories(experience)

                experiences_batch = []
                if len(self.memories) > 1000:
                    for i in range(batch_size):
                        idx = int(random.random() * len(self.memories))
                        experiences_batch.append(self.memories[idx])
                    model.update_model(experiences_batch)



            scores = public_state.scores
            for i in range(len(scores)):
                self.uncompleted_experiences[i].reward                      = scores[i]
                self.uncompleted_experiences[i].next_info_feat              = model.terminal_info_feat()
                self.uncompleted_experiences[i].next_available_action_feats = [model.terminal_action_feat()]
                self.add_experience_to_memories(self.uncompleted_experiences[i])
            model.update_model([self.uncompleted_experiences[i] for i in range(len(scores))])

        return model
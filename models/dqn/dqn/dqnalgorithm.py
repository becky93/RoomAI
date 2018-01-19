#!/bin/python

import random
import roomai.common
from dqn import Experience
from dqn import DqnPlayer


class DqnAlgorithm:
    def __init__(self, params = dict()):
        self.memory_p                = 0
        self.memories                = []
        self.uncompleted_experiences = dict()


    def gen_experience_to_memories(self, model, turn, info, action, reward, params):

        res = None
        if turn in self.uncompleted_experiences:
            res                             = self.uncompleted_experiences[turn]
            res.next_info_feat              = model.gen_info_feat(info)
            res.next_available_action_feats = []
            for action in list(info.person_state.available_actions.values()):
                res.next_available_action_feats.append(model.gen_action_feat(info,action))

        self.uncompleted_experiences[turn] = Experience(  turn = turn,
                                                          info_feat = model.gen_info_feat(info),
                                                          action_feat = model.gen_action_feat(info, action),
                                                          reward = reward,
                                                          next_info_feat= None,
                                                          next_available_action_feats = None)

        if res is not None:
            self.add_experience_to_memories(res, params=params)


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

    def eval(self, model, env, opponents, params = dict()):
        logger = roomai.get_logger()
        logger.info("start an evaluation process")

        model_player = DqnPlayer(model=model)
        scores       = None
        players      = None
        if opponents is not None:
            players = [model_player]+ [opponent for opponent in opponents] + [roomai.common.RandomChancePlayer()]
            scores  = [0 for i in range(len(opponents)+1)]

        num_eval = 2000
        for iter1 in range(num_eval):
            infos, public_state, _, _ = env.init(params)

            for i in range(len(infos)):
                players[i].reset()
                players[i].receive_info(infos[i])

            while public_state.is_terminal != True:
                action = players[public_state.turn].take_action()
                infos, public_state, _, _ = env.forward(action=action)
                for i in range(len(infos)):
                    players[i].receive_info(infos[i])

            score = public_state.scores
            for i in range(len(score)):
                scores[i] += score[i]

        for i in range(len(scores)):
            scores[i] /= num_eval

        logger.info("complete an evaluation process, scores = [%s] for [model_player, opponent_player,....]."%(",".join([str(s) for s in scores])))
        return  scores


    def train(self, model, env, params):

        num_iters = 100
        if "num_iters" in params:
            num_iters = params["num_iters"]
        batch_size = 100
        if "batch_size" in params:
            batch_size = params["batch_size"]

        random_chance_player = roomai.common.RandomChancePlayer()
        logger = roomai.get_logger()
        logger.info("start a training process with num_iters = %d"%(num_iters))

        for i in range(num_iters):
            infos, public_state, _, _   = env.init(params)
            action                      = model.take_action(infos[public_state.turn])
            self.gen_experience_to_memories(model, public_state.turn, infos[public_state.turn], action, reward=0, params = params)

            while public_state.is_terminal == False:
                infos, public_state,_, _ = env.forward(action)

                if public_state.is_terminal == False:
                    if public_state.turn != len(infos)-1:
                        action = model.take_action(infos[public_state.turn])
                        #Not Chance Player
                        self.gen_experience_to_memories(model, turn = public_state.turn, info = infos[public_state.turn], action = action, reward=0, params = params)

                        experiences_batch = []
                        if len(self.memories) > 1000 and random.random() < 1.0 / batch_size:
                            for i in range(batch_size):
                                idx = int(random.random() * len(self.memories))
                                experiences_batch.append(self.memories[idx])
                            model.update_model(experiences_batch)
                    else:
                        random_chance_player.receive_info(infos[public_state.turn])
                        action = random_chance_player.take_action()
                else:
                    scores = public_state.scores
                    for i in range(len(scores)):
                        self.uncompleted_experiences[i].reward                      = scores[i]
                        self.uncompleted_experiences[i].next_info_feat              = model.terminal_info_feat()
                        self.uncompleted_experiences[i].next_available_action_feats = [model.terminal_action_feat()]
                        self.add_experience_to_memories(self.uncompleted_experiences[i], params)
                    model.update_model([self.uncompleted_experiences[i] for i in range(len(scores))])

        logger.info("complete a training process")

        return model
#!/bin/python

import random
import roomai.common
from dqn import Experience
from dqn import DqnPlayer


class DqnAlgorithm:
    def __init__(self, params = dict()):
        self.memory_experiences_p    = dict()
        self.memory_experiences      = dict()
        self.uncompleted_experiences = dict()


    def gen_experience_to_memories(self,info, action, reward, player, params):
        turn = info.public_state.turn

        res = None
        if turn in self.uncompleted_experiences:
            res                             = self.uncompleted_experiences[turn]
            res.next_info_feat              = player.gen_info_feat(info)
            res.next_available_action_feats = []
            for action in list(info.person_state.available_actions.values()):
                res.next_available_action_feats.append(player.gen_action_feat(info,action))

        self.uncompleted_experiences[turn] = Experience(  turn = turn,
                                                          info_feat = player.gen_info_feat(info),
                                                          action_feat = player.gen_action_feat(info, action),
                                                          reward = reward,
                                                          next_info_feat= None,
                                                          next_available_action_feats = None)

        if res is not None:
            self.add_experience_to_memory(experience = res, playerid= turn, params=params)


    def add_experience_to_memory(self, experience, playerid, params):
        if playerid not in self.memory_experiences:
            self.memory_experiences[playerid]   = []
            self.memory_experiences_p[playerid] = 0

        max_memory_size = 10000
        if "max_memory_size" in params:
            max_memory_size = params["max_memory_size"]
        if experience is not None:
            if len(self.memory_experiences[playerid]) < max_memory_size:
                self.memory_experiences[playerid].append(experience)
            else:
                self.memory_experiences[playerid][self.memory_experiences_p[playerid]] = experience
                self.memory_experiences_p[playerid] = (self.memory_experiences_p[playerid] + 1) % max_memory_size

    def eval(self, env, players, params = dict()):
        logger = roomai.get_logger()
        logger.info("start an evaluation process")

        scores = [0 for i in range(len(players)-1)] ### The last one is the chance player
        num_eval = 1000
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


    def train(self, env, players, params):

        num_iters = 100
        if "num_iters" in params:
            num_iters = params["num_iters"]
        batch_size = 100
        if "batch_size" in params:
            batch_size = params["batch_size"]
        exploit_ratio = 0.9
        if "exploit_ratio" in params:
            exploit_ratio = params["exploit_ratio"]

        logger = roomai.get_logger()
        logger.info("start a training process with num_iters = %d"%(num_iters))

        for i in range(num_iters):
            infos, public_state, _, _   = env.init(params)
            for i in range(len(infos)):
                players[i].receive_info(infos[i])

            while public_state.is_terminal == False:
                ## The chance event
                if public_state.turn == len(infos) - 1:
                    infos, public_state,_, _ = env.forward(players[-1].take_action())
                    continue

                ### choose the action
                if random.random() < exploit_ratio:
                    action = players[public_state.turn].take_action()
                else:
                    action_list = list(infos[public_state.turn].person_state.available_actions.values())
                    action = action_list[int(random.random() * len(action_list))]

                ### generate experiences, add them to memory, and update model
                self.gen_experience_to_memories(players[public_state.turn], public_state.turn, infos[public_state.turn], action, reward=-1, params=params)
                experiences_batch = []
                if len(self.memory_experiences[public_state.turn]) > 1000 and random.random() < 1.0 / batch_size:
                    for i in range(batch_size):
                        idx = int(random.random() * len(self.memories))
                        experiences_batch.append(self.memories[idx])
                players[public_state.turn].update_model(experiences_batch)

                ### the game goes forward
                infos, public_state,_, _ = env.forward(action)


            scores = public_state.scores
            for i in range(len(scores)):
                if i not in self.uncompleted_experiences:continue
                self.uncompleted_experiences[i].reward                      = scores[i]
                self.uncompleted_experiences[i].next_info_feat              = players[i].terminal_info_feat()
                self.uncompleted_experiences[i].next_available_action_feats = [players[i].terminal_action_feat()]
                self.add_experience_to_memory(self.uncompleted_experiences[i], i, params)
                experiences_batch = []
                for i in range(batch_size):
                    idx = int(random.random() * len(self.memory_experiences[i]))
                    experiences_batch.append(self.memory_experiences[i][idx])
                players[i].update_model(experiences_batch)
            self.uncompleted_experiences = dict()

        logger.info("complete a training process")

        return players
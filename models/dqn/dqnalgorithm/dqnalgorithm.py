#!/bin/python

import random
import roomai.common
from modelzoo.dqn.dqnalgorithm import Experience
from modelzoo.dqn.dqnalgorithm import DqnPlayer



class DqnAlgorithm:
    def __init__(self, params = dict()):
        self.memory_experiences_p    = dict()
        self.memory_experiences      = dict()
        self.uncompleted_experiences = dict()


    def gen_experience_to_memories(self,info, action, reward, player, params):
        turn = info.public_state.turn
        if turn not in self.memory_experiences:
            self.memory_experiences[turn] = []
            self.memory_experiences_p[turn] = 0

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
                    action = players[-1].take_action()
                    infos, public_state,_, _ = env.forward(action)
                    for i in range(len(infos)):
                        players[i].receive_info(infos[i])
                    continue


                ## only train DqnPlayer
                if isinstance(players[public_state.turn], DqnPlayer) == False:
                    action = players[public_state.turn].take_action()
                    infos, public_state, _, _ = env.forward(action)
                    for i in range(len(infos)):
                        players[i].receive_info(infos[i])
                    continue

                ### choose the action
                if random.random() < exploit_ratio:
                    action = players[public_state.turn].take_action()
                else:
                    action_list = list(infos[public_state.turn].person_state.available_actions.values())
                    action = action_list[int(random.random() * len(action_list))]

                ### generate experiences, add them to memory, and update model
                self.gen_experience_to_memories(info = infos[public_state.turn], action = action, reward=-1,
                                                player= players[public_state.turn], params=params)
                experiences_batch = []
                if len(self.memory_experiences[public_state.turn]) > 1000 and random.random() < 1.0 / batch_size:
                    for i in range(batch_size):
                        idx = int(random.random() * len(self.memory_experiences[public_state.turn]))
                        experiences_batch.append(self.memory_experiences[public_state.turn][idx])
                    players[public_state.turn].update_model(experiences_batch)
                    logger.debug("update the model")

                ### the game goes forward
                infos, public_state,_, _ = env.forward(action)
                for i in range(len(infos)):
                    players[i].receive_info(infos[i])


            scores = public_state.scores
            for playerid in range(len(scores)):
                if playerid not in self.uncompleted_experiences:continue
                if isinstance(players[playerid], DqnPlayer) == False: continue
                experience = self.uncompleted_experiences[playerid]
                experience.reward                      = scores[playerid]
                experience.next_info_feat              = players[playerid].terminal_info_feat()
                experience.next_available_action_feats = [players[playerid].terminal_action_feat()]
                self.add_experience_to_memory(experience, playerid, params)
                experiences_batch = []
                for i in range(batch_size-1):
                    idx = int(random.random() * len(self.memory_experiences[playerid]))
                    experiences_batch.append(self.memory_experiences[playerid][idx])
                experiences_batch.append(experience)
                players[playerid].update_model(experiences_batch)
            self.uncompleted_experiences = dict()

        logger.info("complete a training process")

        return players
#!/bin/python

from Experience import Experience
import random

class DQN:
    def __init__(self, model, env, params):
        self.model                   = model
        self.env                     = env
        self.memories                = []
        self.uncompleted_experiences = dict()
        self.params                  = params


    def gen_experience(self, turn, info, action, reward):

        res = None
        if turn in self.uncompleted_experiences[turn]:
            res                             = self.uncompleted_experiences[turn]
            res.next_info_feat              = self.model.gen_info_feat(info)
            res.next_available_action_feats = []
            for action in list(info.available_actions.values()):
                res.next_available_action_feats.append(self.model.gen_action_feat(action))


        self.uncompleted_experiences[turn] = Experience( turn = turn,
                                                    info_feat = self.model.gen_info_feat(info),
                                                    action_feat = self.model.gen_info_feat(action),
                                                    reward = reward,
                                                    next_info_feat= None,
                                                    next_available_action_feats = None)
        return res

    def add_experience_to_memories(self, experience):
        max_memory_size = 10000
        if "max_memory_size" in self.params:
            max_memory_size = self.params["max_memory_size"]
        if experience is not None:
            if len(self.memories) < max_memory_size:
                self.memories.append(experience)
            else:
                idx = int(random.random() * len(self.memories))
                self.memories[idx] = experience



    def run(self):

        num_iters = 100000
        if "num_iters" in self.params:
            num_iters = self.params["num_iters"]
        batch_size = 100
        if "batch_size" in self.params:
            batch_size = self.params["batch_size"]


        for i in range(num_iters):
            infos, public_state, _, _   = self.env.init()
            action                      = self.model.predict_q(infos[public_state.turn])
            experience                  = self.gen_experience(public_state.turn, infos[public_state.turn], action, reward=0)
            self.add_experience_to_memories(experience)


            while public_state.is_terminal == False:
                infos, public_state,_, _ = self.env.forward(action)
                action                   = self.model.predict_q(infos[public_state])
                experience               = self.gen_experience(public_state.turn, infos[public_state.turn], action)
                self.add_experience_to_memories(experience)

                experiences = []
                if len(self.memories) > 1000:
                    for i in range(batch_size):
                        idx = int(random.random() * len(self.memories))
                        experiences.append(self.memories[idx])
                    self.model.update_model(experiences)



            scores = public_state.scores
            for i in range(len(scores)):
                self.uncompleted_experiences[i].reward                      = scores[i]
                self.uncompleted_experiences[i].next_info_feat              = self.model.terminal_info_feat()
                self.uncompleted_experiences[i].next_available_action_feats = [self.model.terminal_action_feat()]
                self.add_experience_to_memories(self.uncompleted_experiences[i])
            self.model.update_model([self.uncompleted_experiences[i] for i in range(len(scores))])

            
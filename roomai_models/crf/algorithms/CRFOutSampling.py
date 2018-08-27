import roomai.common
import roomai
import random

def sampling(probs):
    logger = roomai.get_logger()
    r = random.random()
    sum1 = 0
    for i in range(len(probs)):
        sum1 += probs[i]
        if sum1 > r:
            return i

    logger.warn("Sampling probs(%s) with r = %f occurs sum(probs) >= r", ",".join([str(i) for i in probs]), r)
    return len(probs)-1

class CRFOutSampling(object):

    def dfs(self, env, player, current_player_idx,reach_probs, action = None, deep = 0):

        if deep == 0:
            infos, public_state, person_states, private_state = env.init({"param_backward_enable": True})
        else:
            infos, public_state, person_states, private_state = env.forward(action)

        print ("deep = %d, param_backward_enable = %s， turn = %d， is_terminal = %s" %(deep, env.public_state.param_backward_enable, public_state.turn, public_state.is_terminal))

        utility_multiply_prob = 1
        if public_state.is_terminal == True:
            utility = public_state.scores
            utility_multiply_prob = utility[current_player_idx] * 1
        elif public_state.turn == 3: ### chance player
            turn                       = public_state.turn
            available_actions          = list(infos[turn].person_state.available_actions.values())
            choose_action              = available_actions[int(random.random() * len(available_actions))]
            utility_multiply_prob      = self.dfs(env, player,current_player_idx, reach_probs=reach_probs, action = choose_action, deep = deep + 1)
        else:
            ### prepare for the basic data
            turn                   = public_state.turn
            available_actions      = list(infos[turn].person_state.available_actions.values())
            num_available_actions  = len(available_actions)
            counterfactual_regrets = player.get_counterfactual_regrets(infos[turn], available_actions)
            averge_strategies      = player.get_averge_strategies(infos[turn], available_actions)


            ### sampling one path
            choose_action_idx                     = sampling(averge_strategies)
            choose_action                         = available_actions[choose_action_idx]
            new_reach_probs                       = list(reach_probs)
            new_reach_probs[turn]                 = reach_probs[turn] * averge_strategies[choose_action_idx]
            utility_multiply_prob                 = self.dfs(env, player, current_player_idx, new_reach_probs, choose_action, deep + 1)

            if current_player_idx  == turn:
                utility_multiply_prob = utility_multiply_prob * averge_strategies[choose_action_idx]

                ### update new counterfactual_values
                prod1 = 1
                for i in range(len(reach_probs)):
                    if i != current_player_idx: prod1 *= reach_probs[i]
                counterfactual_regrets[choose_action_idx] = prod1 * utility_multiply_prob
                player.update_counterfactual_regrets(infos[turn], available_actions, counterfactual_regrets)

                ### computing immediate regret and current_strategy
                mean_counterfactual_regret = sum(counterfactual_regrets) / len(counterfactual_regrets)
                immediate_regret          = [counterfactual_regrets[i] - mean_counterfactual_regret for i in range(len(counterfactual_regrets))]
                cur_strategy = [0 for i in range(num_available_actions)]
                sum1 = 0
                for i in range(num_available_actions):
                    sum1 += max(0, immediate_regret[i])
                for i in range(num_available_actions):
                    if sum1 > 0:
                        cur_strategy[i] = max(0, immediate_regret[i]) / sum1
                    else:
                        cur_strategy[i] = 1.0 / num_available_actions

                #### update average strategy
                new_strategies = [0 for i in range(num_available_actions)]
                for i in range(num_available_actions):
                    ## 李博帮忙看下这里对不对
                    new_strategies[i] = averge_strategies[i] + reach_probs[turn] * cur_strategy[i]
                sum1 = sum(new_strategies)
                for i in range(num_available_actions):
                    new_strategies[i] = new_strategies[i] /  sum1

                player.update_averge_strategies(infos[turn], available_actions, new_strategies)


        if deep != 0:
            if env.public_state.param_backward_enable == False:
                xxx = 0
                yyy = 0
            env.backward()

        return utility_multiply_prob






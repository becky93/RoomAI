#!/bin/python
import unittest
import roomai.bridge
import roomai
import roomai.common
from functools import cmp_to_key

def compare_action(a,b):
    return a.key > b.key

if __name__ == "__main__":
    import time
    import logging
    roomai.set_loglevel(logging.DEBUG)
    start = time.time()
    for iter in range(1000):
        env = roomai.bridge.BridgeEnv()
        allcards = list(roomai.bridge.AllBridgePlayingPokerCards.values())
        allcards.sort(key = cmp_to_key(roomai.common.PokerCard.compare))
        infos, public_state, person_states, private_state = env.init({ "start_turn":0})
        env.__deepcopy__()

        #### bidding stage
        action = roomai.bridge.BridgeAction.lookup("bidding_bid_A_Heart")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_double")
        infos, public_state, person_states, private_state = env.forward(action)
        action = roomai.bridge.BridgeAction.lookup("bidding_pass")
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)
        infos, public_state, person_states, private_state = env.forward(action)

        #### playing_stage
        count = 0
        while env.public_state.is_terminal == False:
            logger = roomai.get_logger()

            actions = list(env.person_states[env.public_state.turn].available_actions.values())
            actions.sort(key = cmp_to_key(compare_action))
            action  = actions[0]
            logger.debug("turn=%d\tcontract_card = %s\taction = %s"%(env.public_state.turn, env.public_state.playing_contract_card.key,action.key))
            env.forward(action)
            count += 1
        logger.info("completes a game\n\n\n\n\n\n\n")

    end = time.time()
    print (end-start)
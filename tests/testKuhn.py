import unittest
import roomai.kuhnpoker
import roomai.common

class KuhnTester(unittest.TestCase):
    """
    """
    def testKuhn(self):
        """

        """
        for i in range(1000):
            players = [roomai.kuhnpoker.Example_KuhnPokerAlwaysBetPlayer() for i in range(2)] + [roomai.kuhnpoker.KuhnPokerChancePlayer()]
            env     = roomai.kuhnpoker.KuhnPokerEnv()
            infos,public_state,_,_ = env.init()


            for i in range(len(players)):
                players[i].receive_info(infos[i])

            while public_state.is_terminal == False:
                turn = infos[-1].public_state.turn
                action = players[turn].take_action()

                infos,public_state,_,_ = env.forward(action)
                for i in range(len(players)):
                    players[i].receive_info(infos[i])

            print (env.public_state.scores)

    def testKuhnEnvBackward(self):
        env = roomai.kuhnpoker.KuhnPokerEnv()
        env.init({"param_backward_enable":True})
        env.forward(roomai.kuhnpoker.KuhnPokerActionChance.lookup("0,2"))

        action = roomai.kuhnpoker.KuhnPokerAction("bet")
        infos, public_state, person_states, private_state = env.forward(action)
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 2)

        infos, public_state, person_states, private_state = env.forward(roomai.kuhnpoker.KuhnPokerAction("bet"))
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 3)

        infos, public_state, person_states, private_state = env.backward()
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 2)

    def testCompete(self):
        players = [roomai.kuhnpoker.Example_KuhnPokerAlwaysBetPlayer() for i in range(2)]
        env = roomai.kuhnpoker.KuhnPokerEnv()


        env.compete(env, players + [roomai.common.RandomPlayerChance()])

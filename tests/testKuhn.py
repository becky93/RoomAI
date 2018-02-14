import unittest
import roomai.kuhn
import roomai.common

class KuhnTester(unittest.TestCase):
    """
    """
    def testKuhn(self):
        """

        """
        for i in range(1000):
            players = [roomai.kuhn.Example_KuhnPokerAlwaysBetPlayer() for i in range(2)] + [roomai.kuhn.KuhnPokerChancePlayer()]
            env     = roomai.kuhn.KuhnPokerEnv()
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
        env = roomai.kuhn.KuhnPokerEnv()
        env.init({"backward_enable":True})
        env.forward(roomai.kuhn.KuhnPokerActionChance.lookup("0,2"))

        action = roomai.kuhn.KuhnPokerAction("bet")
        infos, public_state, person_states, private_state = env.forward(action)
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 2)

        infos, public_state, person_states, private_state = env.forward(roomai.kuhn.KuhnPokerAction("bet"))
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 3)

        infos, public_state, person_states, private_state = env.backward()
        print (public_state.action_history,person_states[public_state.turn].id)
        assert(len(public_state.action_history) == 2)

    def testCompete(self):
        players = [roomai.kuhn.Example_KuhnPokerAlwaysBetPlayer() for i in range(2)]
        env = roomai.kuhn.KuhnPokerEnv()


        env.compete(env, players + [roomai.common.RandomPlayerChance()])

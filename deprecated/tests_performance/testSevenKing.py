#!/bin/python
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingPokerCard
import roomai.common
import unittest

class AlwaysFoldPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """

        if "" not in self.available_actions:
            min_card = None
            for a in self.available_actions.values():
                if a.pattern[0] == "p_0":
                    if min_card is None:    min_card = a.hand_card[0]
                    else:
                        card = a.hand_card[0]
                        if SevenKingPokerCard.compare(card, min_card) < 0 : min_card = card
            if min_card is None:
                return list(self.available_actions.values())[0]
            else:
                return SevenKingAction.lookup(min_card.key)
        else:
            return SevenKingAction("")

    def receive_info(self,info):
        """

        Args:
            info:
        """
        self.public_state      = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysNotFoldPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """
        for a in self.available_actions.values():
            if a.key != "":
                return a
        return SevenKingAction.lookup("")

    def receive_info(self, info):
        """

        Args:
            info:
        """
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysMinPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """
        min_card = None
        for a in self.available_actions.values():
            if a.pattern[0] == "p_1":
                if min_card is None:    min_card = a.cards[0]
                else:
                    card = a.cards[0]
                    if SevenKingPokerCard.compare(card, min_card) < 0 : min_card = card
        if min_card is None:
            return list(self.available_actions.values())[0]
        else:
            return SevenKingAction.lookup(min_card.key)

    def receive_info(self,info):
        """

        Args:
            info:
        """
        self.public_state      = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysMaxPlayer(roomai.common.AbstractPlayer):
            """
            """

            def take_action(self):
                """

                Returns:

                """
                max_action = SevenKingAction.lookup("")
                max_pattern = 0
                for a in self.available_actions.values():
                    if (a.pattern[1] > max_pattern):
                        max_pattern = a.pattern[1]
                        max_action = a
                    elif (a.pattern[1] == max_pattern):
                        if (a.pattern[0] != 'p_0' and (SevenKingPokerCard.compare(a.cards[-1], max_action.cards[-1]) > 0)):
                            max_action = a

                return max_action

            def receive_info(self, info):
                """

                Args:
                    info:
                """
                self.public_state = info.public_state
                self.available_actions = info.person_state.available_actions

            def reset(self):
                """

                """
                pass


class testSevenKing(unittest.TestCase):
    """
    """

    def show_hand_card(self,hand_card):
        """

        Args:
            hand_card:
        """
        print (",".join([c.key for c in hand_card]))
    def testEnv(self):
        """

        """
        env = SevenKingEnv()

        infos, public_state, person_states, private_state = env.init({"param_num_normal_players":2})
        assert(len(infos) == 2)
        turn = public_state.turn
        self.show_hand_card(person_states[turn].hand_cards)
        print (turn)
        print ("available_actions=",person_states[turn].available_actions.keys())
        print ("available_actions_v=",person_states[turn].available_actions.values())

#      it may go wrong
        action = SevenKingAction("%s,%s" % (person_states[turn].hand_cards[0].key, person_states[turn].hand_cards[1].key))
     #   infos, public_state, person_states, private_state = env.forward(action)


    def testRandom(self):
        """

        """
        env = SevenKingEnv()
        env.num_normal_players = 2
        players = [roomai.common.RandomPlayer() for i in range(2)]

        for i in range(100):
            SevenKingEnv.compete_silent(env, players)

    def testScores(self):
        """

        """
        env = SevenKingEnv()
        env.num_normal_players = 3

        print ("aaa")
        players = [AlwaysFoldPlayer(), AlwaysFoldPlayer(), AlwaysNotFoldPlayer()]
        scores  = env.compete_silent(env, players)
        print (scores)

        self.assertEqual(scores[0],-1)
        self.assertEqual(scores[1],-1)
        self.assertEqual(scores[2],2)

    def testScores1(self):
        """

        """
        env = SevenKingEnv()
        infos, public_state, person_states, private_state = env.init()

        self.assertTrue("" not in infos[public_state.turn].person_state.available_actions)
        self.assertFalse(env.is_action_valid(SevenKingAction.lookup(""),public_state, person_states[public_state.turn]))


if __name__ == "__main__":
    env = SevenKingEnv()
    players = [AlwaysMaxPlayer(), AlwaysNotFoldPlayer(), AlwaysMinPlayer(), roomai.common.RandomPlayer()]
    import time
    start =time.time()
    for i in range(10):
        scores = env.compete_silent(env, players)
        print(scores)
    end = time.time()
    print (end-start)

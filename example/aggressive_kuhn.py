#!bin/python
import roomai.common
import roomai.kuhnpoker

class AggressiveKuhnPlayer(roomai.common.AbstractPlayer):
    def receive_info(self, info):
        self.number = info.person_state.number
    def take_action(self):
        if self.number >= 1:
            return roomai.kuhnpoker.KuhnPokerAction.lookup("bet")
        else:
            return roomai.kuhnpoker.KuhnPokerAction.lookup("check")
    def reset(self):
        pass

if __name__ == "__main__":

        players        = [AggressiveKuhnPlayer()] + [roomai.common.RandomPlayer()] + [roomai.common.RandomPlayerChance()]
        players_random = [roomai.common.RandomPlayer() for i in range(2)] + [roomai.common.RandomPlayerChance()]
        env = roomai.kuhnpoker.KuhnPokerEnv()

        total_scores = [0,0]
        total_scores_random = [0,0]
        for i in range(10000):
            scores = roomai.kuhnpoker.KuhnPokerEnv.compete(env, players)
            total_scores[0] += scores[0]
            total_scores[1] += scores[1]

            scores = roomai.kuhnpoker.KuhnPokerEnv.compete(env, players_random)
            total_scores_random[0] += scores[0]
            total_scores_random[1] += scores[1]

        total_scores = [s/10000 for s in total_scores]
        total_scores_random = [s/10000 for s in total_scores_random]
        print ("aggressive_vs_random",total_scores)
        print ("random_vs_random",total_scores_random)
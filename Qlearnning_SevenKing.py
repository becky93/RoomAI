import roomai.sevenking
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingPokerCard
from roomai.sevenking import  SevenKingPlayer as skp
from roomai.sevenking import  SevenKingEnv

if __name__ == '__main__':
    env = SevenKingEnv()
    players = [skp.AlwaysMaxPlayer(), skp.AlwaysMaxPatternPlayer(), skp.AlwaysMinPlayer(), roomai.common.RandomPlayer()]
    import time

    start = time.time()
    for i in range(10):
        scores = env.compete(env, players)
        print(scores)
    end = time.time()
    print(end - start)
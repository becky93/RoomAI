# Guides for AI Developers

This is some guides for the people, who want to develop some AI bots. To develop an AI bot is
 to implement a player class with your strategy. There are some common steps of developing AI bots.
 
##### Step 1: Work out a Strategy

The first step of developing an AI bot is to work out a strategy. 

We take SevenKing for example. In the game of SevenKing, 
multi-players use a deck of poker cards, the descending order of the rank of cards is 7, King, Wang, 5, 2, 3, A, K, Q, J, 10, 9, 8, 6, 4.
There are two stages: the preparing and play stages. In the preparing stage, each player receives 5 cards in beginning of this stage, and receives x cards after playing x cards (There are always 5 cards in each player). In the play stage, the player, who is first to play all his hand cards, is the winner. 



##### Step 2: Access the State of the Game


##### Step 3: Write the Code

<pre>
class ExamplePlayer(roomai.common.AbstractPlayer):
    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions
            
    def take_action(self):
        values = self.available_actions.values()
        return list()[int(random.random() * len(values))]
        
    def reset(self):
        pass
</pre>





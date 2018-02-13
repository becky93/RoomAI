# Guides for AI Developers

This is some guides for developers, who want to add some games into RoomAI. There are some common steps.

##### Step 1: Choose the Game

The first step is to choose the game, which you want to add into RoomAI. 

##### Step 2: Make the Game into the Extensive Form Game.

The difference between the common game and the extensive form game is [the chance player](fqa.md#).There are some random events in the games. For example, the initialized hand cards in players are due to "Nature". The extensive form game adds "Nature" as a player, who decides the samples of these random events. 
 We call the "Nature" player as the chance player. 
  
##### Step 3: Implement the Game

Write Python 2/3 compatible code to implement your game.

##### Step 4: Test

Write the unittest code to ensure the correctness of your game. Improve the performance of your game. The suggestion baseline of the performance is
100 competitions per second with 4-6 random players.

##### Step 5: Documents

Write the comment using the reStructureText Docstring format.


 



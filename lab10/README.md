Lab 10 
This lab was made with Salvatore Tartaglione s317815

We implemented Q-Learning model free approach to solve the TicTacToe game. The interesting points are:

-class QLearning : we have defined here the Qtable as a dictionary of float that we used to choose the best action, then we have defined the other parameters and the functions that are useful to the Q value evaluation and update.

-function train: we've trained the model by taking in account the fact that the agent could play first or second during a game assuming that the player x is starting always firstly in our game.

-function game: it is the function which is simulating the game between the Q-Learning agent and a random player. We have taken in account that the agent can start first or second depending on the variable agent_player.

-function search_best_parameters: this function tries different values for tuning the parameters of the Q-Learning agent and it returns the best Q-Learning agent with the best parameters.

We have also changed the state_value function in which ,depending on who is the agent, the function returns 1 if the agent wins. 

The variable agent_player is the one which decides who is the agent.

After running the code we've found these best results:

X as agent (first player):
    Best parameters found
    Epsilon: 0.1
    Alpha: 0.2
    Discount Factor: 1.0

    Results:
    Percentage wins of the agent: 87.4%
    Percentage wins of the random player: 8.799999999999999%
    Percentage of draws: 3.8%
    Percentage wins of the agent with respect to the random player: 90.85239085239085%

O as agent (second player):
    Best parameters found
    Epsilon: 0.1
    Alpha: 0.2
    Discount Factor: 0.3

    Results:
    Percentage wins of the agent: 53.6%
    Percentage wins of the random player: 38.6%
    Percentage of draws: 7.8%
    Percentage wins of the agent with respect to the random player: 58.13449023861171%
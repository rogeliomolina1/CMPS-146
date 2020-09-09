# MCTS-CMPM146
Teammate was Marcus Nikaido
The modification made to mcts_modified was in the rollout function.
Instead of simulating with pure randomness we checked if there was a possible next move that resulted in a win. If there was we took it if not we chose a random move while avoiding choosing a move that resulted in the opponent winning.

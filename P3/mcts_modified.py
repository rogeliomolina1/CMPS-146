
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.
# Teammate was Marcus Nikaido
def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    if identity == board.current_player(state):
        return (sorted(list(node.child_nodes.values()), key = lambda c: c.wins/c.visits + sqrt(2*log(node.visits)/c.visits))[-1])
    else:
        return (sorted(list(node.child_nodes.values()), key = lambda c:(1-(c.wins/c.visits)) + sqrt(2*log(node.visits)/c.visits))[-1])
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    newMove = choice(node.untried_actions)
    newState = board.next_state(state, newMove)
    new_node = MCTSNode(node, newMove, board.legal_actions(newState))
    node.child_nodes[newMove] = new_node
    node.untried_actions.remove(newMove)
    return (new_node)
    # Hint: return new_node




def rollout(board, state, identity):
    """ Given the state of the game, the rollout plays out the remainder randomly.
    Args:
        board:  The game setup.
        state:  The state of the game.
    """
    while not board.is_ended(state):
        for moves in board.legal_actions(state):
            tempState = state
            tempState = board.next_state(tempState, moves)
            if board.is_ended(tempState) and board.current_player(tempState) == identity:
                return(tempState)
                break
            elif board.is_ended(tempState) and board.current_player(tempState) != identity:
                board.legal_actions(state).remove(moves)
                continue
        move = choice(board.legal_actions(state))
        state = board.next_state(state, move)
    return(state)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node:
        node.visits += 1
        if won == 1:
            node.wins += 1
        node = node.parent

    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        while node.untried_actions == [] and list(node.child_nodes.values()) != []:
            node = traverse_nodes(node, board, sampled_game, identity_of_bot)
            sampled_game = board.next_state(sampled_game, node.parent_action)
        if(node.untried_actions != []):
            node = expand_leaf(node, board, sampled_game)

        rollout_state = rollout (board, sampled_game, identity_of_bot)
        backpropagate(node, board.points_values(rollout_state)[identity_of_bot])
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return (sorted(list(root_node.child_nodes.values()), key = lambda c: c.visits)[-1].parent_action)
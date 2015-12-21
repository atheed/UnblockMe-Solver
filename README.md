# Unblock Me - Solver
This is a solver for the classic puzzle game, [Unblock Me](https://play.google.com/store/apps/details?id=com.kiragames.unblockmefree&hl=en), that uses A* heuristic search and other artificial intelligence techniques to find a path of moves from an initial board to a goal/winning state.

This problem was modeled as a search problem, where the "target block" must reach a "goal state" through a sequence of moves (the path for which is of interest to us). 

##Statespace

###States
A state is simply any configuration of the blocks on the board (see Usage to see what an initial board looks like). Each state is uniquely represented by the position of each block on our 6 x 6 board.

###Actions
The actions in the statespace relate to moving any one block on the board a certain number of spaces. The three allowed actions are:

1. Move a vertically-oriented block up or down X number of spaces
2. Move a horizontally-oriented block left or right X number of spaces
3. Move the [horizontally-oriented] target block left or right X number of spaces

###Initial/Starting State
The initial state of our problem is any configuration of the board, which can be specified in `unblockme_sample_run.py`, as specified below (see Usage).

###Goal State
The goal state in this statespace is when the target block has no other blocks obstructing it, and is directly in front of the receptacle/goal (located at position `(2, 4)` on the board. 

###Heuristic
The heuristic that was used was the sum of two things:

1. Number of spaces (i.e. distance) between the target block and the receptacle (i.e. the 'goal' that the target block must reach)
2. Number of “moves” to unblock the target block. That is, the number of spaces needed to
move each of the blocks obstructing the target block so that they are no longer
blocking it (under the assumption that those obstructing blocks are not
blocked)

This heuristic is both [admissible](https://en.wikipedia.org/wiki/Admissible_heuristic) and [monotonic](https://en.wikipedia.org/wiki/Consistent_heuristic) (a.k.a consistent).

##Usage
To use the solver, you will require Python 3 (the solver was formally tested only on Python 3.4.3, but should work fine on any Python 3.x). 
Download the files from this repo, and in the terminal, simply run (where `python` is the version as specified in the previous sentence):

```
python unblockme_sample_run.py
```

Note: You may edit `unblockme_sample_run.py` to add/remove/change the given sample boards. You will notice in the file that a sample board can be initialized as below:

```python
board = make_init_state(
		[["B1", 2, V, (0, 0)],
         ["B2", 2, H, (0, 1)],
         ["B3", 3, V, (1, 2)],
         ["B4", 3, H, (5, 0)],
         ["B5", 3, V, (0, 5)], 
         ["B6", 3, H, (3, 3)],
         ["B7", 2, V, (4, 4)]
         ], (2, 0))
```

As can be seen, there are 7 'blocks' in the above sample board. Each block must have:

* a `String`  name (e.g. 'B3')
* an `int` length (e.g. 3)
* an orientation (either 'H' for horizontal, or 'V' for vertical), AND
* a "starting position" -- this is an `(int, int)` tuple denoting the location of the "top-leftmost" part of a block

The final component to initialize a board is the starting position of the target block (the target's starting position is defined the same as for other blocks). In the above, the target's starting position is `(2, 0)`, as specified by the final argument to `make_init_state()`.

Once a block has been specified (as above), the solver can be run on the board by adding the following two lines:

```python
se = SearchEngine('astar', 'full')
se.search(board, unblockme_goal_fn, heur_num_blocks_blocking)
```

where  `board` is the newly initialized board configuration, `unblockme_goal_fn` is the 'goal state' function (checks if the current configuration of the board has reached the goal state, and `heur_num_blocks_blocking` is the heuristic function. 

Enjoy!
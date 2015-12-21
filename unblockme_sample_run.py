from unblockme import *
V = "vertical"
H = "horizontal"

if __name__ == '__main__':
    
    beginner_board_1 = make_init_state(
        [["B1", 3, V, (0, 0)],
         ["B2", 2, H, (0, 1)],
         ["B3", 2, V, (3, 0)],
         ["B4", 2, H, (4, 1)],
         ["B5", 3, V, (1, 3)], 
         ["B6", 3, H, (5, 2)],
         ["B7", 3, V, (3, 5)]
         ], (2, 1))
    # ----------------------------
    # For the above board:
    # Search time = 0.009999999999999995
    # Num moves = 4
 
    beginner_board_2 = make_init_state(
        [["B1", 3, H, (0, 0)],
         ["B2", 3, V, (1, 2)],
         ["B3", 2, V, (3, 0)],
         ["B4", 3, H, (5, 0)],
         ["B5", 2, H, (3, 4)],
         ["B6", 2, V, (4, 4)]
         ], (2, 0))
    # ----------------------------
    # For the above board:
    # Search time = 0.6199999999999999
    # Num moves = 12
    
    intermediate_board_1 = make_init_state(
        [["B1", 2, H, (0, 0)],
         ["B2", 3, V, (1, 0)],
         ["B3", 2, V, (4, 0)],
         ["B4", 3, H, (3, 1)],
         ["B5", 3, V, (0, 3)], 
         ["B6", 3, V, (1, 4)],
         ["B7", 2, V, (0, 5)],
         ["B8", 2, V, (2, 5)],
         ["B9", 2, H, (4, 4)],
         ["B10", 2, H, (5, 4)]
         ], (2, 1))
    # ----------------------------
    # For the above board:
    # Search time = 2.39
    # Num moves = 9
    
    intermediate_board_2 = make_init_state(
        [["B1", 2, V, (0, 1)],
         ["B2", 2, H, (0, 2)],
         ["B3", 2, V, (1, 3)],
         ["B4", 2, H, (0, 4)],
         ["B5", 2, H, (1, 4)], 
         ["B6", 3, V, (3, 0)],
         ["B7", 3, H, (3, 1)],
         ["B8", 2, V, (4, 2)],
         ["B9", 3, V, (2, 4)],
         ["B10", 2, V, (2, 5)],
         ["B11", 2, V, (4, 5)],
         ], (2, 0))
    #----------------------------
    # For the above board:
    # Search time = 4.18
    # Num moves = 12
    
    advanced_board_1 = make_init_state(
        [["B1", 2, V, (0, 0)],
         ["B2", 3, H, (3, 0)],
         ["B3", 2, H, (5, 0)],
         ["B4", 2, V, (4, 2)],
         ["B5", 3, H, (0, 3)], 
         ["B6", 2, V, (1, 3)],
         ["B7", 2, V, (2, 4)],
         ["B8", 3, V, (1, 5)],
         ["B9", 2, H, (4, 4)],
         ["B10", 2, H, (5, 3)]
         ], (2, 0))
    #----------------------------
    # For the above board:
    # Search time = 6.46
    # Num moves = 9
    
    advanced_board_2 = make_init_state(
        [["B1", 2, H, (0, 0)],
         ["B2", 3, V, (1, 0)],
         ["B3", 2, V, (4, 0)],
         ["B4", 3, V, (1, 3)],
         ["B5", 3, H, (5, 2)], 
         ["B6", 3, V, (0, 5)],
         ["B7", 2, H, (4, 4)]
         ], (2, 1))
    # ----------------------------
    # For the above board:
    # Search time = 8.27
    # Num moves = 11
    
    expert_board_2 = make_init_state(
        [["B1", 2, V, (0, 0)],
         ["B2", 2, H, (0, 1)],
         ["B3", 3, V, (1, 2)],
         ["B4", 3, H, (5, 0)],
         ["B5", 3, V, (0, 5)], 
         ["B6", 3, H, (3, 3)],
         ["B7", 2, V, (4, 4)]
         ], (2, 0))
    # ----------------------------
    # For the above board:
    # Search time = 23.64
    # Num moves = 19

    expert_board_1 = make_init_state(
        [["B1", 2, H, (3, 0)],
         ["B2", 2, H, (4, 0)],
         ["B3", 2, H, (5, 0)],
         ["B4", 2, H, (1, 2)],
         ["B5", 2, V, (2, 2)], 
         ["B6", 2, V, (4, 2)],
         ["B7", 2, V, (2, 3)],
         ["B8", 2, H, (0, 3)],
         ["B9", 2, V, (1, 4)],
         ["B10", 3, V, (0, 5)],
         ["B11", 2, H, (3, 4)],
         ["B12", 3, H, (4, 3)],
         ["B13", 3, H, (5, 3)]
         ], (2, 0))
    #----------------------------
    # For the above board:
    # Search time = 49.94
    # Num moves = 15

    
    se = SearchEngine('astar', 'full')
    print("\n\n------TESTING BOARD 1: Beginner Board 1------")
    se.search(beginner_board_1, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 2: Beginner Board 2------")
    se.search(beginner_board_2, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 3: Intermediate Board 1------")
    se.search(intermediate_board_1, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 4: Intermediate Board 2------")
    se.search(intermediate_board_2, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 5: Advanced Board 1------")
    se.search(advanced_board_1, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 6: Advanced Board 2------")
    se.search(advanced_board_2, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 7: Expert Board 1------")
    se.search(expert_board_1, unblockme_goal_fn, heur_num_blocks_blocking)
    print("\n\n------TESTING BOARD 8: Expert Board 2------")
    se.search(expert_board_2, unblockme_goal_fn, heur_num_blocks_blocking)
    
    print("\n\n\nAll boards have been tested!")
# 
# UnblockMe STATESPACE
# 


from search import *
import copy
from random import randint

# CONSTANTS
BOARD_ROWS = 6
BOARD_COLUMNS = 6
TARGET_ROW = 2
TARGET_LENGTH = 2
TARGET_NAME = "target"
HORIZONTAL = "horizontal"
VERTICAL = "vertical"

##################################################################
# The search space class 'UnblockMe'                             #
# This class is a sub-class of 'StateSpace' (from Search.py)     #
##################################################################

class Block:
    ''' A class to represent the blocks in the Unblock Me board.'''

    def __init__(self, name, length, orientation, position):
        ''' Returns a new block with the given attributes.
            a) self.name = a string which is the name of the block
            b) self.length = an integer which number of squares the block 
               occupies
            c) self.orientation = either "horizontal" or "vertical"
            d) self.position = a tuple (x, y) where x and y are integers
               representing the row and column of the top left square of the 
               block.
        '''
        self.name = name
        self.length = length
        self.orientation = orientation
        self.position = position


class UnblockMe(StateSpace):
    '''
    action: str - the action that caused you to get to this state
        - "START" or
        - move (<block-name> <down/up/left/right> <num> spaces 
                        from <old-position> to <new-position>)
    gval: a number (integer) that is the cost of getting to this state. We 
        define this as the number of spaces a block was moved to get to this
        state.
    target_block: a Block object which represents the block that we are trying
        to unblock
    block_list: a list of Blocks which represent all the OTHER blocks on the
        board (excluding the target block).
    board: a 2-D list of Booleans which represents the current state of
        the board. self.board[i][j] == True iff there is some block occupying
        square [i][j] of the board. self.board[0] is the topmost row of the 
        board, and self.board[i][0] is the leftmost column. Our board has 6
        rows and 6 columns.
    parent: the unblockme state that brought us here
    '''
    def __init__(self, action, gval, target_block, block_list, board, parent=None):
        StateSpace.__init__(self, action, gval, parent)
        self.target_block = target_block
        self.block_list = block_list
        self.board = board

    def successors(self):
        '''Return list of UnblockMe objects that are the successors of the 
        current object

        Options:
        1) Move a vertical block UP
        2) Move a vertical block DOWN
        3) Move a horizontal block LEFT
        4) Move a horizontal block RIGHT
        5) Move the target block LEFT or RIGHT
        '''
        successors_list = []
        # Go through all the blocks in the block list
        for i in range(len(self.block_list)):
            # for each block, we add all valid movings of this block to the
            # successors list
            block = self.block_list[i]
            if block.orientation == VERTICAL:
                # check how much we can move it up and down               
                up, down = self.get_vertical_moves(block)
                # get the successor states which are the result of moving this
                # block up or down, and add them to the list of successors
                successors_list += self.vertical_successors(block, up, i) + \
                                   self.vertical_successors(block, down, i)
            else:
                # check how much we can move it left and right
                left, right = self.get_horizontal_moves(block)
                successors_list += self.horizontal_successors(block, left, i) + \
                                   self.horizontal_successors(block, right, i)
        # now check how much we can move the target block
        target_left, target_right = self.get_horizontal_moves(self.target_block)
        successors_list += self.horizontal_successors(self.target_block, target_left, None) + \
                           self.horizontal_successors(self.target_block, target_right, None)
        return successors_list

    def horizontal_successors(self, block, distance, block_index):
        '''Return a list of the successor states (UnblockMe objects) which are 
        the results of moving the given block left or right <distance> spaces.
        '''
        successors_list = []
        if distance != 0:
            # change the block
            new_block = almost_clone_block(block, (block.position[0], block.position[1] + distance))
            # change the list
            new_block_list = self.block_list
            new_target_block = self.target_block
            if block.name != TARGET_NAME:
                new_block_list = self.block_list[:block_index] + [new_block] + self.block_list[block_index+1:]
            else:
                new_target_block = new_block
            # change the board
            new_board = self.update_board(block, new_block.position)
            if distance < 0:
                dir = "left"
            else:
                dir = "right"
            action = "Move {} {} {} spaces from {} to {}".format(block.name, dir, abs(distance), block.position,
                                                                    new_block.position)
            successor = UnblockMe(action, self.gval + abs(distance), new_target_block, new_block_list, new_board, self)
            successors_list.append(successor)
        return successors_list

    def vertical_successors(self, block, distance, block_index):
        '''Return a list of the successor states (UnblockMe objects) which are 
        the results of moving the given block up or down <distance> spaces.
        '''
        successors_list = []
        if distance != 0:
            # change the block
            new_block = almost_clone_block(block, (block.position[0] + distance, block.position[1]))
            # change the list
            new_block_list = self.block_list[:block_index] + [new_block] + self.block_list[block_index+1:]
            # change the board
            new_board = self.update_board(block, new_block.position)
            if distance < 0:
                dir = "up"
            else:
                dir = "down"
            action = "Move {} {} {} spaces from {} to {}".format(block.name, dir, abs(distance), block.position,
                                                                    new_block.position)
            successor = UnblockMe(action, self.gval + abs(distance), self.target_block, new_block_list, new_board, self)
            successors_list.append(successor)
        return successors_list

    def get_vertical_moves(self, block):
        '''Return a tuple where the first item is the amount of free spaces 
        above the given block and the second item is the amount below.
        The amount of spaces above is stored as a negative number, to make
        it easier to add to the current position of a block later on.
        '''
        position = block.position
        up = 0
        down = 0
        row = position[0] - 1
        # check how far we can move up
        while row >= 0:
            if not self.board[row][position[1]]:
                up -= 1
                row -= 1
            else:
                break
        # check how far we can move down
        row = position[0] + block.length
        while row < 6:
            if not self.board[row][position[1]]:
                down += 1
                row += 1
            else:
                break
        return up, down

    def get_horizontal_moves(self, block):
        '''Return a tuple where the first item is the amount of free spaces 
        left of the given block and the second item is the amount to the right.
        The amount of spaces to the left is stored as a negative number, to 
        make it easier to add to the current position of a block later on.
        '''
        position = block.position
        left = 0
        right = 0
        column = position[1] - 1
        # check how far we can move left
        while column >= 0:
            if not self.board[position[0]][column]:
                left -= 1
                column -= 1
            else:
                break

        column = position[1] + block.length
        # check how far we can move right
        while column < 6:
            if not self.board[position[0]][column]:
                right += 1
                column += 1
            else:
                break
        return left, right

    def update_board(self, block, new_position):
        '''Return a copy of the game board where block has been moved to 
        new_position.
        '''
        new_board = copy.deepcopy(self.board)
        old_position = block.position
        if block.orientation == VERTICAL:
            for i in range(block.length):
                new_board[old_position[0] + i][old_position[1]] = False
            for i in range(block.length):
                new_board[new_position[0] + i][new_position[1]] = True
        else:
            for i in range(block.length):
                new_board[old_position[0]][old_position[1] + i] = False
            for i in range(block.length):
                new_board[new_position[0]][new_position[1] + i] = True
        return new_board

    def hashable_state(self):
        '''Return a tuple which is the list representation of the target_block 
        followed by the flattened block_list. This will be used as a dictionary
        key to UNIQUELY represent the state.
        '''
        sorted_blocks = sorted(self.get_blocks(), key=lambda block: block[0])
        flat_blocks = [x for sublist in sorted_blocks for x in sublist]
        return tuple(self.get_target_block() + flat_blocks)

    def get_blocks(self):
        '''Return list containing status of each block
           This list is in the format: [b_1, b_2, ..., b_n]
           with one status list for each block in the state. 
           Each block status item b_i is itself a list in the format: 
                [<name>, <length>, <orientation>, <position>]
           Where <name> is the name of the block (a string)
                 <length> is the number of squares the block occupies
                 <orientation> is either "horizontal" or "vertical"
                 <position> is a tuple (row, column)
        '''
        blocks = []
        for block in self.block_list:
            blocks.append([block.name, block.length, block.orientation, block.position])
        return blocks

    def get_target_block(self):
        '''Return the block status of the target block, which is a list in the 
        format: 
                [<name>, <length>, <orientation>, <position>]
           Where <name> is "target"
                 <length> is 2 (target block always has same length)
                 <orientation> is always "horizontal"
                 <position> is a tuple (row, column) where row is always 2
        '''
        target_block = self.target_block
        return [target_block.name, target_block.length, target_block.orientation, target_block.position]

    def print_state(self):
        '''Return a string representation of this state.'''
        if self.parent:
            print("Action= \"{}\", S{}, f-value = {}, g-value = {}, h-value = {}, (From S{})".format(self.action, self.index, self.gval + heur_num_blocks_blocking(self), self.gval, heur_num_blocks_blocking(self), self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

#############################################
# heuristics                                #
#############################################

def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_num_blocks_blocking(state):
    '''Return the heuristic value for this state. The heuristic value is 
    defined as (number of squares the target block is away from the right
    side of the board) + (number of moves to move the blocks blocking the 
    target block).
    '''
    if state.index == 6324:
        pass
    num_moves = 0
    # get the position of the square to the right of the target block
    target_column = state.target_block.position[1] + TARGET_LENGTH
    # find the number of blocks in front of the target block
    for block in state.block_list:
        # only vertical blocks can block the target block
        if block.orientation == VERTICAL:
            top = block.position[0]
            bottom = block.position[0] + block.length - 1
            # check if it's blocking
            if (top <= TARGET_ROW <= bottom) and block.position[1] >= target_column:
                # num_up is the number of squares we would have to move the
                # block UP to move it out of the way of the target block
                num_up = bottom - TARGET_ROW + 1
                # num_down is the number of squares we would have to move the
                # block DOWN to move it out of the way of the target block
                num_down = TARGET_ROW - top + 1
                if top < num_up:
                    # if there aren't enough squares above, we can't move it 
                    # up, we have to go down
                    num_moves += num_down
                elif (BOARD_ROWS - (bottom + 1)) < num_down:
                    # if there aren't enough squares below, we can't move it 
                    # down, we have to go up
                    num_moves += num_up
                else:
                    # if we can go either way, we want the minimum
                    num_moves += min(num_up, num_down)
    # add the distance from the target block to the goal
    num_moves += BOARD_COLUMNS - target_column
    return num_moves


def unblockme_goal_fn(state):
    '''Our goal state is defined as the target_block being at position (2, 4)
    which means there are no blocks blocking it, and it is at the edge of the
    board.'''
    return state.target_block.position == (TARGET_ROW, 4)


def make_init_state(block_list, target_block_pos):
#IMPLEMENT
    '''Input the following items which specify a state and return a warehouse 
    object representing this initial state.
            The state's its g-value is zero
            The state's parent is None
            The state's action is the dummy action "START"
        block_list = a list in the format: [b_1, b_2, ..., b_n]
           where each b_1 represents the status of a block on the board
           Each block status item b_i is itself a list in the format: 
                [<name>, <length>, <orientation>, <position>]
        target_block_pos = a tuple (x, y) which is the row and column of the
           top_left square of the target_block (the block that needs to be 
           unblocked.)
        In our implementation, we assume target_block is always in row 2.
    '''
    # create the blocks
    blocks = []
    for block in block_list:
        blocks.append(Block(block[0], block[1], block[2], block[3]))
    # create the target block
    target_block = Block(TARGET_NAME, TARGET_LENGTH, HORIZONTAL, target_block_pos)
    board = [[False for x in range(6)] for y in range(6)]
    # fill in the board
    for block in blocks:
        for i in range(block.length):
            if block.orientation == VERTICAL:
                board[block.position[0] + i][block.position[1]] = True
            else:
                board[block.position[0]][block.position[1] + i] = True
    for i in range(target_block.length):
        board[target_block.position[0]][target_block.position[1] + i] = True
    return UnblockMe("START", 0, target_block, blocks, board)

########################################################
# Helper functionS                        #
########################################################

def almost_clone_block(block, new_position):
    '''Return a new block with the same attributes as block, but at the
    new_position.'''
    return Block(block.name, block.length, block.orientation, new_position)
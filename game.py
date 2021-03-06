import random
import copy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        count = 0
        for r in state:
            count += r.count('b') + r.count('r')
        if(count < 8):
            drop_phase = True   # detect drop phase
        else:
            drop_phase = False  # detect drop phase
        move = []
        if not drop_phase:
            successor_list = self.succ_move(state, self.my_piece)
            random.shuffle(successor_list)
            alpha_val= -999999
            next_move = [(0,0),(0,0)]
            for successor in successor_list:
                ts = copy.deepcopy(state)
                ts[successor[0][0]][successor[0][1]] = self.my_piece
                ts[successor[1][0]][successor[1][1]] = ' '
                successor_val = self.Min_Value(ts, 0, drop_phase)
                if(alpha_val < successor_val):
                    next_move = successor
                    alpha_val = successor_val
            move = next_move
            return move
        
        if drop_phase:
            ts = copy.deepcopy(state)
            successor_list = self.succ(state)
            random.shuffle(successor_list)
            alpha_val= -999999
            next_move = (0,0)
            for successor in successor_list:
                row = successor[0]
                col = successor[1]
                ts[row][col] = self.my_piece
                successor_val = self.Min_Value(ts, 0, drop_phase)
                if(alpha_val <= successor_val):
                    next_move = (row,col)
                    alpha_val = successor_val
            move.insert(0, next_move)
            return move
        
    def Min_Value(self, state, depth, drop):
        alpha_val = 0
        beta_val = 0
        ts = copy.deepcopy(state)
        if(self.game_value(state) != 0):
            return self.game_value(state)
        if(depth  >= 1):
            return self.heuristic_game_value(state,self.opp)
        if(drop ):
            successor_list = self.succ(state)
            random.shuffle(successor_list)
            for row,col in successor_list:
                ts[row][col] = self.opp
                if beta_val < self.Max_Value(ts,depth+1,drop):
                    beta_val = beta_val
                elif beta_val > self.Max_Value(ts,depth+1,drop):
                    beta_val = self.Max_Value(ts,depth+1,drop)
        else:
            successor_list = self.succ_move(state,self.opp)
            random.shuffle(successor_list)
            for succ in successor_list:
                ts[succ[0][0]][succ[0][1]] = self.opp
                ts[succ[1][0]][succ[1][1]] = ' '
                if beta_val < self.Max_Value(ts,depth+1,drop):
                    beta_val = beta_val
                elif beta_val > self.Max_Value(ts,depth+1,drop):
                    beta_val = self.Max_Value(ts,depth+1,drop)
        return beta_val

    def Max_Value(self, state, depth, drop):
        alpha_val = 0
        beta_val = 0
        ts = copy.deepcopy(state)
        if(self.game_value(state) != 0):
            return self.game_value(state)
        if(depth  >= 1):
            return self.heuristic_game_value(state)
        if(drop):
            successor_list = self.succ(state)
            random.shuffle(successor_list)
            for row,col in successor_list:
                ts[row][col] = self.my_piece
                if alpha_val > self.Min_Value(ts,depth+1, drop):
                    alpha_val = alpha_val
                elif alpha_val < self.Min_Value(ts,depth+1, drop):
                    alpha_val = self.Min_Value(ts,depth+1, drop)
        else:
            successor_list = self.succ_move(state, self.my_piece)
            random.shuffle(successor_list)            
            for succ in successor_list:
                ts[succ[0][0]][succ[0][1]] = self.my_piece
                ts[succ[1][0]][succ[1][1]] = ' '
                if alpha_val > self.Min_Value(ts,depth+1, drop):
                    alpha_val = alpha_val
                elif alpha_val < self.Min_Value(ts,depth+1, drop):
                    alpha_val = self.Min_Value(ts,depth+1, drop)
        return alpha_val
    
    def succ(self, state): 
        size = len(state)
        succ = []
        for row in range(size):
            for col in range(size):
                if(state[row][col] == ' '):
                    succ.append((row,col))
        return succ
        
    def succ_move(self, state, piece):
        size = len(state)
        moves = [-1,0,1]
        succ = []
        for row in range(size):
            for col in range(size):
                if(state[row][col] == piece):
                    for r in moves:
                        for c in moves:
                            if (row + r < size) and (row + r >=0) and (col + c < size) and (col + c >=0) and state[row+r][col+c] == ' ':
                                succ.append( [(row + r, col + c),(row,col)] )
        return succ
        

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
    
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
    
       
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.
        
        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        
        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
            
        # check / diagonal wins
        for row in range(2):
            for col in range(3,5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col]==self.my_piece else -1

        # check 3x3 square corners wins
        for row in range(1,4):
            for col in range(1,4):
                if state[row][col] == ' ' and state[row+1][col] != ' ' and state[row+1][col] == state[row-1][col] == state[row][col-1] == state[row][col+1]:
                    return 1 if state[row][col+1]==self.my_piece else -1
        
        return 0 # no winner yet    
    
    def heuristic_game_value(self, state):
        length = len(state)
        val = self.game_value(state)
        if(val != 0):
            return val
        max_val = -2
        min_val = 2
        for row in state:
            for col in range(2):
                temp = []
                for i in range(4):
                    temp.append(row[col+i])
                
                if max_val > temp.count(self.my_piece)*0.15:    #Range value has to be between 1 and -1
                    max_val = max_val
                elif max_val < temp.count(self.my_piece)*0.15:    #Range value has to be between 1 and -1
                    max_val = temp.count(self.my_piece)*0.15
                
                if min_val < temp.count(self.opp)*(-1)*0.15:    #Range value has to be between 1 and -1
                    min_val = min_val
                elif min_val > temp.count(self.opp)*(-1)*0.15:    #Range value has to be between 1 and -1
                    min_val = temp.count(self.opp)*(-1)*0.15
                

        for col in range(length):
            for row in range(2):
                temp = []
                for i in range(4):
                    temp.append(state[row+i][col])

                if max_val > temp.count(self.my_piece)*0.15:
                    max_val = max_val
                elif max_val < temp.count(self.my_piece)*0.15:
                    max_val = temp.count(self.my_piece)*0.15
                
                if min_val < temp.count(self.opp)*(-1)*0.15:
                    min_val = min_val
                elif min_val > temp.count(self.opp)*(-1)*0.15:
                    min_val = temp.count(self.opp)*(-1)*0.15


        for row in range(2):
            for col in range(2):
                temp = []
                for i in range(4):
                    if(col+i < length and row+i < length):
                        temp.append(state[row+i][col+i])

                if max_val > temp.count(self.my_piece)*0.15:
                    max_val = max_val
                elif max_val < temp.count(self.my_piece)*0.15:
                    max_val = temp.count(self.my_piece)*0.15
                
                if min_val < temp.count(self.opp)*(-1)*0.15:
                    min_val = min_val
                elif min_val > temp.count(self.opp)*(-1)*0.15:
                    min_val = temp.count(self.opp)*(-1)*0.15
            

        for row in range(2):
            for col in range(3,length):
                temp = []
                for i in range(4):
                    if(col-i >= 0 and row+i < length):
                        temp.append(state[row+i][col-i])

                if max_val > temp.count(self.my_piece)*0.15:
                    max_val = max_val
                elif max_val < temp.count(self.my_piece)*0.15:
                    max_val = temp.count(self.my_piece)*0.15
                
                if min_val < temp.count(self.opp)*(-1)*0.15:
                    min_val = min_val
                elif min_val > temp.count(self.opp)*(-1)*0.15:
                    min_val = temp.count(self.opp)*(-1)*0.15
                

        for row in range(1,4):
            for col in  range(1,4):
                temp = []
                temp.append(state[row+1][col])
                temp.append(state[row][col+1])
                temp.append(state[row-1][col])
                temp.append(state[row][col-1])
                
                if max_val > temp.count(self.my_piece)*0.15:
                    max_val = max_val
                elif max_val < temp.count(self.my_piece)*0.15:
                    max_val = temp.count(self.my_piece)*0.15
                
                if min_val < temp.count(self.opp)*(-1)*0.15:
                    min_val = min_val
                elif min_val > temp.count(self.opp)*(-1)*0.15:
                    min_val = temp.count(self.opp)*(-1)*0.15
        return max_val+min_val   
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    while piece_count < 8 and ai.game_value(ai.board) == 0:

        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            print(move)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        piece_count += 1
        turn += 1
        turn %= 2

    while ai.game_value(ai.board) == 0:
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(move)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "_main_":
    main()
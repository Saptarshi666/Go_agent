from copy import deepcopy
import numpy as np
import random

def find_died_pieces(Matrix_for_opponent, piece_type):
        '''
        Find the died stones that has no liberty in the board for a given piece type.

        :param piece_type: 1('X') or 2('O').
        :return: a list containing the dead pieces row and column(row, column).
        '''
        board = Matrix_for_opponent
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not find_liberty(i, j,board):
                        died_pieces.append((i,j))
        return died_pieces
def detect_neighbor( i, j,Matrix_for_opponent):
        '''
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        '''
        board = Matrix_for_opponent
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors
def detect_neighbor_ally( i, j, Matrix_for_opponent):
        '''
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        '''
        board = Matrix_for_opponent
        neighbors = detect_neighbor(i, j, Matrix_for_opponent)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies
def ally_dfs(i,j,Matrix_for_opponent):
    stack = [(i, j)]  # stack for DFS serach
    ally_members = []  # record allies positions during the search
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = detect_neighbor_ally(piece[0], piece[1],Matrix_for_opponent)
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members
def find_liberty(i,j,Matrix_for_opponent):
     board = Matrix_for_opponent
     ally_members = ally_dfs(i, j,Matrix_for_opponent)
     for member in ally_members:
        neighbors = detect_neighbor(member[0], member[1], Matrix_for_opponent)
        for piece in neighbors:
                # If there is empty space around a piece, it has liberty
            if board[piece[0]][piece[1]] == 0:
                return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
     return False
               
def positions_according_to_rule1(Matrix_for_opponent,what_player_I_am):
    i = 0
    valid_positions = []
    while i < 5:
         j = 0
         while j < 5:
              if Matrix_for_opponent[i][j] == 0:
                   #check if stone is placed over here than if it still has liberty 
                   Matrix_for_opponent[i][j] = what_player_I_am
                   valid_place = find_liberty(i,j,Matrix_for_opponent)
                   if valid_place == True:
                        valid_positions.append([i,j])
                   else:
                        #.....do something ekse
                        opponent_number = -1
                        if what_player_I_am == 1:
                             opponent_number = 2
                        else:
                             opponent_number = 1
                        killed_stones = find_died_pieces(Matrix_for_opponent,opponent_number)
                        if len(killed_stones) != 0:
                             valid_positions.append([i,j])
                   Matrix_for_opponent[i][j] = 0
              j = j + 1
         i = i + 1   
    return valid_positions
def remove_certain_pieces(Matrix_for_opponent, positions):
        '''
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        '''
        board = Matrix_for_opponent
        for piece in positions:
            board[piece[0]][piece[1]] = 0
def remove_died_pieces(Matrix_for_opponent, piece_type):
        '''
        Remove the dead stones in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        '''

        died_pieces = find_died_pieces(Matrix_for_opponent,piece_type)
        if not died_pieces: return []
        remove_certain_pieces(Matrix_for_opponent,died_pieces)
        return died_pieces  
def compare_board(board1, board2):
        for i in range(5):
            for j in range(5):
                if board1[i][j] != board2[i][j]:
                    return False
        return True       
def positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am):
     for position in valid_positions:
        Matrix_for_opponent_test = deepcopy(Matrix_for_opponent)
        opponent = -1
        if what_player_I_am == 1:
            opponent = 2
        else:
            opponent = 1
        Matrix_for_opponent_test[position[0]][position[1]] = what_player_I_am
        killed_stones = remove_died_pieces(Matrix_for_opponent_test,opponent)
        if  compare_board(Matrix_for_opponent_test,Matrix_for_me):
            valid_positions.remove(position)   
     return valid_positions   
def countliberty(Matrix_for_opponent_test,what_player_I_am):
     num = 0 
     i = 0
     while i <  5:
          j = 0 
          while j < 5:
               if Matrix_for_opponent_test[i][j] == what_player_I_am:
                    if i == 0 :
                         if j == 0 :
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
                         if j == 4 :
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
                         else:
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                    elif i == 4:
                         if j == 0 :
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                         if j == 4 :
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                         else:
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                    else:
                         if j == 0:
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                         elif j == 4:
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                         else:
                              if Matrix_for_opponent_test[i][j+1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i][j-1] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i-1][j] == 0:
                                   num = num + 1
                              if Matrix_for_opponent_test[i+1][j] == 0:
                                   num = num + 1
               j = j + 1
          i = i + 1
     return num
def eulernum(Matrix_for_opponent_test,what_player_I_am):
     test = np.array(Matrix_for_opponent_test)
     # Array to be added as row
     row_to_be_added = np.array([0, 0, 0, 0, 0])
     #last row
     row_n = test.shape[0] 
     new_matrix = np.insert(test,row_n,[row_to_be_added],axis= 0)
     new_matrix = np.insert(new_matrix,0,[row_to_be_added],axis= 0)  
     column_to_be_added = np.array([0,0, 0,0,0,0,0]) 
     # Adding column to array using append() method
     new_matrix = np.insert(new_matrix, 0, column_to_be_added, axis=1)
     column_n = new_matrix.shape[1]
     new_matrix = np.insert(new_matrix,column_n,column_to_be_added, axis = 1)
     opponent = -1
     if what_player_I_am == 1:
          opponent = 2
     else:
          opponent = 1
     new_matrix[new_matrix == opponent] = 0
     Q1 = 0
     Q3 = 0
     Qd = 0
     window = [[0 for i in range(2) ] for j in range(2)]
     i = 0
     j = 0 
     while i < 6:
          j = 0
          while j < 6:
               window[0][0] = new_matrix[i][j]
               window[0][1] = new_matrix[i][j+1]
               window[1][0] = new_matrix[i+1][j]
               window[1][1] = new_matrix[i+1][j+1]
               if window == [[0,what_player_I_am],[0,0]] or window == [[what_player_I_am,0],[0,0]] or window == [[0,0],[what_player_I_am,0]] or window == [[0,0],[0,what_player_I_am]]:
                    Q1 +=1
               elif window == [[what_player_I_am,what_player_I_am],[0,what_player_I_am]] or window == [[0,what_player_I_am],[what_player_I_am,what_player_I_am]] or window ==  [[what_player_I_am,0],[what_player_I_am,what_player_I_am]] or window == [[what_player_I_am,what_player_I_am],[what_player_I_am,0]]:
                    Q3+=1
               elif window == [[what_player_I_am,0],[0,what_player_I_am]] or window == [[0,what_player_I_am],[what_player_I_am,0]]:
                    Qd+=1
               j+=1
          i+= 1
     E = (Q1 - Q3 + (2*Qd))/4
     return E
     

def eval_function(Matrix_for_opponent,valid_positions,what_player_I_am,total_moves):
     eval = [-1]* len(valid_positions)
     i = 0
     eval_value_p = 0
     eval_value_o = 0
     if what_player_I_am == 1:
          opponent = 2
     else:
          opponent = 1
     for position in valid_positions:
          
          Matrix_for_opponent_test = deepcopy(Matrix_for_opponent)
          #Matrix_for_opponent_test_o = deepcopy(Matrix_for_opponent)
          Matrix_for_opponent_test[position[0]][position[1]] = what_player_I_am
          #Matrix_for_opponent_test_o[position[0]][position[1]] = opponent
          #deadpieces = remove_died_pieces(Matrix_for_opponent_test,what_player_I_am)
          deadpieces_o = remove_died_pieces(Matrix_for_opponent_test,opponent)
          deadpieces_p = remove_died_pieces(Matrix_for_opponent_test,what_player_I_am) 
          total_pieces_p = 0
          if what_player_I_am == 1:
               total_pieces_p = blackpieces(Matrix_for_opponent_test)
               total_pieces_o = whitepieces(Matrix_for_opponent_test)
          else:
               total_pieces_p = whitepieces(Matrix_for_opponent_test)
               total_pieces_o = blackpieces(Matrix_for_opponent_test)
          diff_in_pieces = total_pieces_p - total_pieces_o        
          total_liberty_of_my_pieces_p = countliberty(Matrix_for_opponent_test,what_player_I_am)
          total_liberty_of_my_pieces_o = countliberty(Matrix_for_opponent_test,opponent)
          diff_in_liberty = total_liberty_of_my_pieces_p - total_liberty_of_my_pieces_o  
          #this is to make connecting stones and eyes
          eNum = eulernum(Matrix_for_opponent_test,what_player_I_am)
          eNum1 = eulernum(Matrix_for_opponent_test,opponent)
          diff_in_euler_num = eNum1 - eNum  
          eval[i] = (1.06*diff_in_pieces) + (1.1*len(deadpieces_o))+ (1.04*diff_in_liberty) + (1.06*diff_in_euler_num) + 1.16
          i = i + 1
     return eval


  
      
def blackpieces(Matrix_for_opponent):
     num = 0
     i = 0
     while i < 5:
          j = 0
          while j < 5:
               if Matrix_for_opponent[i][j] == 1:
                    num = num + 1
               j = j + 1
          i = i + 1
     return num 
def whitepieces(Matrix_for_opponent):
     num = 0
     i = 0
     while i < 5:
          j = 0
          while j < 5:
               if Matrix_for_opponent[i][j] == 2:
                    num = num + 1
               j = j + 1
          i = i + 1
     return num
def minmax(Matrix_for_opponent,Matrix_for_me, what_player_I_am,depth,total_moves,max_player):
     #check if we have reached the end of the game
     if depth == 1:
        valid_positions = positions_according_to_rule1(Matrix_for_opponent,what_player_I_am)
        valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am)
        if len(valid_positions) == 0:
             return "PASS", 0
        eval_values = eval_function(Matrix_for_opponent,valid_positions,what_player_I_am,total_moves)
        max_eval_value = max(eval_values)
        if max_eval_value <= 0:
             'PASS',0
        max_eval_index = eval_values.index(max_eval_value)
        max_eval_action = valid_positions[max_eval_index]
        return max_eval_action,max_eval_value
     else:
          if max_player:
               value = - np.inf
               valid_positions = positions_according_to_rule1(Matrix_for_opponent,what_player_I_am)
               valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am)
               if len(valid_positions) == 0:
                    return "PASS", 0
               best_action = ''
               opponent = -4
               if what_player_I_am == 1:
                    opponent = 2
               else:
                    opponent =1 
               for position in valid_positions:
                    Matrix_for_test = deepcopy(Matrix_for_opponent)
                    Matrix_for_test[position[0]][position[1]] = what_player_I_am
                    dead_peice = remove_died_pieces(Matrix_for_test,opponent)
                    action,best_value = minmax(Matrix_for_test,Matrix_for_opponent,what_player_I_am,depth-1,total_moves+1,False)
                    if best_value > value:
                         value = best_value
                         best_action = position
               #alpha beta goes here
               return best_action,value
          else:
               value = np.inf
               oponent = -1
               if what_player_I_am == 1:
                    opponent = 2
               else:
                    opponent =1 
               valid_positions = positions_according_to_rule1(Matrix_for_opponent,opponent)
               valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,opponent)
               if len(valid_positions) == 0:
                    return "PASS", 0
               best_action = ''
               for position in valid_positions:
                    Matrix_for_test = deepcopy(Matrix_for_opponent)
                    Matrix_for_test[position[0]][position[1]] = opponent
                    dead_peice = remove_died_pieces(Matrix_for_test,what_player_I_am)
                    action,best_value = minmax(Matrix_for_test,Matrix_for_opponent,what_player_I_am,depth-1,total_moves+1,True)
                    if best_value < value:
                         value = best_value
                         best_action = position
                    #put 
               return best_action,value

def alphabeta(Matrix_for_opponent,Matrix_for_me,what_player_I_am, depth,total_moves,alpha,beta,max_player,valid_positions,startingdepth):  
     Dict = {}
     if depth == 1:
        valid_positions = positions_according_to_rule1(Matrix_for_opponent,what_player_I_am)
        valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am)
        if len(valid_positions) == 0:
             return "PASS", 0
        eval_values = eval_function(Matrix_for_opponent,valid_positions,what_player_I_am,total_moves)
        max_eval_value = max(eval_values)
        if max_eval_value <= 0:
             'PASS',0
        max_eval_index = eval_values.index(max_eval_value)
        max_eval_action = valid_positions[max_eval_index]
        return max_eval_action,max_eval_value
     else:
          if max_player:
               value = - np.inf
               if depth != startingdepth:
                    valid_positions = positions_according_to_rule1(Matrix_for_opponent,what_player_I_am)
                    valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am)
               if len(valid_positions) == 0:
                    return "PASS", 0
               best_action = ''
               opponent = -4
               if what_player_I_am == 1:
                    opponent = 2
               else:
                    opponent =1 
               for position in valid_positions:
                    Matrix_for_test = deepcopy(Matrix_for_opponent)
                    Matrix_for_test[position[0]][position[1]] = what_player_I_am
                    dead_peice = remove_died_pieces(Matrix_for_test,opponent)
                    action,best_value = alphabeta(Matrix_for_test,Matrix_for_opponent,what_player_I_am,depth-1,total_moves+1,alpha,beta,False,valid_positions,startingdepth)
                    if depth == startingdepth:
                         if what_player_I_am == 1:
                              if position == [0,0] or position == [4,0] or position == [0,4] or position == [4,4]:
                                   best_value = best_value - 1.5
                              elif position[0] == 0 or position[0] == 4 or position[1] == 0 or position[1] == 4:
                                   best_value = best_value - 0.5

                    if best_value > value:
                         value = best_value
                         best_action = position
                    if value >alpha:
                         alpha = value     
                    if value >= beta:
                         break
               #alpha beta goes here
               return best_action,value
          else:
               value = np.inf
               oponent = -1
               if what_player_I_am == 1:
                    opponent = 2
               else:
                    opponent =1 
               valid_positions = positions_according_to_rule1(Matrix_for_opponent,opponent)
               valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,opponent)
               if len(valid_positions) == 0:
                    return "PASS", 0
               best_action = ''
               for position in valid_positions:
                    Matrix_for_test = deepcopy(Matrix_for_opponent)
                    Matrix_for_test[position[0]][position[1]] = opponent
                    dead_peice = remove_died_pieces(Matrix_for_test,what_player_I_am)
                    action,best_value = alphabeta(Matrix_for_test,Matrix_for_opponent,what_player_I_am,depth-1,total_moves+1,alpha,beta,True, valid_positions,startingdepth)
                    if best_value < value:
                         value = best_value
                         best_action = position
                    if value < beta:
                         beta = value
                    if value <=  alpha:
                         break
                    #put 
               return best_action,value

                    
                    
               
          
          
          
                              
def main():
    f = open("input.txt","r")
    num = int(f.readline())
    what_player_I_am = num
    Matrix_for_opponent = [[0 for i in range(5) ] for j in range(5)]
    mystones = []
    Matrix_for_me = [[0 for i in range(5) ] for j in range(5)]
    for i in range(len(Matrix_for_me)):
        line = f.readline()
        value = [*line]
        Matrix_for_me[i][0] = int(value[0])
        Matrix_for_me[i][1] = int(value[1])
        Matrix_for_me[i][2] = int(value[2])
        Matrix_for_me[i][3] = int(value[3])
        Matrix_for_me[i][4] = int(value[4])
    for i in range(len(Matrix_for_opponent)):
        line = f.readline()
        value = [*line]
        Matrix_for_opponent[i][0] = int(value[0])
        if (Matrix_for_opponent[i][0] == what_player_I_am):
             mystones.append([i,0])
        Matrix_for_opponent[i][1] = int(value[1])
        if (Matrix_for_opponent[i][1] == what_player_I_am):
             mystones.append([i,1])
        Matrix_for_opponent[i][2] = int(value[2])
        if (Matrix_for_opponent[i][2] == what_player_I_am):
             mystones.append([i,2])
        Matrix_for_opponent[i][3] = int(value[3])
        if (Matrix_for_opponent[i][3] == what_player_I_am):
             mystones.append([i,3])
        Matrix_for_opponent[i][4] = int(value[4])
        if (Matrix_for_opponent[i][4] == what_player_I_am):
             mystones.append([i,4])
    f.close()
    check = not np.any(Matrix_for_me)
    if check == True:
         total_moves = 0
    else: 
     f = open("num_of_moves.txt","r")
     total_moves = int(f.readline())
     f.close()
    if total_moves == 0 and what_player_I_am == 1:
        f = open("output.txt","w")
        sente = ""
        move = [2,2]
        sente = sente + str(move[0])+','+ str(move[1])+ '\n'
        total_moves += 1
        f.write(sente)
        f.close()
        f = open("num_of_moves.txt","w")
        total_moves_str = str(total_moves)
        f.write(total_moves_str)
        f.close()
        return
    if total_moves <= 4 and what_player_I_am == 1 :
          i = 1
          ally_mem = ''
          while i <= 3:
               j = 1
               while j <= 3:
                    if Matrix_for_opponent[i][j] == 1:
                         ally_mem = ally_dfs(i,j,Matrix_for_opponent)
                         break
                    j +=1
               i+=1
          for allies in ally_mem:
               neigh = detect_neighbor(allies[0],allies[1],Matrix_for_opponent)
               for neighbor in neigh:
                    if neighbor[0] >=1 and neighbor[0] <=3:
                         if neighbor[1] >=1 and neighbor[1] <=3:
                              if Matrix_for_opponent[neighbor[0]][neighbor[1]] == 0:
                                    f = open("output.txt","w")
                                    sente = ""
                                    move = neighbor
                                    sente = sente + str(move[0])+','+ str(move[1])+ '\n'
                                    total_moves += 1
                                    f.write(sente)
                                    f.close()
                                    f = open("num_of_moves.txt","w")
                                    total_moves_str = str(total_moves)
                                    f.write(total_moves_str)
                                    f.close()
                                    return
          for allies in ally_mem:
               neigh = detect_neighbor(allies[0],allies[1],Matrix_for_opponent)
               for neighbor in neigh:
                    if neighbor != [0,0] and neighbor !=[0,4] and neighbor != [4,0] and neighbor != [4,4]:
                              if Matrix_for_opponent[neighbor[0]][neighbor[1]] == 0:
                                    f = open("output.txt","w")
                                    sente = ""
                                    move = neighbor
                                    sente = sente + str(move[0])+','+ str(move[1])+ '\n'
                                    total_moves += 1
                                    f.write(sente)
                                    f.close()
                                    f = open("num_of_moves.txt","w")
                                    total_moves_str = str(total_moves)
                                    f.write(total_moves_str)
                                    f.close()
                                    return
          


                       
    #what if this is the first play of the game
         #satrt with variable initialization
         #all my stones are numbered from left to right , top to bottom     
         #liberty rule
       
         #ko rule
         
     #start with min-max or alpha-beta pruning
    valid_positions = positions_according_to_rule1(Matrix_for_opponent,what_player_I_am)
    valid_positions = positions_according_to_rule2(Matrix_for_opponent,Matrix_for_me,valid_positions,what_player_I_am)
    opponent = 3- what_player_I_am
    Dict = {}
    for position in valid_positions:
          Matrix_for_test = deepcopy(Matrix_for_opponent)
          Matrix_for_test[position[0]][position[1]] = what_player_I_am
          dead_peice = remove_died_pieces(Matrix_for_test,opponent)
          if len(dead_peice) > 0:
               Dict[tuple(position)] = len(dead_peice)
    if len(Dict) > 0: 
          move = max(Dict, key=Dict.get)
          f = open("output.txt","w")
          sente = ""
          sente = sente + str(move[0])+','+ str(move[1])+ '\n'
          total_moves += 1
          f.write(sente)
          f.close()
          f = open("num_of_moves.txt","w")
          total_moves_str = str(total_moves)
          f.write(total_moves_str)
          f.close()
          return
    if what_player_I_am == 1:
          i = 1
          ally_mem = ''
          flag = 0
          while i <= 3:
               j = 1
               while j <= 3:
                    if Matrix_for_opponent[i][j] == 1:
                         ally_mem = ally_dfs(i,j,Matrix_for_opponent)
                         flag =1
                         break
                    j +=1
               if flag == 1:
                    break
               i+=1
          for allies in ally_mem:
               neigh = detect_neighbor(allies[0],allies[1],Matrix_for_opponent)
               for neighbor in neigh:
                    if neighbor[0] >=1 and neighbor[0] <=3:
                         if neighbor[1] >=1 and neighbor[1] <=3:
                              if Matrix_for_opponent[neighbor[0]][neighbor[1]] == 0:
                                    f = open("output.txt","w")
                                    sente = ""
                                    move = neighbor
                                    sente = sente + str(move[0])+','+ str(move[1])+ '\n'
                                    total_moves += 1
                                    f.write(sente)
                                    f.close()
                                    f = open("num_of_moves.txt","w")
                                    total_moves_str = str(total_moves)
                                    f.write(total_moves_str)
                                    f.close()
                                    return
          for allies in ally_mem:
               neigh = detect_neighbor(allies[0],allies[1],Matrix_for_opponent)
               for neighbor in neigh:
                    if neighbor != [0,0] and neighbor !=[0,4] and neighbor != [4,0] and neighbor != [4,4]:
                              if Matrix_for_opponent[neighbor[0]][neighbor[1]] == 0:
                                    f = open("output.txt","w")
                                    sente = ""
                                    move = neighbor
                                    sente = sente + str(move[0])+','+ str(move[1])+ '\n'
                                    total_moves += 1
                                    f.write(sente)
                                    f.close()
                                    f = open("num_of_moves.txt","w")
                                    total_moves_str = str(total_moves)
                                    f.write(total_moves_str)
                                    f.close()
                                    return
         
        
   
    if total_moves<12:
        depth = 3
    else:
        depth = 5
    alpha = -np.inf
    beta = np.inf
    startingdepth = depth
    move,value = alphabeta(Matrix_for_opponent,Matrix_for_me,what_player_I_am, depth,total_moves,alpha,beta,True,valid_positions,startingdepth)
    f = open("output.txt","w")
    sente = ""
    if move == 'PASS':
          sente = sente + move + '\n'
          total_moves += 1
    else:
          sente = sente + str(move[0])+','+ str(move[1])+ '\n'
          total_moves += 1
    f.write(sente)
    f.close()
    f = open("num_of_moves.txt","w")
    total_moves_str = str(total_moves)
    f.write(total_moves_str)
    f.close()

         
    
if __name__ == "__main__":  
        main()
from kalah import reverse_board
from runner import Player, Mercy
import copy


class User(Player):
    def __init__(self):
        super().__init__()
        self.mercy = Mercy()
        '''
        Check Player class in runner.py to get information about useful predefined functions
        e.g. move, get_score, is_empty, step
        '''

    class Node:
        def __init__(self, board, f, path, terminate):
            self.board = board
            self.f = f
            self.path = path
            self.terminate = terminate

        def setboard(self, board):
            self.board = board

        def set_f_value(self, f):
            self.f = f

        def setpath(self, path):
            self.path = path

        def setterminate(self, terminate):
            self.terminate = terminate

        def getboard(self):
            return self.board

        def get_f_value(self):
            return self.f

        def getpath(self):
            return self.path

        def gettermiate(self):
            return self.terminate

    def search(self, board, step=1):
        '''
        board: board information before move
        step: # of steps after move
        '''
        finallist = []
        all_step_list=[]
        for i in range(6):
            if board[i]==0:
                continue
            path=[]
            first_step_board,gameover=self.move(i,board)
            first_step_f = self.g(step, first_step_board) + self.h(first_step_board)
            path.append(i)
            node = self.Node(first_step_board, first_step_f, path, gameover)
            if gameover == False:
                all_step_list.append(node)
            else:
                finallist.append(node)


        step +=1

        for nodetemp in all_step_list:
            sec_step_positon=self.mercy.response(nodetemp.path[0])
            sec_step_board,gameover=self.move(sec_step_positon,nodetemp.board,False)
            sec_step_f = self.g(step, sec_step_board) + self.h(sec_step_board)
            nodetemp.terminate = gameover
            if gameover==False:
                nodetemp.board=sec_step_board
                nodetemp.f = sec_step_f
                nodetemp.path.append(sec_step_positon)

            else:
                sec_step_terminate_board=sec_step_board
                sec_step_terminate_f=sec_step_f
                nodetemp.path.append(i)
                sec_step_terminate_path=nodetemp.path
                sec_step_terminate_terminate=gameover
                sec_step_terminate_node=self.Node(sec_step_terminate_board,sec_step_terminate_f,sec_step_terminate_path,sec_step_terminate_terminate)
                finallist.append(sec_step_terminate_node)
        step +=1


        for nodetemp in all_step_list:
            if nodetemp.terminate == False:
                for i in range(6):
                    copypath = copy.deepcopy(nodetemp.path)
                    if nodetemp.board[i]==0:
                        continue
                    third_step_board, gameover = self.move(i,nodetemp.board)

                    third_step_f=self.g(step,third_step_board)+self.h(third_step_board)
                    final_f=third_step_f
                    copypath.append(i)
                    final_path=copypath
                    final_terminate=gameover
                    final_node=self.Node(third_step_board,final_f,final_path,final_terminate)
                    finallist.append(final_node)



        min=finallist[0].f
        for nodetemp in finallist:
            if nodetemp.f < min:
                min=nodetemp.f

        nodelist=[]
        for nodetemp in finallist:
            if nodetemp.f==min:
                nodelist.append(nodetemp)

        minindex=nodelist[0].path[0]
        for nodetemp in nodelist:
            if nodetemp.path[0] <minindex:
                minindex=nodetemp.path[0]

        return minindex

            

    def g(self, step, board):
        '''
        cost function
        '''
        return step - self.get_score(board) + self.get_score(board, is_mine=False)
    
    def h(self, board): #Not implemented!
        '''
        heuristic function
        v1: h1
        v2: h1 + h21 + h22
        '''
        return  self.h1(board)+self.h21(board)+self.h22(board)

        
    def h1(self, board):
        '''
        (# of pieces in holes in oppo’s side) - (# of pieces in holes in user side)
        '''
        sum_oppo=0
        for i in range(7,13):
            sum_oppo = sum_oppo + board[i]
        sum_user=0
        for i in range(0,6):
            sum_user = sum_user + board[i]
        return sum_oppo - sum_user

    def board_move(self,board,position,player=True):
        newboard=copy.deepcopy(board)
        assert position >= 0 and position < 6
        if player:
            score_idx = 6
        else:
            position += 7
            score_idx = -1
        move_cnt = copy.deepcopy(newboard[position])
        assert move_cnt > 0


        take_opponents = []
        pos = position
        last_position = pos
        for i in range(1, move_cnt + 1):
            if player and pos + i == len(newboard) - 1:
                pos = -i
            elif not player and pos + i == len(newboard):
                pos = -i
            elif not player and pos + i == 6:
                pos += 1
            newboard[pos + i] += 1
            last_position = pos + i
        newboard[position] -= move_cnt

        c_hole=False
        if player and last_position < 6 and newboard[last_position] == 1:
            take_opponents.append(last_position)
            c_hole=True

        elif not player and 5 < last_position and last_position < len(newboard) - 1 and newboard[
            last_position] == 1:
            c_hole=True
            take_opponents.append(last_position)


        for i in take_opponents:
            newboard[score_idx] += newboard[i]
            newboard[score_idx] += newboard[-2-i]
            newboard[i] = 0
            newboard[-2-i] = 0



        if (player and last_position == 6) or (not player and last_position == len(newboard) - 1):
            free_turn = True
            pass
        else:
            free_turn = False

        return free_turn,c_hole,last_position




    
    def h21(self, board):
        '''
        (# of oppo’s f-holes) - (# of user’s f-holes)
        '''
        oppo_f_num=0
        user_f_num=0
        for i in range(6):
            if board[i+7]==0:
                continue
            free_turn,c_hole,last_position=self.board_move(board,i,False)
            if free_turn:
                oppo_f_num+=1
        for i in range(6):
            if board[i]==0:
                continue
            free_turn,c_hole,last_position=self.board_move(board,i)
            if free_turn:
                user_f_num+=1


        return oppo_f_num-user_f_num

    def h22(self, board):
        '''
        {(# of pieces in oppo’s c-hole) + (# of oppo’s c-hole)} – {(# of pieces in user’s c-hole) + (# of user’s c-hole)}
        '''

        oppo_c_hole_set=set()
        c_hole_list=[]
        for i in range(6):
            if board[i+7]==0 or board[i+7] >=13:
                continue
            free_turn,c_hole,last_position=self.board_move(board,i,False)
            if  c_hole:
                oppo_c_hole_set.add(last_position)
                node_list=[i,last_position]
                c_hole_list.append(node_list)

        num_oppo_c_hole=len(oppo_c_hole_set)
        pices_oppo_c_hole=0

        if num_oppo_c_hole !=0:
            for i in oppo_c_hole_set:
                for node in c_hole_list:
                    if node[1]==i:
                        pices_oppo_c_hole += board[-2-node[1]]
                        break

        user_c_hole_set=set()
        c_hole_list=[]
        for i in range(6):
            if board[i]==0 or board[i] >=13:
                continue
            free_turn,c_hole,last_position=self.board_move(board,i)
            if  c_hole:
                user_c_hole_set.add(last_position)
                node_list=[i,last_position]
                c_hole_list.append(node_list)

        num_user_c_hole=len(user_c_hole_set)
        pices_user_c_hole=0

        if num_user_c_hole !=0:
            for i in oppo_c_hole_set:
                for node in c_hole_list:
                    if node[1]==i:
                        pices_user_c_hole += board[-2-i]
                        break


        return num_oppo_c_hole + pices_oppo_c_hole - num_user_c_hole - pices_user_c_hole




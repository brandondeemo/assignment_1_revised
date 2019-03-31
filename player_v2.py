from kalah import reverse_board
from runner import Player, Mercy


class User(Player):
    def __init__(self):
        super().__init__()
        self.mercy = Mercy()
        '''
        Check Player class in runner.py to get information about useful predefined functions
        e.g. move, get_score, is_empty, step
        '''        
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
            first_step_f = self.g(step, first_step_board) + self.h1(first_step_board)
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
            sec_step_f = self.g(step, sec_step_board) + self.h1(sec_step_board)
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

                    third_step_f=self.g(step,third_step_board)+self.h1(third_step_board)
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

        raise NotImplementedError
        
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



    
    def h21(self, board):
        '''
        (# of oppo’s f-holes) - (# of user’s f-holes)
        '''
        raise NotImplementedError

    def h22(self, board):
        '''
        {(# of pieces in oppo’s c-hole) + (# of oppo’s c-hole)} – {(# of pieces in user’s c-hole) + (# of user’s c-hole)}
        '''
        raise NotImplementedError
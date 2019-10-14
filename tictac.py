import copy
import pdb
import math

class tictac(object):

    def __init__(self):
        pass

    def resultmax(self,A,action): # 2 means CPU plays 
        state = copy.copy(A)
        state[action] = 2
        return state

    def resultmin(self,A,action): # 1 means Player plays
        state = copy.copy(A)
        state[action] = 1
        return state

    def terminalTest(self,A): 
        pos = -1 
        
        if A[0] != 0 and ((A[0]==A[3] and A[3]==A[6]) or (A[0]==A[4] and A[4]==A[8]) or (A[0]==A[1] and A[1]==A[2])):
            pos = 0
        
        elif A[1]!=0 and pos == -1 and (A[1]==A[4] and A[4] == A[7]):
            pos = 1
        elif A[2]!=0 and pos == -1 and ((A[2]==A[5] and A[5]==A[8]) or (A[2]==A[4] and A[4]==A[6])):
            pos = 2
        elif A[3]!=0 and pos == -1 and A[3] == A[4] and A[4] == A[5]:
            pos = 3
        elif A[6]!=0 and pos == -1 and A[6] == A[7] and A[7] == A[8]:
            pos = 6
        
        if pos == -1:
            for i in range(0,9): # -2 if it is not filled 
                if A[i] == 0:
                    return -2

        return pos
    
    def utility(self,state,pos):
        if pos == -1: #space not available  and draw
            return 0

        if state[pos] == 1: # player made it
            return -1
        else: 
            return 1      #CPU made it

    def maxValue(self,A):

        state = copy.copy(A)
        pos = self.terminalTest(state)
        if pos != -2:  #space not available
            return self.utility(state,pos)
        
        v = -math.inf

        for a in range(0,9):
            if state[a]==0:  # action if space was empty ie neither 0 or 1
                v = max(v,self.minValue(self.resultmax(state,a)))
            if v == 1:
                return v

        return v


    def minValue(self,A):
        state = copy.copy(A)
        pos = self.terminalTest(state)
        if pos != -2:  #space not available
            return self.utility(state,pos)
        
        v = math.inf 

        for a in range(0,9):
            if state[a]==0:
                v = min(v,self.maxValue(self.resultmin(state,a)))
            if v == -1:
                return v

        return v 


    def minimax(self,state):
        maxval = -3 # to initialize final value will  be 0 ,1 or -1 ( draw , win , or loose)
        maxa = -3   # action which gave maximum value

        #print("in minimax ",state)

        for a in range(0,9):
            if state[a]==0:

                
                temp = self.minValue(self.resultmax(state,a))
                
                #print("inside minimax ",temp)

                if maxval < temp :
                    maxval  = temp
                    maxa = a

                if maxval == 1:
                    
                    break 
        
        return maxa
    
    def display(self,state):

        l = [] # to transform list of 0,1,2 to ' ','*' and 'o' 

        for i in range(0,9):
            if state[i]== 0:
                l.append(' ')
            elif state[i] == 1:
                l.append('*')
            else:
                l.append('o')
        
        print(' ',l[0],' | ',l[1],' | ',l[2],' ')
        print('-----|-----|------')
        print(' ',l[3],' | ',l[4],' | ',l[5],' ')
        print('-----|-----|------')
        print(' ',l[6],' | ',l[7],' | ',l[8],' ')

    def moveInp(self,state): # to take imput from player
        move = int(input("Enter your  move .. "))
        while state[move] != 0:
            move = int(input(" Invalid! input Enter your  move .. "))

        return move

    def game(self,state): # game after first input from player

        while True:
            move = self.minimax(state)
            print("CPU PLAYS ",move)
            state[move] = 2
            self.display(state)
            pos = self.terminalTest(state)
            if pos!= -2 :
                if pos == -1:
                    print("Its a draw")
                else:
                    print("CPU WON")
                break
            move = self.moveInp(state)
            state[move] = 1
            self.display(state)
            pos = self.terminalTest(state)
            if pos!= -2 :
                if pos == -1:
                    print("Its a draw")
                else:
                    print("YOU WON")
                break
        return
                
    
    def displayHelp(self):
        
        print("move positions for input ")
        print('  0  |  1  |  2  ')
        print('-----|-----|------')
        print('  3  |  4  |  5  ')
        print('-----|-----|------')
        print('  6  |  7  |  8  ')



    def gamePlay(self): #main funtion to start game

    
        while True:

            print("======Player vs CPU TIC-TAC-TOE=====")
            print("1. First Move CPU ")
            print("2. First Move Player ")
            print("3. Help ")
            print("4. Exit ")
            choice = int(input("MAKE YOUR CHOICE ...... "))

            if choice > 3:
                break

            state = [0,0,0,0,0,0,0,0,0]
            self.display(state)


            move = 0

            if choice == 1:
                move = self.minimax(state)
                print("CPU plays  ",move)
                state[move] = 2
                move = self.moveInp(state)
                state[move] = 1
                self.game(state)

            elif choice == 2:
                move = self.moveInp(state)
                state[move] = 1
                self.game(state)

            else:
                self.displayHelp()    
            

                  

#s = [0,0,0,0,0,0,0,0,0]
tmp = tictac()
tmp.gamePlay()
#print(tmp.minimax(s))





               
            
        

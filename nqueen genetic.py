import numpy as np
import sys
import random
import copy 
import pdb
import matplotlib.pyplot as plt
class NQueen(object):
    
    def __init__(self,n=8,pNum=4,gens=500000):
        '''
        inputs :
        n : Number of Queens
        popu : Population
        gen : number of maximum generations
        Output: returns an object of chessboard with N queens
        '''

        self.n = n
        self.pNum = pNum
        self.gens = gens
        self.ecou =[]
        self.errorZero = False
        self.population = np.zeros((pNum,n),int) 

    def populate(self):
        '''
        To initialize population
        '''
        
        cb = np.array([x for x in range(0,self.n)])
        for x in range(0,self.pNum): 
            random.shuffle(cb)
            self.population[x] = copy.deepcopy(cb)


    def xover(self,state1,state2,site):
        temp = copy.deepcopy(state1)
        for x in range(site,self.n):
            temp[x] = state2[x]
        return temp    


    def crossover(self,ActualCount):
        '''
        input : Actual Count for next gen
        output
        crossovered population
        '''
        '''
        print("----INSIDE CROSSOVER---")
        self.printPop()
        print("----exp----")
        print(self.ecou)
        
        print("----actcou----")
        print(ActualCount)'''
        temp = np.zeros((self.pNum,self.n),int)
        mate = []
        xOverSite = []
        tIndex = 0
        #print("------")
        #self.printPop()
        #print(ActualCount)
        #print("------")

        for i in range(0,self.pNum):
            if(tIndex==self.pNum):
                break
            for j in range(0,ActualCount[i]):
                if(tIndex==self.pNum):
                    break
                temp[tIndex] = copy.deepcopy(self.population[i])
                tIndex = tIndex + 1
        self.population = copy.deepcopy(temp)
        #mate  = np.zeros(self.pNum,int)
        #xOverSite = np.zeros(self.pNum,int)
        '''
        print("updated populaion---")
        self.printPop()
        print("-----")'''

        for i in range(0,self.pNum):
            mate.append(random.randrange(0,self.pNum))
            xOverSite.append(random.randrange(0,self.n))
        for i in range(0,self.pNum):
            temp[i] = self.xover(self.population[i],self.population[mate[i]],xOverSite[i])
        '''
        print("-----M and X--")
        print(mate)
        print(xOverSite)
        print("----temp-----")
        print(temp)'''

        self.population = copy.deepcopy(temp)
        ''' 
        self.printPop()
        print("-----End CrossOver-----")'''


        

    def mutate(self):
        '''
        To mutation population
        
        '''
        
        for i in range(0,self.pNum):
            self.population[i][random.randrange(0,self.n)] = random.randrange(0,self.n)
        


    def fitValue(self,state):
        '''
        input :
        state : one population state
        output : returns how fit a state is
        '''
        #print("state recieved",state)

        
        
        Attack = 0
            
        for x in range(0,self.n):
            for y in range(0,self.n):
                if x!=y  and state[x]==state[y]:
                    Attack = Attack + 1
        #print("attack after horizontal scan ",Attack)
        for col in range(0,self.n):
            row = state[col]
            sc = 0

            if row <= col:
                sc = col - row
            sr = row -(col - sc)
            while sc < self.n and sr < self.n:
                if state[sc] == sr and sc!=col and sr != row:
                    Attack = Attack + 1
                sc = sc+1
                sr = sr + 1

            ec = self.n-1

            if row + col < self.n-1:
                ec = row + col
                sr = 0
            else:
                sr = row + col - ec
            
            while ec >= 0 and sr < self.n :
                if state[ec]==sr and ec!=col and sr != row:
                    Attack = Attack + 1
                ec =  ec - 1
                sr = sr + 1

            
            
        error = Attack

        if error == 0:
            #print(state,"===",Attack)
            self.errorZero = True

        return ((self.n*(self.n-1))- Attack) ,error
                       


    def fitness(self):
        
        x = np.zeros(self.pNum,int)
        xSq = np.zeros(self.pNum,int)
        er = np.zeros(self.pNum,int)
        #expCount = np.zeros(self.pNum,float)
        self.ecou = np.zeros(self.pNum,float)
        ActualCount = np.zeros(self.pNum,int)
        sumfitness = 0

        for i in range(0,self.pNum):
            x[i],er[i] = self.fitValue(self.population[i])
            xSq[i] = x[i]*x[i]

        
        sumfitness = sum(xSq)
        error = sum(er)/len(er)
        for i in range(0,self.pNum):
            #expCount[i] = (xSq[i] / sumfitness) * self.pNum
            if sumfitness ==0:
                self.ecou[i] = 0
            else:

                self.ecou[i] = (xSq[i] / sumfitness) * self.pNum
            
                
               
            ActualCount[i] = round(self.ecou[i])
             
        #print(expCount)
        return ActualCount,error   

    def allOnes(self,Act_count):
        for i in range(0,self.pNum):
            if Act_count[i]==1:
                return False
        return True        
    
    def equal(self,CountA,CountB):
        for i in range(0,self.pNum):
           if CountA[i]!=CountB[i]:
               return False
        return True   
    
    def printPop(self):
        for i in range(0,self.pNum):
            print(self.population[i])

    def evolve(self):
        '''
        input :
        threshold : error to achieve before stopping evoltuion
        '''
        p = 0
        Prev_Act_Count,p = self.fitness()
        print("initial gen")
        self.printPop()
        print("-----end init-----")
        e = []
        temp_e = 0
        
        x = 0
        for gen in range(0,self.gens):
            Act_Count, temp_e = self.fitness()
            e.append(temp_e)
            
            x= gen
            if self.errorZero:
                
                break

            if self.equal(Act_Count,Prev_Act_Count):    
                self.mutate()
            else:
                self.crossover(Act_Count)
            Prev_Act_Count = copy.deepcopy(Act_Count)    
            
        print("stopped after gen",x)
        self.errorZero = False

        for i in range(0,self.pNum):
            self.fitValue(self.population[i])
            if self.errorZero:
                print(self.population[i],"\n------------")
                break
        z = []
        factor = len(e)/100
        z.append(e[0])
        for i in range(0,len(e),int(factor)-1):
            z.append(e[i])
        plt.plot(z)
        plt.show()

        print("-----end final------")
        self.printPop()


                
        
            
a = NQueen()
a.evolve()


                


            

            

        


                
                
            
    

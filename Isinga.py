import math
import random
import numpy as np
class Ising:
    
    def __init__ (self,temp, conf, N=100):
        
        self.N = N
        self.temp = temp
        self.J = 1
        self.conf = conf
        if (conf == 1):
            start = np.random.random((N,N))
            self.table = np.zeros((N,N))
            self.table[start>=0.25] = 1
            self.table[start<0.25] =-1
        elif (conf == 2):
            self.table = np.zeros((N,N))
            self.table[start>=0.75] = 1
            self.table[start<0.75] =-1
        else:
            self.table = np.random.choice([-1,1], size = (N,N))
            
        self.Et = 0
        self.Mt = 0
        self.Ct = 0
        
    def evoluzionemc(self):
        """
        Fa un passo di evoluzione (1 flip)
        """
        for i in range (self.N**2):
            riga=np.random.randint(0,self.N)
            colonna=np.random.randint(0,self.N)
            s = self.table[riga,colonna]
            primi = self.table[(riga-1)%self.N,colonna]+self.table[(riga+1)%self.N,colonna]+\
                          self.table[riga,(colonna-1)%self.N]+self.table[riga,(colonna+1)%self.N]
            delta_en = 2*s*primi
        
            if(self.flip_accettato(delta_en)):
                self.table[riga,colonna]*=-1
        return self.table
    
    def flip_accettato(self,delta_en):
        """
        Si passa la delta_energia per calcolare la 
        probabilità di accettare la mossa
        """
        accettato = False
        exp = math.exp(-(delta_en/self.temp))
        if(delta_en<0):
            accettato = True
        else:
            x = random.random()
            if(exp>x):
                accettato = True
            else:
                accettato = False
        return accettato
        
        
    def energia(self):
        """
        Calcola l'energia totale del sistema in una data configurazione
        """
        en = 0
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                primi_vicini = self.table[(i-1)%self.N,j]+self.table[(i+1)%self.N,j]+\
                          self.table[i,(j-1)%self.N]+self.table[i,(j+1)%self.N]
                en -= self.table[i,j]*primi_vicini
        return en/4.
    
    def magnetizzazione(self):
        """
        Calcola la magnetizzazione del sistema in una data configurazione
        """
        return np.sum(self.table)
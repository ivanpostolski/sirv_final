# -*- coding: utf-8 -*-
"""SIR with SS
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1XdkuI8dn70I5tLOkuiDVsed828pui6U4
"""
"""
Created on Sept 16 2020
 
@author: emanuel
"""
import numpy as np
import pylab as plb
from pynverse import inversefunc
from scipy.integrate import quad
from scipy import interpolate
from scipy.interpolate import interp1d
 

def ecs(x,t,EK,beta,gamma,M):
    Th=x[0] #g^-1 susceptibles
    NS=x[1] 
    NIS=x[2] 
    NRS=x[3]
    NS2=x[4]

    S=x[5]
    I=x[6]
    R=x[7]
    N=x[8]
    
    if NS>1e-20:
        pS=(NS-NRS-NIS)/NS
        pI=NIS/NS
        pR=NRS/NS
    else:
        print(I,Th)
        pS=0
        pI=NIS/(NIS+NRS)
        pR=NRS/(NIS+NRS)
    
    if g(Th) < 1e-40:
        __import__('ipdb').set_trace()
        Th=0
    
    if x.all()>-1e-20:
      dTh=(-beta*pI)*Th
      #dNS=dTh*gprima(Th)+Th*dTh*gdosprima(Th)+beta*EK*pI*pS*NS #MM
      dNS=dTh*gprima(Th)+Th*dTh*gdosprima(Th)
      dNIS=-gamma*NIS+beta*pI*((pS-pI)*(NS2-NS+EK*NS)-NS) #Nueva
      #dNIS=-gamma*NIS+beta*pI*((pS-pI)*NS2-(pS-pI+1)*NS)-beta*pI*(pS-pI)*EK*NS #NuevaOP2
      dNRS=gamma*NIS-beta*pI*pR*((NS2-NS)+EK*NS) ##MM 

      #dNS=dTh*gprima(Th)+Th*dTh*gdosprima(Th) #MOYAL
      #dNIS=beta*pI*((pS-pI)*Th*2*gdosprima(Th)-Th*gprima(Th))-gamma*NIS  #MOYAL
      #dNRS=gamma*NIS-beta*pI*pR*(Th**2)*gdosprima(Th) #MOYAL
      #dNS2=(-beta*pI)*(Th*gprima(Th)+(Th**2)*gdosprima(Th)+(Th**3)*gtresprima(Th))+beta*pI*pS*EK*(2*NS2+NS)
      dNS2=(-beta*pI)*(Th*gprima(Th)+(Th**2)*gdosprima(Th)+(Th**3)*gtresprima(Th))
      dS=dTh*gprima(Th)
      dI=beta*pI*Th*gprima(Th)-gamma*I
      dR=gamma*I
      dN=beta*NIS*EK

      dx=np.array([dTh,dNS,dNIS,dNRS,dNS2,dS,dI,dR,dN])
      return dx
    else:
      return np.zeros(len(x))


 
def int_rk4(f,x,dt,t,EK,beta,gamma,M):
    k_1 = f(x,t,EK,beta,gamma,M)
    k_2 = f(x+dt*0.5*k_1,t,EK,beta,gamma,M)
    k_3 = f(x+dt*0.5*k_2,t,EK,beta,gamma,M)
    k_4 = f(x+dt*k_3,t,EK,beta,gamma,M)
    y=x + dt*(k_1/6 + k_2/3 + k_3/3 + k_4/6)
    return y
 
def integra(T,dt,EK,beta,gamma,M):
    tiempo_modelo=np.arange(0,T,dt)
    sir=np.zeros([9,len(tiempo_modelo)])


    epsilon=1/M  
    alpha0=invg(1-epsilon)
    sir[0,0]=alpha0
    sir[1,0]=alpha0*gprima(alpha0)#/gprima(1)
    sir[2,0]=1*gprima(1)-alpha0*gprima(alpha0)#/gprima(1)
    sir[3,0]=0
    sir[4,0]=((alpha0**2)*gdosprima(alpha0)+alpha0*gprima(alpha0))#/gprima(1)
    sir[5,0]=1-epsilon
    sir[6,0]=epsilon
    sir[7,0]=0
    sir[8,0]=gprima(1)
    
    R2t=np.zeros(int(T/dt)-1)
    for i in range(len(tiempo_modelo)-1):
      aux=int_rk4(ecs,sir[:,i],dt,tiempo_modelo[i],EK,beta,gamma,M)
      sir[:,i+1]=[max(0,aux[i]) for i in range(len(aux))]
      R2t[i]=1
    return np.array([sir,R2t])


lambd=5
g = lambda x: np.exp(lambd*(x-1))
gprima = lambda x: lambd*np.exp(lambd*(x-1));
gdosprima = lambda x: lambd*lambd*np.exp(lambd*(x-1))
gtresprima = lambda x: (lambd**3)*np.exp(lambd*(x-1))
invg=inversefunc(g)



#M=10000
#EK=0.9*0+0.1*50

#gamma=1
#beta=3



def sir_num(T,dt,EK,ga,b,lamb,pob):
    beta=b
    gamma=ga
    lambd=lamb
    M=pob
    g = lambda x: np.exp(lambd*(x-1))
    gprima = lambda x: lambd*np.exp(lambd*(x-1));
    gdosprima = lambda x: lambd*lambd*np.exp(lambd*(x-1))
    gtresprima = lambda x: (lambd**3)*np.exp(lambd*(x-1))
    invg=inversefunc(g)
    sirss=integra(T,dt,EK,beta,gamma,M)
    th,NS,NIS,NRS,NS2,S,I,R,N=sirss[0]
    #plb.figure()
    #plb.plot(S)
    #plb.plot(I)
    #plb.plot(R)
    #plb.show()
    return np.array([S,I,R])

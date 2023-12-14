#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:40:53 2023

@author: salma
"""

from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, execute, Aer
import numpy as np
import random


'''Introducing Error'''
def error():
    
    qc = QuantumCircuit(n*10, 1,name='Noise')
    
    qc.ry(np.pi/8, (n*10)-1)
    qc.measure((n*10)-1,0)

    for i in range(n*10):
        ran= random.randint(0, 10)
        if ran >=8:
            qc.x(i).c_if(0, 1)
        
    for i in range(n*10):
        ran= random.randint(0, 10)
        if ran >=7:
            qc.z(i).c_if(0, 1)
 
    return qc.to_instruction()

    

'''Error Correcrion Code'''
def QEC(c, n):
    
    qc = QuantumCircuit(n*10, n)
    qc = qc.compose(c)
    qc.barrier()
    
    for i in range(n):
        
        ind = i*8 + (n-1)
        
        bf = QuantumCircuit(n*9, name='Bit-Flip')
        
        bf.cx(i,ind+3)
        bf.cx(i,ind+6)
        bf.h(i)
        bf.h(ind+3)
        bf.h(ind+6)
        bf.cx(i,ind+1)
        bf.cx(i,ind+2)
        bf.cx(ind+3,ind+4)
        bf.cx(ind+3,ind+5)
        bf.cx(ind+6,ind+7)
        bf.cx(ind+6,ind+8)
        
        qc = qc.compose(bf)
        qc.barrier()
    
    
    qc= qc.compose(error())      
    qc.barrier()


    for i in range(n):
            
        ind = i*8 + (n-1)
        
        pf = QuantumCircuit(n*9, name='Phase-Flip')
        
        pf.cx(i,ind+1)
        pf.cx(i,ind+2)
        pf.cx(ind+3,ind+4)
        pf.cx(ind+3,ind+5)
        pf.cx(ind+6,ind+7)
        pf.cx(ind+6,ind+8)
        pf.ccx(ind+2, ind+1, i)
        pf.ccx(ind+5, ind+4, ind+3)
        pf.ccx(ind+8, ind+7, ind+6)
        pf.h(i)
        pf.h(ind+3)
        pf.h(ind+6)
        pf.cx(i,ind+3)
        pf.cx(i,ind+6)
        pf.ccx(ind+6, ind+3, i)
        
        qc = qc.compose(pf)
        qc.barrier()
        
        qc.measure(i, i)
        
        
    qc.draw("mpl")
    
    return qc



'''Our Circuit''' 
n = 1
qc = QuantumCircuit(n,n)
qc = QEC(qc, n)

qc.measure(0, 0) 
qc.draw()


'''Results'''
job = execute(qc, Aer.get_backend('qasm_simulator'),shots=1000)
output = job.result().get_counts()
plot_histogram(output, title='Results With QEC')
print(output)


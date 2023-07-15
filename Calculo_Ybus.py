import numpy as np
import cmath
import math

#------------------------------------------------------- Y BUS ---------------------------------------------------------
def Matriz_Y_Bus(V_fuentes, I_fuentes, Zs, Nro_Nodos, Nro_N_i, Nro_N_j):
    matriz_dato = np.concatenate([V_fuentes, I_fuentes, Zs], axis=0)
    salida_bus = np.zeros((Nro_Nodos, Nro_Nodos),dtype="complex_")

    filas, columnas = matriz_dato.shape

#admitancias de las lineas (fuera de la diagonal)
    for k in range(filas):
        i = int(matriz_dato[k,0].real-1)
        j = int(matriz_dato[k,1].real-1)       
        if i == -1 or j == -1:
            continue
        else:
            salida_bus[i,j] = (-1)/(matriz_dato[k,2])
            salida_bus[j,i] = salida_bus[i,j]

#admitancias de la diagonal
    aux = salida_bus.sum(axis=1)
    aux = np.diag(aux)
    salida_bus = salida_bus - aux


    for k in range(filas):
        i = int(matriz_dato[k,0].real-1)
        j = int(matriz_dato[k,1].real-1)
        if i == -1 or j == -1:
            if i == -1:
                salida_bus[j,j] = salida_bus[j,j] + 1/matriz_dato[k,2]
            elif j == -1:
                salida_bus[i,i] = salida_bus[i,i] + 1/matriz_dato[k,2]


    return salida_bus

#--------------------------------------------------- Z Thevenin ----------------------------------------------------
def Zth(y_bus):
    z_bus = np.linalg.inv(y_bus)
    zth = np.diag(z_bus)
    return zth, z_bus

#----------------------------------------------------- V Thevenin ---------------------------------------------------
def Vth(z_bus, corrientes, num_barra):
    vth = np.inner(z_bus,np.transpose(corrientes))
    matriz_thevenin = np.zeros((num_barra,2))

#Forma polar    
    for i in range(num_barra):
        matriz_thevenin[i,0],matriz_thevenin[i,1] = cmath.polar(vth[i])

#Radianes a grados
    for i in range(num_barra):
        matriz_thevenin[i,1] = matriz_thevenin[i,1]*180/math.pi
    return matriz_thevenin,vth
'''
#----------------------------------------------------- G BUS -------------------------------------------------------
def gbus(ybus,num_barra):
    g_bus=np.zeros((num_barra,num_barra))

    for i in range(num_barra):
        for j in range(num_barra):
            g_bus[i,j] = ybus[i,j].real

    return g_bus

#---------------------------------------------------- B BUS --------------------------------------------------------
def bbus(ybus,num_barra):
    b_bus=np.zeros((num_barra,num_barra))

    for i in range(num_barra):
        for j in range(num_barra):
            b_bus[i,j] = ybus[i,j].imag

    return b_bus
'''
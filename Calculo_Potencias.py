import numpy as np
import math
import cmath

                                    # -Potencias de las fuentes de voltaje- #

def V_fuentes(Imp_V_fuente, Voltaje_Pico, Desfase, Vth, Indice_V_fuente):

    Voltajes_Fuente = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")
    
    S_V_Fuente = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")

    # Cálculo de la corriente de las fuentes de voltaje.

    Corrientes_V_fuentes = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")

    for i in range(len(Voltaje_Pico)):

        #Indice_Vth = Indice_V_fuente[i] - 1
        Voltajes_Fuente[i] = Voltaje_Pico[i] * ((np.cos(Desfase[i])) + (np.sin(Desfase[i]) * 1j))
        
        Voltaje_Impedancia = Voltajes_Fuente[i] - Vth[Indice_V_fuente[i] - 1]
        
        Corrientes_V_fuentes[i] = Voltaje_Impedancia / Imp_V_fuente[i]

        S_V_Fuente[i] = (Voltajes_Fuente[i] * np.conjugate(Corrientes_V_fuentes[i]))
        
    
    P_V_fuente = S_V_Fuente.real
    Q_V_fuente = S_V_Fuente.imag
    
    return P_V_fuente, Q_V_fuente

                                # -Potencias de las fuentes de corriente- #

def I_fuentes(Corriente_I_fuente, V_Thevenin, Imp_I_fuente, Bus_I_i):
    
    Voltaje_I_Fuente = np.zeros(len(Bus_I_i), dtype="complex_")
    S_I_Fuente = np.zeros(len(Bus_I_i), dtype="complex_")
    
    for i in range(len(Bus_I_i)):
        
        Voltaje_I_Fuente[i] = V_Thevenin[Bus_I_i[i] - 1] + Corriente_I_fuente[i] * Imp_I_fuente[i]
        S_I_Fuente[i] =   Voltaje_I_Fuente[i] * np.conjugate(Corriente_I_fuente[i])

    P_I_fuente = S_I_Fuente.real
    Q_I_fuente = S_I_Fuente.imag
    
    return S_I_Fuente, P_I_fuente, Q_I_fuente
    
                                    # -Potencias de las impedancias- #

def Potencia_Z_Vf(Vfuente, DesfaseV, VThevenin, ImpVfuente, Nodo_i_Vfuente):
    
    VoltajesF = np.zeros((len(Nodo_i_Vfuente), 1), dtype="complex_")
    
    S_Vf_Z = np.zeros((len(Nodo_i_Vfuente), 1), dtype="complex_")
    

    for i in range(len(Nodo_i_Vfuente)):
        
        VoltajesF[i] = Vfuente[i] * ((np.cos(DesfaseV[i])) + (1j * np.sin(DesfaseV[i])))
        
        Voltaje_IMP = VThevenin[Nodo_i_Vfuente[i] - 1] - VoltajesF[i]
        Corriente_IMP = Voltaje_IMP / ImpVfuente[i]
        
        S_Vf_Z[i] = Voltaje_IMP * np.conjugate(Corriente_IMP)
        #print(S_Vf_Z[i])

    PZ_Vf = S_Vf_Z.real
    QZ_Vf = S_Vf_Z.imag
    
    return PZ_Vf, QZ_Vf

def Potencia_Z_If(ICorriente, Vthevenin, Impedancia_I_fuente, Nodo_i_Ifuente):

    S_If_Z = np.zeros((len(Nodo_i_Ifuente), 1), dtype="complex_")

    for i in range(len(Nodo_i_Ifuente)):

        S_If_Z[i] = (abs(ICorriente) ** 2) * Impedancia_I_fuente[i]

    PZ_If = S_If_Z.real
    QZ_If = S_If_Z.imag
    #print(PZ_If, QZ_If)
    return PZ_If, QZ_If

def Potencias_Z(Indice_Rama, Impedancias_Z, V_thevenin):
        
    S_Z = np.zeros((len(Impedancias_Z), 1), dtype="complex_")
    
    for i in range(len(Impedancias_Z)):

        if Indice_Rama[i, 1] == 0 or Indice_Rama[i, 0] == 0:
            
            if Indice_Rama[i, 1] == 0:

                S_Z[i] = (np.sqrt((V_thevenin[Indice_Rama[i, 0] - 1]).real ** 2 + (V_thevenin[Indice_Rama[i, 0] - 1]).imag ** 2)) ** 2 / np.conjugate(Impedancias_Z[i])
                

            elif Indice_Rama[i, 0] == 0:
                 
                S_Z[i] = (np.sqrt((V_thevenin[Indice_Rama[i, 1] - 1]).real ** 2 + (V_thevenin[Indice_Rama[i, 1] - 1]).imag ** 2)) ** 2 / np.conjugate(Impedancias_Z[i])
                

        elif Indice_Rama[i, 1] != 0 or Indice_Rama[i, 0] != 0:

            S_Z[i] = np.sqrt(((V_thevenin[Indice_Rama[i, 1] - 1] - V_thevenin[Indice_Rama[i, 0] - 1]).real ** 2) + ((V_thevenin[Indice_Rama[i, 1] - 1] - V_thevenin[Indice_Rama[i, 0] - 1]).imag ** 2)) ** 2 / np.conjugate(Impedancias_Z[i])
            
    P_Z = S_Z.real
    Q_Z = S_Z.imag
    
    return S_Z, P_Z, Q_Z  
    
                                        # -Balance de Potencias- #

def Balance_Potencias(P_f_v, PzVf, Q_f_v, QzVf, P_Z, Q_Z, PIf, QIf, PzIf,QzIf):

    P_V_Entregado = np.sum(P_f_v) + np.sum(PIf)
    Q_V_Entregado = np.sum(Q_f_v) + np.sum(QIf)

    P_Impedancias = np.sum(P_Z) + np.sum(PzVf) + np.sum(PzIf)
    Q_Impedancias = np.sum(Q_Z) + np.sum(QzVf) + np.sum(QzIf) 

    Delta_P = P_V_Entregado - P_Impedancias
    Delta_Q = Q_V_Entregado - Q_Impedancias
    
    return Delta_P, Delta_Q


#print(f"Pv: {P_V_fuente}")
#print(f"Qv: {Q_V_fuente}")
#print(S_Z)

#print(P_V_Entregado - P_Impedancias)


#print(Delta_P)
#print(Delta_Q)
import numpy as np
import math
import cmath

                                    # -Potencias de las fuentes de voltaje- #
def V_fuentes(Imp_V_fuente, Voltaje_Pico, Desface, Vth, Indice_V_fuente):

    

    # Transformación del voltaje pico de las fuentes a forma rectangular.

    Voltajes_Fuente = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")

    for i in range(len(Voltaje_Pico)):

        Voltajes_Fuente[i,0] = Voltaje_Pico[i] * (math.cos(Desface[i])) + Voltaje_Pico[i] * (math.sin(Desface[i]) * 1j)

    Voltaje_Potencia = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")

    # Cálculo de la corriente de las fuentes de voltaje.

    Corrientes_V_fuentes = np.zeros((len(Voltaje_Pico), 1), dtype="complex_")

    for i in range(len(Voltaje_Pico)):

        Indice_Vth = Indice_V_fuente[i] - 1
        Voltaje_Potencia[i,0] = Vth[Indice_Vth,0]
        Voltaje_Impedancia = Voltajes_Fuente[i,0] - Vth[Indice_Vth,0]
        Corrientes_V_fuentes[i,0] = Voltaje_Impedancia / Imp_V_fuente[i]
    
    P_V_fuente = (Voltaje_Potencia * np.conjugate(Corrientes_V_fuentes)).real
    Q_V_fuente = (Voltaje_Potencia * np.conjugate(Corrientes_V_fuentes)).imag
    #print(f"Pv: {P_V_fuente}")
    #print(f"Qv: {Q_V_fuente}")
    
    return P_V_fuente, Q_V_fuente
                                # -Potencias de las fuentes de corriente- #

def I_fuentes(Corriente_I_fuente, V_Thevenin, Imp_I_fuente, Bus_I_i):

    Voltaje_I_Fuente = np.zeros(len(Bus_I_i), dtype="complex_")
    S_I_Fuente = np.zeros(len(Bus_I_i), dtype="complex_")

    for i in range(len(Bus_I_i)):

        Voltaje_I_Fuente[i] = V_Thevenin[i]

        S_I_Fuente[i] =  Voltaje_I_Fuente[i] * np.conjugate(Corriente_I_fuente[i])

    P_I_fuente = S_I_Fuente.real
    Q_I_fuente = S_I_Fuente.imag
    print(S_I_Fuente)
    return S_I_Fuente, P_I_fuente, Q_I_fuente
    
                                    # -Potencias de las impedancias- #

def Potencia_Z_Vf(Vfuente, VThevenin, ImpVfuente, Nodo_i_Vfuente):
    #print(VThevenin)

    S_Vf_Z = np.zeros((len(Nodo_i_Vfuente), 1), dtype="complex_")

    for i in range(len(Nodo_i_Vfuente)):
        #print(VThevenin[Nodo_i_Vfuente[i] - 1])
        S_Vf_Z[i] = ((np.sqrt((((VThevenin[Nodo_i_Vfuente[i] - 1] - Vfuente[i]).real) ** 2) + (((VThevenin[Nodo_i_Vfuente[i] - 1] - Vfuente[i]).imag) ** 2))) ** 2) / np.conjugate(ImpVfuente[i])
        #print(S_Vf_Z[i])
        #print(S_Vf_Z)

    PZ_Vf = S_Vf_Z.real
    QZ_Vf = S_Vf_Z.imag

    return PZ_Vf, QZ_Vf

def Potencia_Z_If(IFuente, Vthevenin, Impedancia_I_fuente, Nodo_i_Ifuente):

    S_If_Z = np.zeros((len(Nodo_i_Ifuente), 1), dtype="complex_")

    for i in range(len(Nodo_i_Ifuente)):

        S_If_Z[i] = (np.sqrt(Vthevenin[i].real ** 2 + Vthevenin[i].imag ** 2)) ** 2 / np.conjugate(Impedancia_I_fuente)

    PZ_If = S_If_Z.real
    QZ_If = S_If_Z.imag

    return PZ_If, QZ_If

def Potencias_Z(Indice_Rama, Impedancias_Z, V_thevenin):
        
    S_Z = np.zeros((len(Impedancias_Z), 1), dtype="complex_")

    for i in range(len(Impedancias_Z)):

        if Indice_Rama[i, 1] == 0 or Indice_Rama[i, 0] == 0:
            
            if Indice_Rama[i, 1] == 0:

                S_Z[i] = (np.sqrt((V_thevenin[Indice_Rama[i, 0].real - 1]) ** 2 + (V_thevenin[Indice_Rama[i, 0] - 1].imag ** 2)) ** 2) / np.conjugate(Impedancias_Z[i])
                
                

            elif Indice_Rama[i, 0] == 0:
                 
                S_Z[i] = (np.sqrt((V_thevenin[Indice_Rama[i, 1].real - 1]) ** 2 + (V_thevenin[Indice_Rama[i, 1] - 1].imag ** 2)) ** 2) / np.conjugate(Impedancias_Z[i])
                

        elif Indice_Rama[i, 1] != 0 or Indice_Rama[i, 0] != 0:

            S_Z[i] = np.sqrt(((V_thevenin[Indice_Rama[i, 1] - 1] - V_thevenin[Indice_Rama[i, 0] - 1]).real ** 2) + ((V_thevenin[Indice_Rama[i, 1] - 1] - V_thevenin[Indice_Rama[i, 0] - 1]).imag ** 2)) ** 2 / np.conjugate(Impedancias_Z[i])
            
    P_Z = S_Z.real
    Q_Z = S_Z.imag
    #print(S_Z)
    return S_Z, P_Z, Q_Z  
    
                                        # -Balance de Potencias- #

def Balance_Potencias(P_f_v, PzVf, Q_f_v, QzVf, P_Z, Q_Z, PIf, QIf, PzIf,QzIf):

    P_V_Entregado = np.sum(P_f_v) + np.sum(PIf)
    Q_V_Entregado = np.sum(Q_f_v) + np.sum(QIf)

    P_Impedancias = np.sum(P_Z) + np.sum(PzVf) + np.sum(PzIf)
    Q_Impedancias = np.sum(Q_Z) + np.sum(QzVf) + np.sum(QzIf)
    #print(P_V_Entregado - P_Impedancias)

    Delta_P = np.round(P_V_Entregado - P_Impedancias, 4)
    Delta_Q = np.round(Q_V_Entregado - Q_Impedancias, 4)
   # print(Delta_P)
    #print(Delta_Q)
    return Delta_P, Delta_Q
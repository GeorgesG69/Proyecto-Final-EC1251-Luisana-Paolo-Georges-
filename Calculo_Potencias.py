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
        
    return P_V_fuente, Q_V_fuente
                                # -Potencias de las fuentes de corriente- #

def I_fuentes(Corriente_I_fuente, V_Thevenin, Imp_I_fuente):
    pass
                                    # -Potencias de las impedancias- #

def Potencias_Z(Imp_Z, Vth, Bus_i_Z):

    Admitancia = 1/Imp_Z
    S_carga = np.zeros((len(Bus_i_Z), 1), dtype="complex_")

    for i in range(len(Bus_i_Z)):
        index = Bus_i_Z[i] -1
        S_carga[i] = ((Vth[index,0]) ** 2) * np.conjugate(Admitancia[i])
    
        P_Carga = np.real(S_carga)
        Q_Carga = np.imag(S_carga)

    return P_Carga, Q_Carga

                                        # -Balance de Potencias- #

def Balance_Potencias(P_f_v, Q_f_v, P_Z, Q_Z):

    P_V_Entregado = P_f_v.sum(axis=0)
    Q_V_Entregado = Q_f_v.sum(axis=0)

    P_Carga = P_Z.sum(axis=0)
    q_carga = Q_Z.sum(axis=0)

    Delta_P = P_V_Entregado - P_Carga
    Delta_Q = Q_V_Entregado - q_carga

    return Delta_P, Delta_Q


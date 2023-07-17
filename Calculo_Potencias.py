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
                                    # -Potencias de las impedancias- #

def Potencias_Z(Imp_Z, Vth, Bus_i_Z):

    admitancia = 1/Imp_Z
    s_carga = np.zeros((len(Bus_i_Z), 1), dtype="complex_")

    for i in range(len(Bus_i_Z)):
        index = Bus_i_Z[i] -1
        s_carga[i] = ((Vth[index,0]) ** 2) * np.conjugate(admitancia[i])
    
        p_carga = np.real(s_carga)
        q_carga = np.imag(s_carga)

    print(p_carga, "\n\n", q_carga)
    return p_carga, q_carga

#------------------------------------------------ LINEFLOW --------------------------------------------------------
def lineflow(indice_l, dato_lineas, voltline):
    filas, columnas = indice_l.shape
    impline = np.zeros((filas,1),dtype="complex_")
    z_ij = np.zeros((filas,1),dtype="complex_")
    z_ji = np.zeros((filas,1),dtype="complex_")
    #corr_i = np.zeros((filas,1), dtype="complex_")
    #corr_j = np.zeros((filas,1), dtype="complex_")
    impline = dato_lineas[:,0] + dato_lineas[:,1]*1j
    admline = 1/(impline)

    for k in range(filas):
        #print(impline[k])
        v_i = voltline[indice_l[k,0] - 1,0]
        v_j = voltline[indice_l[k,1] - 1,0]
        corr_i = (v_i - v_j)*(admline[k])
        corr_j = (v_j - v_i)*(admline[k])
        z_ij[k,0] = v_i * np.conjugate(corr_i)
        z_ji[k,0] = v_j * np.conjugate(corr_j)
        #print(round(v_i - v_j, 4), admline[k])
        #print(corr_i)

    Pij = np.real(z_ij)
    Qij = np.imag(z_ij)
    Pji = np.real(z_ji)
    Qji = np.imag(z_ji)
    #print(f"{v_i} * conj(({v_i} - {v_j}) * {impline}) = {z_ij}")
    #print(cmath.polar(z_ij), "\n\n")
    #print(indice_l)
    return Pij, Qij, Pji, Qji

#-------------------------------------------------BALANCE DE POTENCIAS-------------------------------------------------
def Balance_Potencias(p_gen, q_gen, p_load, q_load):
    p_entregado = p_gen.sum(axis=0)
    q_entregado = q_gen.sum(axis=0)

    p_carga = p_load.sum(axis=0)
    q_carga = q_load.sum(axis=0)
    delta_p = p_entregado - p_carga
    delta_q = q_entregado - q_carga
    return delta_p, delta_q


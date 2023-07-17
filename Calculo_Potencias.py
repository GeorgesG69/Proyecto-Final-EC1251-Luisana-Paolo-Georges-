import numpy as np
import math
import cmath

#--------------------------------------------------- POTENCIA DEL GENERADOR -----------------------------------------
def generador(Imp_V_fuente, voltaje, phi, vth, index_gen):

    

    #Pasamos el voltaje del generador a su forma rectangular
    voltaje_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        voltaje_generado[i,0] = voltaje[i]*(math.cos(phi[i]) )+ voltaje[i]*(math.sin(phi[i])*1j)

    voltaje_potencia=np.zeros((len(voltaje),1),dtype="complex_")
    #Calculo de la corriente del generador
    corriente_generado=np.zeros((len(voltaje),1),dtype="complex_")
    for i in range(len(voltaje)):
        indice_vth = index_gen[i] - 1
        voltaje_potencia[i,0] = vth[indice_vth,0]
        voltaje_carga = voltaje_generado[i,0] - vth[indice_vth,0]
        corriente_generado[i,0] = voltaje_carga/Imp_V_fuente[i]
    
    p_generado = (voltaje_potencia * np.conjugate(corriente_generado)).real
    q_generado = (voltaje_potencia * np.conjugate(corriente_generado)).imag
    #print(np.sqrt(p_generado **2 + q_generado**2))
        
    return p_generado, q_generado
#---------------------------------------------------- POTENCIA DE LA CARGA ------------------------------------------

def Cargas(imp_carga, Vth, bus_i_carga):

    admitancia = 1/imp_carga
    s_carga = np.zeros((len(bus_i_carga), 1), dtype="complex_")

    for i in range(len(bus_i_carga)):
        index = bus_i_carga[i] -1
        s_carga[i] = ((Vth[index,0]) ** 2) * np.conjugate(admitancia[i])
    
        p_carga = np.real(s_carga)
        q_carga = np.imag(s_carga)
    #print(np.sqrt(p_carga ** 2 + q_carga **2))
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
def balance(p_gen, q_gen, p_load, q_load):
    p_entregado = p_gen.sum(axis=0)
    q_entregado = q_gen.sum(axis=0)

    p_carga = p_load.sum(axis=0)
    q_carga = q_load.sum(axis=0)
    delta_p = p_entregado - p_carga
    delta_q = q_entregado - q_carga
    return delta_p, delta_q

def perdidas(P_ij, Q_ij, P_ji, Q_ji):

    s_perdida = (P_ij + Q_ij*1j) + (P_ji + Q_ji*1j)
    #print(s_perdida)

    return s_perdida
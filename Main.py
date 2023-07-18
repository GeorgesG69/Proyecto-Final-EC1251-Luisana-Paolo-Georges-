import pandas as pd
import numpy as np
import Calculo_Impedancias
import Calculo_Ybus
import Calculo_Potencias

                            # -Cálculo de la velocidad angular en base a la frecuencia- #

Dframe_f_output = pd.read_excel("data_io.xlsx","f_and_ouput", header=None)

Frecuencia = Dframe_f_output.iloc[0, 1]

Vel_Ang = round(Frecuencia * 2 * np.pi)

                                            # -Lectura de datos- #

# -Fuente de voltaje:

Dframe_V_fuente = pd.read_excel("data_io.xlsx", "V_fuente")
Dframe_V_fuente.fillna(0, inplace=True)    # Rellenar vacíos con 0.

Res_V_fuente = np.array(Dframe_V_fuente.iloc[:, 4])                     # Resistencia de la V_fuente.
Ind_V_fuente = np.array(Dframe_V_fuente.iloc[:, 5]) * (10 ** -3)        # Inductancia de la V_fuente.
Cap_V_fuente = np.array(Dframe_V_fuente.iloc[:, 6]) * (10 ** -6)        # Capacitancia de la V_fuente.
Desfase_V_fuente = np.array(Dframe_V_fuente.iloc[:, 3], dtype="float_") # Angulo de desfase V_fuente.
V_pico_V_fuente = np.array(Dframe_V_fuente.iloc[:, 2] / np.sqrt(2))     # Voltaje pico de la V_fuente.
Nodo_V_fuente_i = np.array(Dframe_V_fuente.iloc[:, 0])                  # Nodo i V_fuente.
Nodo_V_fuente_j = np.full((len(Dframe_V_fuente.iloc[:, 0])), 0)         # Nodo j V_fuente.

# -Fuente de corriente:

Dframe_I_fuente = pd.read_excel("data_io.xlsx","I_fuente")
Dframe_I_fuente.fillna(0, inplace=True)    # Rellenar vacíos con 0.

Res_I_fuente = np.array(Dframe_I_fuente.iloc[:, 4])                     # Resistencia de la I_fuente.
Ind_I_fuente = np.array(Dframe_I_fuente.iloc[:, 5]) * (10 ** -3)        # Inductancia de la I_fuente.
Cap_I_fuente = np.array(Dframe_I_fuente.iloc[:, 6]) * (10 ** -6)        # Capacitancia de la I_fuente.

Desfase_I_fuente = np.array(Dframe_I_fuente.iloc[:, 3], dtype="float_") # Angulo de desfase I_fuente.
I_pico_I_fuente = np.array(Dframe_I_fuente.iloc[:, 2] / np.sqrt(2))     # Corriente pico de la I_fuente.

Nodo_I_fuente_i = np.array(Dframe_I_fuente.iloc[:, 0])                  # Nodo i I_fuente.
Nodo_I_fuente_j = np.full((len(Dframe_I_fuente.iloc[:, 0])), 0)         # Nodo j I_fuente.
index_carga = np.concatenate(([Nodo_I_fuente_i], [Nodo_I_fuente_j]))    # Matriz de conexion de las cargas.
index_carga = np.transpose(index_carga)

# -Resistencias, inductancias y capacitancias:

Dframe_Z = pd.read_excel("data_io.xlsx","Z")
Dframe_Z.fillna(0, inplace=True)    # Rellenar vacíos con 0.

Res_Z = np.array(Dframe_Z.iloc[:, 3])                                   # Resistores.
Ind_Z = np.array(Dframe_Z.iloc[:, 4]) * (10 ** -6)                      # Inductores.
Cap_Z = np.array(Dframe_Z.iloc[:, 5]) * (10 ** -6)                      # Capacitores.

Nodo_Z_i = np.array(Dframe_Z.iloc[:, 0])                                # Bus i.
Nodo_Z_j = np.array(Dframe_Z.iloc[:, 1])                                # Bus j.

                                            # -Indices de las ramas- #

Indice_Rama = np.concatenate(([Nodo_Z_i],[Nodo_Z_j]))     
Indice_Rama = np.transpose(Indice_Rama)

                                    # -Numero de nodos del Circuito en AC- #
# Buscar el número más alto entre los nodos i y j de Z.

Nro_Nodos_i = max(Dframe_Z.iloc[:,0])
Nro_Nodos_j = max(Dframe_Z.iloc[:,1])

Nro_Nodos = int(max(Nro_Nodos_i,Nro_Nodos_j))

                        # -Inicio de los cálculos para el análisis del Circuito en AC- #
def Main_Analisis():

                                        # -Cálculo de impedancias- #

    # Fuentes de voltaje.

    Imp_V_fuente, Impres_v, Impind_v, Impcap_v = Calculo_Impedancias.V_fuente(Res_V_fuente, Ind_V_fuente, Cap_V_fuente, Vel_Ang, Nodo_V_fuente_i)
    V_fuente =  np.concatenate(([Nodo_V_fuente_i], [Nodo_V_fuente_j], [Imp_V_fuente]), axis=0)
    V_fuente = np.transpose(V_fuente)
    
    
    # Fuentes de corriente.

    Imp_I_fuente, Impres_i, Impind_i, impcap_i = Calculo_Impedancias.I_fuente(Res_I_fuente, Ind_I_fuente, Cap_I_fuente, Vel_Ang, Nodo_I_fuente_i)
    I_fuente = np.concatenate(([Nodo_I_fuente_i], [Nodo_I_fuente_j], [Imp_I_fuente]), axis=0)
    I_fuente = np.transpose(I_fuente)
    

    # Ramas.

    Imp_Z, Impres_Z, Impind_Z, Impcap_Z = Calculo_Impedancias.Z(Res_Z, Ind_Z, Cap_Z, Vel_Ang, Nodo_Z_i)
    Zs = np.concatenate(([Nodo_Z_i], [Nodo_Z_j], [Imp_Z]), axis=0)      
    Zs = np.transpose(Zs)
    
    Dato_Ramas = np.concatenate(([Res_Z], [Ind_Z], [Cap_Z]), axis=0)
    Dato_Ramas = np.transpose(Dato_Ramas)


                                            # -Cálculo del Ybus, Zth y Vth- #

    # Corrientes inyectadas.

    Vector_Corrientes_I = Calculo_Impedancias.Matriz_Corrientes(V_pico_V_fuente, Desfase_V_fuente, Imp_V_fuente, Nro_Nodos, Nodo_V_fuente_i)
    

    # Ybus.

    y_bus = Calculo_Ybus.Matriz_Y_Bus(V_fuente, I_fuente, Zs, Nro_Nodos, Nro_Nodos_i, Nro_Nodos_j) 
    y_bus = np.round(y_bus,4)
    

    # Zth.

    zth, zbus = Calculo_Ybus.Zth(y_bus)


    # Vth.

    V_thevenin, V_thevenin_rect = Calculo_Ybus.Vth(zbus, Vector_Corrientes_I, Nro_Nodos)
    
    
                                                # -Cálculo de las potencias- #

    # Potencia del generador.

    P_V_fuente, Q_V_fuente= Calculo_Potencias.V_fuentes(Imp_V_fuente, V_pico_V_fuente, Desfase_V_fuente, V_thevenin_rect, Nodo_V_fuente_i)
    

    # Potencia de las impedancias.

    P_Z, Q_Z  = Calculo_Potencias.Potencias_Z(Imp_Z, V_thevenin_rect, Nodo_Z_i)


    # Balance de potencias.

    D_P, D_Q = Calculo_Potencias.Balance_Potencias(P_V_fuente, Q_V_fuente, P_Z, Q_Z)
    

if __name__ == "__main__":

    print(f"\n\tIniciando cálculos para el circuito en AC\n")
    Main_Analisis()

import pandas as pd
import numpy as np



# Extracción de datos de data_io.xlsx (f_and_output)

datos_f_output = pd.read_excel("data_io.xlsx","f_and_ouput", header=None)
frecuencia = datos_f_output.iloc[0, 1]



# Extracción de datos de data_io.xlsx (V_fuente)

datos_V_fuente = pd.read_excel("data_io.xlsx", "V_fuente")            # Datos de hoja V_fuente
#datos_V_fuente.fillna(0, inplace=True)                                   # Cuadros vacios = 0

res_V = np.array(datos_V_fuente.iloc[:, 4])                              # Resistencias fuentes de voltaje
ind_V = np.array(datos_V_fuente.iloc[:, 5]) * (10 ** -3)                 # Inductancias fuentes de voltaje
cap_V = np.array(datos_V_fuente.iloc[:, 6]) * (10 ** -6)                 # Capacitancias fuentes de voltaje
des_V = np.array(datos_V_fuente.iloc[:, 3], dtype="float_")              # Angulos de desfase fuentes de voltaje
Vpico = np.array(datos_V_fuente.iloc[:, 2] / np.sqrt(2))                              # Voltajes pico fuentes de voltaje
bus_i_V = np.array(datos_V_fuente.iloc[:, 0])                            # Bus i V_fuente
bus_j_V = np.full((len(datos_V_fuente.iloc[:, 0])), 0)                   # Bus j V_fuente



# Extracción de datos de data_io.xlsx (I_fuente)

datos_I_fuente = pd.read_excel("data_io.xlsx","I_fuente")             # Datos de hoja I_fuente
#datos_I_fuente.fillna(0, inplace=True)                                   # Cuadros vacios = 0

res_I = np.array(datos_I_fuente.iloc[:, 4])                              # Resistencias fuentes de corriente
ind_I = np.array(datos_I_fuente.iloc[:, 5]) * (10 ** -3)                 # Inductancias fuentes de corriente
cap_I = np.array(datos_I_fuente.iloc[:, 6]) * (10 ** -6)                 # Capacitancias fuentes de corriente
des_I = np.array(datos_I_fuente.iloc[:, 3], dtype="float_")              # Angulos de desfase fuentes de corriente
Ipico = np.array(datos_I_fuente.iloc[:, 2] / np.sqrt(2))                              # Corrientes pico fuentes de corriente
bus_i_I = np.array(datos_I_fuente.iloc[:, 0])                            # Bus i I_fuente
bus_j_I = np.full((len(datos_I_fuente.iloc[:, 0])), 0)                   # Bus j I_fuente

index_carga = np.concatenate(([bus_i_I], [bus_j_I]))                     # Matriz de conexion de las cargas
index_carga = np.transpose(index_carga)

 

# Extracción de datos de data_io.xlsx (Z)

datos_Z = pd.read_excel("data_io.xlsx","Z")                           # Datos de hoja Z
#datos_Z.fillna(0, inplace=True)

res_Z = np.array(datos_Z.iloc[:, 3])                                     # Resistencias Z
ind_Z = np.array(datos_Z.iloc[:, 4]) * (10 ** -6)                        # Inductancias Z
cap_Z = np.array(datos_Z.iloc[:, 5]) * (10 ** -6)                        # Capacitancias Z
bus_i_Z = np.array(datos_Z.iloc[:, 0])                                  # Nodo i Z
bus_j_Z = np.array(datos_Z.iloc[:, 1])                                  # Nodo j Z

index_linea = np.concatenate(([bus_i_Z],[bus_j_Z]))                    # Matriz de conexion de las cargas
index_linea = np.transpose(index_linea)



# Calculo de w

w = round(frecuencia * 2 * np.pi)



# Numero de nodos prorporcionados por el usuario

num_nodos_i = max(datos_Z.iloc[:,0])
num_nodos_j = max(datos_Z.iloc[:,1])
num_nodos_total = int(max(num_nodos_i,num_nodos_j))


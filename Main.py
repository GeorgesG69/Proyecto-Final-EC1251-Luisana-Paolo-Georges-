import pandas as pd
import numpy as np
import Calculo_Impedancias
import Calculo_Ybus
import Calculo_Potencias


#Lectura del archivo excel a trabajar
       
        
                      
Dframe_f_output = pd.read_excel("data_io.xlsx","f_and_ouput", header=None)

#Colocar 0 en lugares vacíos





#Cálculo de la velocidad angular en base a la frecuencia

Frecuencia = Dframe_f_output.iloc[0, 1]

Vel_Ang = round(Frecuencia * 2 * np.pi)







# Datos
# -Fuente de voltaje:
Dframe_V_fuente = pd.read_excel("data_io.xlsx", "V_fuente")
Dframe_V_fuente.fillna(0, inplace=True)

Res_V_fuente = np.array(Dframe_V_fuente.iloc[:, 4])                     #Resistencia de la V_fuente
Ind_V_fuente = np.array(Dframe_V_fuente.iloc[:, 5]) * (10 ** -3)        #Inductancia de la V_fuente
Cap_V_fuente = np.array(Dframe_V_fuente.iloc[:, 6]) * (10 ** -6)        #Capacitancia de la V_fuente
Desfase_V_fuente = np.array(Dframe_V_fuente.iloc[:, 3], dtype="float_") #Angulo de desfase V_fuente
V_pico_V_fuente = np.array(Dframe_V_fuente.iloc[:, 2] / np.sqrt(2))                  #Voltaje pico de la V_fuente
Nodo_V_fuente_i = np.array(Dframe_V_fuente.iloc[:, 0])                  #Nodo i V_fuente
Nodo_V_fuente_j = np.full((len(Dframe_V_fuente.iloc[:, 0])), 0)         #Nodo j V_fuente


# -Fuente de corriente:
Dframe_I_fuente = pd.read_excel("data_io.xlsx","I_fuente")
Dframe_I_fuente.fillna(0, inplace=True)

Res_I_fuente = np.array(Dframe_I_fuente.iloc[:, 4])                     #Resistencia de la I_fuente
Ind_I_fuente = np.array(Dframe_I_fuente.iloc[:, 5]) * (10 ** -3)        #Inductancia de la I_fuente
Cap_I_fuente = np.array(Dframe_I_fuente.iloc[:, 6]) * (10 ** -6)        #Capacitancia de la I_fuente
Desfase_I_fuente = np.array(Dframe_I_fuente.iloc[:, 3], dtype="float_") #Angulo de desfase I_fuente
I_pico_I_fuente = np.array(Dframe_I_fuente.iloc[:, 2] / np.sqrt(2))     #Voltaje pico de la I_fuente
Nodo_I_fuente_i = np.array(Dframe_I_fuente.iloc[:, 0])                  #Nodo i I_fuente
Nodo_I_fuente_j = np.full((len(Dframe_I_fuente.iloc[:, 0])), 0)         #Nodo j I_fuente
index_carga = np.concatenate(([Nodo_I_fuente_i], [Nodo_I_fuente_j]))    #Matriz de conexion de las cargas
index_carga = np.transpose(index_carga)


# -Resistencias, inductancias y capacitancias
Dframe_Z = pd.read_excel("data_io.xlsx","Z")
Dframe_Z.fillna(0, inplace=True)

Res_Z = np.array(Dframe_Z.iloc[:, 3])                     
Ind_Z = np.array(Dframe_Z.iloc[:, 4]) * (10 ** -6)        
Cap_Z = np.array(Dframe_Z.iloc[:, 5]) * (10 ** -6)        
Nodo_Z_i = np.array(Dframe_Z.iloc[:, 0])                  
Nodo_Z_j = np.array(Dframe_Z.iloc[:, 1])                  

index_linea = np.concatenate(([Nodo_Z_i],[Nodo_Z_j]))     
index_linea = np.transpose(index_linea)

# --Numero de nodos del SEP
Nro_Nodos_i = max(Dframe_Z.iloc[:,0])
Nro_Nodos_j = max(Dframe_Z.iloc[:,1])

Nro_Nodos = int(max(Nro_Nodos_i,Nro_Nodos_j))


def run():

    #Fuentes de voltaje
    Imp_V_fuente, Impres_v, Impind_v, Impcap_v = Calculo_Impedancias.V_fuente(Res_V_fuente, Ind_V_fuente, Cap_V_fuente, Vel_Ang, Nodo_V_fuente_i)
    V_fuente =  np.concatenate(([Nodo_V_fuente_i],[Nodo_V_fuente_j],[Imp_V_fuente]), axis=0)
    V_fuente = np.transpose(V_fuente)
    
    
    #Fuentes de corriente
    Imp_I_fuente, Impres_i, Impind_i, impcap_i = Calculo_Impedancias.I_fuente(Res_I_fuente, Ind_I_fuente, Cap_I_fuente, Vel_Ang, Nodo_I_fuente_i)
    I_fuente = np.concatenate(([Nodo_I_fuente_i],[Nodo_I_fuente_j],[Imp_I_fuente]),axis=0)
    I_fuente = np.transpose(I_fuente)
    


    #Ramas
    Imp_Z, Impres_Z, Impind_Z, Impcap_Z = Calculo_Impedancias.Z(Res_Z, Ind_Z, Cap_Z, Vel_Ang, Nodo_Z_i)
    Zs = np.concatenate(([Nodo_Z_i],[Nodo_Z_j],[Imp_Z]),axis=0)      
    Zs = np.transpose(Zs)
    #print(imp_linea)
    dato_linea = np.concatenate(([Res_Z],[Ind_Z], [Cap_Z]),axis=0)
    dato_linea = np.transpose(dato_linea)

   
#------------------------------------------------- CALCULO DE YBUS, VTH Y ZTH --------------------------------------------------
    #Corrientes inyectadas
    Vector_Corrientes_I = Calculo_Impedancias.Matriz_Corrientes(V_pico_V_fuente, Desfase_V_fuente, Imp_V_fuente, Nro_Nodos, Nodo_V_fuente_i)
    #print(Vector_Corrientes_I)

    #Y bus
    y_bus = Calculo_Ybus.Matriz_Y_Bus(V_fuente, I_fuente, Zs, Nro_Nodos, Nro_Nodos_i, Nro_Nodos_j) 
    y_bus = np.round(y_bus,4)
    #print(y_bus)


    #Z de thevenin
    zth, zbus = Calculo_Ybus.Zth(y_bus)

    #Voltajes de thevenin
    V_thevenin,V_thevenin_rect = Calculo_Ybus.Vth(zbus, Vector_Corrientes_I, Nro_Nodos)
    #print(V_thevenin)


#------------------------------------------------ CALCULO DE LAS POTENCIAS ------------------------------------------------

    #Potencia del generador
    p_gen, q_gen= Calculo_Potencias.generador(Imp_V_fuente, V_pico_V_fuente, Desfase_V_fuente, V_thevenin_rect, Nodo_V_fuente_i)
    

    #Potencia de las impedancias
    p_load, q_load  = Calculo_Potencias.Cargas(Imp_Z, V_thevenin_rect, Nodo_Z_i)

    #Lineflow (Flujo de potencias)
    p_ij, q_ij, p_ji, q_ji = Calculo_Potencias.lineflow(index_linea, dato_linea, V_thevenin_rect)

    #Balance de potencias
    delta_p, delta_q = Calculo_Potencias.balance(p_gen, q_gen, p_load, q_load)
    #print(delta_p)
    #print(delta_q)




if __name__ == "__main__":
    run()

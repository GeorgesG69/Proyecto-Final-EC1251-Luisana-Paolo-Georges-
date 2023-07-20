import pandas as pd
import numpy as np
import shutil
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
Valores_V_fuente = Dframe_V_fuente.astype(float, errors="ignore")
Dframe_V_fuente.fillna(0, inplace=True)    # Rellenar vacíos con 0.
DfWarnings_V = pd.DataFrame(Valores_V_fuente)

Res_V_fuente = np.array(Dframe_V_fuente.iloc[:, 4])                     # Resistencia de la V_fuente.
Ind_V_fuente = np.array(Dframe_V_fuente.iloc[:, 5]) * (10 ** -3)        # Inductancia de la V_fuente.
Cap_V_fuente = np.array(Dframe_V_fuente.iloc[:, 6]) * (10 ** -6)        # Capacitancia de la V_fuente.

Desfase_V_fuente = np.array(Dframe_V_fuente.iloc[:, 3], dtype="float_") # Angulo de desfase V_fuente.
V_pico_V_fuente = np.array(Dframe_V_fuente.iloc[:, 2] / np.sqrt(2))     # Voltaje pico de la V_fuente.

Nodo_V_fuente_i = np.array(Dframe_V_fuente.iloc[:, 0])                  # Nodo i V_fuente.
Nodo_V_fuente_j = np.full((len(Dframe_V_fuente.iloc[:, 0])), 0)         # Nodo j V_fuente.

# -Fuente de corriente:

Dframe_I_fuente = pd.read_excel("data_io.xlsx","I_fuente")
Valores_I_fuente = Dframe_I_fuente.astype(float, errors="ignore")
Dframe_I_fuente.fillna(0, inplace=True)    # Rellenar vacíos con 0.
DfWarnings_I = pd.DataFrame(Valores_I_fuente)

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
Valores_Z = Dframe_Z.astype(float, errors="ignore")
Dframe_Z.fillna(0, inplace=True)    # Rellenar vacíos con 0.
DfWarnings_Z = pd.DataFrame(Valores_Z)


Res_Z = np.array(Dframe_Z.iloc[:, 3])                                   # Resistores.
Ind_Z = np.array(Dframe_Z.iloc[:, 4]) * (10 ** -6)                      # Inductores.
Cap_Z = np.array(Dframe_Z.iloc[:, 5]) * (10 ** -6)                      # Capacitores.

Nodo_Z_i = np.array(Dframe_Z.iloc[:, 0])                                # Bus i.
Nodo_Z_j = np.array(Dframe_Z.iloc[:, 1])                                # Bus j.

                                          # -Dataframes para guardado- #

Dframe_VZth = pd.read_excel("data_io.xlsx","VTH_AND_ZTH")
Dframe_Sfuente = pd.read_excel("data_io.xlsx","Sfuente")
Dframe_SZ = pd.read_excel("data_io.xlsx","S_Z")
Dframe_BalanceS = pd.read_excel("data_io.xlsx","Balance_S")

#Dframe_VZth.iloc[0:0]
#Dframe_Sfuente.iloc[0:0]
#Dframe_SZ.iloc[0:0]
#Dframe_BalanceS.iloc[0:0]

                                            # -Indices de las ramas- #

Indice_Rama = np.concatenate(([Nodo_Z_i],[Nodo_Z_j]))     
Indice_Rama = np.transpose(Indice_Rama)

                                    # -Numero de nodos del Circuito en AC- #
# Buscar el número más alto entre los nodos i y j de Z.

Nro_Nodos_i = max(Dframe_Z.iloc[:,0])
Nro_Nodos_j = max(Dframe_Z.iloc[:,1])

Nro_Nodos = int(max(Nro_Nodos_i,Nro_Nodos_j))

                                                # -Warnings- #
Escritor_Warnings = pd.ExcelWriter("data_io.xlsx", mode="a", if_sheet_exists="overlay")

# -V fuente
for i in range(len(Nodo_V_fuente_i)):

    if (V_pico_V_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(V_pico_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Valor pico no puede ser negativo"

        DfWarnings_V.to_excel(Escritor_Warnings, "V_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("Valor pico no puede ser negativo")

    if (Res_V_fuente[i] < 0) or (Ind_V_fuente[i] < 0) or (Cap_V_fuente[i] < 0):

        IndiceVPNeg = [valor for valor, dato in enumerate(Res_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."   

        IndiceVPNeg = [valor for valor, dato in enumerate(Ind_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        IndiceVPNeg = [valor for valor, dato in enumerate(Cap_V_fuente) if dato < 0]
        DfWarnings_V.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        DfWarnings_V.to_excel(Escritor_Warnings, "V_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("(V) Res/Ind/Cap no puede ser negativo.")

# -I fuente
for i in range(len(Nodo_I_fuente_i)):

    if (I_pico_I_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(I_pico_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Valor pico no puede ser negativo"

        DfWarnings_I.to_excel(Escritor_Warnings, "I_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("Valor pico no puede ser negativo")

    if (Res_I_fuente[i] < 0) or (Ind_I_fuente[i] < 0) or (Cap_I_fuente[i] < 0):
        IndiceVPNeg = [valor for valor, dato in enumerate(Res_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."   

        IndiceVPNeg = [valor for valor, dato in enumerate(Ind_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        IndiceVPNeg = [valor for valor, dato in enumerate(Cap_I_fuente) if dato < 0]
        DfWarnings_I.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

        DfWarnings_I.to_excel(Escritor_Warnings, "I_fuente", index=False)
        Escritor_Warnings.close() 

        raise TypeError("(I) Res/Ind/Cap no puede ser negativo.")
    
# -Z
for i in range(len(Nodo_Z_i)):

    if (Res_Z[i] < 0) or (Ind_Z[i] < 0) or (Cap_Z[i] < 0):
       
       IndiceVPNeg = [valor for valor, dato in enumerate(Res_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo."
        
       IndiceVPNeg = [valor for valor, dato in enumerate(Ind_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

       IndiceVPNeg = [valor for valor, dato in enumerate(Cap_Z) if dato < 0]
       DfWarnings_Z.loc[IndiceVPNeg, "Warning"] = "Res/Ind/Cap no puede ser negativo." 

       DfWarnings_Z.to_excel(Escritor_Warnings, "Z", index=False)
       Escritor_Warnings.close()     

       raise TypeError("(Z) Res/Ind/Cap no puede ser negativo.")


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
    #print(V_pico_V_fuente)
    Vector_Corrientes_I = Calculo_Impedancias.Matriz_Corrientes(V_pico_V_fuente, I_pico_I_fuente,  Desfase_V_fuente, Desfase_I_fuente, Imp_V_fuente, Nro_Nodos, Nodo_V_fuente_i, Nodo_I_fuente_i)
    

    # Ybus.

    y_bus = Calculo_Ybus.Matriz_Y_Bus(V_fuente, I_fuente, Zs, Nro_Nodos, Nro_Nodos_i, Nro_Nodos_j) 
    #y_bus = np.round(y_bus,4)
    

    # Zth.

    Zth, zbus = Calculo_Ybus.Zth(y_bus)


    # Vth.

    V_thevenin, V_thevenin_rect = Calculo_Ybus.Vth(zbus, Vector_Corrientes_I, Nro_Nodos)
    

                                                # -Cálculo de las potencias- #

    # Potencia de las fuentes de voltaje.

    P_V_fuente, Q_V_fuente = Calculo_Potencias.V_fuentes(Imp_V_fuente, V_pico_V_fuente, Desfase_V_fuente, V_thevenin_rect, Nodo_V_fuente_i)

    # Potencia de las impedancias de las fuentes de voltaje

    Pzvf, Qzvf = Calculo_Potencias.Potencia_Z_Vf(V_pico_V_fuente, Desfase_V_fuente, V_thevenin_rect, Imp_V_fuente, Nodo_V_fuente_i)


    # Potencia de las fuentes de corriente

    S_I_fuente, P_I_fuente, Q_I_fuente = Calculo_Potencias.I_fuentes(I_pico_I_fuente, V_thevenin_rect, Imp_I_fuente, Nodo_I_fuente_i)

    # Potencia de las impedancias de las fuentes de corriente

    Pzif, Qzif = Calculo_Potencias.Potencia_Z_If(I_pico_I_fuente, V_thevenin_rect, Imp_I_fuente, Nodo_I_fuente_i)
    
    # Potencia de las impedancias.

    S_Z, P_Z, Q_Z = Calculo_Potencias.Potencias_Z(Indice_Rama, Imp_Z, V_thevenin_rect)


    # Balance de potencias.

    D_P, D_Q = Calculo_Potencias.Balance_Potencias(P_V_fuente, Pzvf, Q_V_fuente,  Qzvf, P_Z, Q_Z, P_I_fuente, Q_I_fuente, Pzif, Qzif)


                                                # -Guardado de datos- #

    Escritor_Guardado = pd.ExcelWriter("data_io.xlsx", mode="a", if_sheet_exists="overlay")
    
    # -Vth y Zth
    Modulo_Vth = np.sqrt((V_thevenin_rect.real ** 2) + (V_thevenin_rect.imag ** 2))
    Angulo_Vth = np.arctan(V_thevenin_rect.imag / V_thevenin_rect.real) * 180 / np.pi

    for i in range(len(Modulo_Vth)):

        Dframe_VZth.loc[i, "Bus i"] = i + 1
        Dframe_VZth.loc[i, "|Vth| (kV)"] = Modulo_Vth[i]
        Dframe_VZth.loc[i, "<Vth (degrees)"] = Angulo_Vth[i]
        Dframe_VZth.loc[i, "Rth (ohms)"] = Zth[i].real
        Dframe_VZth.loc[i, "Xth (ohms)"] = Zth[i].imag

    Dframe_VZth.to_excel(Escritor_Guardado, "VTH_AND_ZTH", index=False)

    # -Sfuente
    for i in range(len(Nodo_V_fuente_i)):
        
        Dframe_Sfuente.loc[i, "Bus i"] = Nodo_V_fuente_i[i]
        Dframe_Sfuente.loc[i, "Bus j"] = Nodo_V_fuente_j[i]
        Dframe_Sfuente.loc[i, "P [W]"] = P_V_fuente[i]
        Dframe_Sfuente.loc[i, "Q [VAr]"] = Q_V_fuente[i]

    FilaIV = len(Nodo_V_fuente_i) 
    
    for k in range(len(Nodo_I_fuente_i)):
        
        Dframe_Sfuente.loc[FilaIV + k + 1, "Bus i"] = Nodo_I_fuente_i[k]
        Dframe_Sfuente.loc[FilaIV + k + 1, "Bus j"] = Nodo_I_fuente_j[k]
        Dframe_Sfuente.loc[FilaIV + k + 1, "P [W]"] = round(P_I_fuente[k], 4)
        Dframe_Sfuente.loc[FilaIV + k + 1, "Q [VAr]"] = round(Q_I_fuente[k], 4)
      
    Dframe_Sfuente.to_excel(Escritor_Guardado, "Sfuente", index=False)

    # -S_Z
    for i in range(len(P_Z)):

        Dframe_SZ.loc[i, "Bus i"] = Nodo_Z_i[i]
        Dframe_SZ.loc[i, "Bus j"] = Nodo_Z_j[i]
        Dframe_SZ.loc[i, "P [W]"] = P_Z[i]
        Dframe_SZ.loc[i, "Q [Var]"] = Q_Z[i]


    Dframe_SZ.to_excel(Escritor_Guardado, "S_Z", index=False)

    # -Balance S
    Dframe_BalanceS.loc[0, "Pf total(W)"] = round(np.sum(P_V_fuente) + np.sum(P_I_fuente), 4)
    Dframe_BalanceS.loc[0, "Qf total(VAr)"] = round(np.sum(Q_V_fuente) + np.sum(Q_I_fuente), 4)
    Dframe_BalanceS.loc[0, "Pz total(W)"] = round(np.sum(P_Z) + np.sum(Pzvf) + np.sum(Pzif), 4)
    Dframe_BalanceS.loc[0, "Qz total(VAr)"] = round(np.sum(Q_Z) + np.sum(Qzvf) + np.sum(Qzif), 4)
    Dframe_BalanceS.loc[0, "Delta P(W)"] = D_P
    Dframe_BalanceS.loc[0, "Delta Q total(VAr)"] = D_Q

    Dframe_BalanceS.to_excel(Escritor_Guardado, "Balance_S", index=False)
    

    Escritor_Guardado.close()

    

                                                # -Copiado del archivo- #

    FileName = Dframe_f_output.iloc[1, 1]

    shutil.copy2("data_io.xlsx", FileName)

    print(f"\n\tFinalizado para: {FileName}.\n")

if __name__ == "__main__":

    print(f"\n\tIniciando cálculos para el circuito en AC\n")
    Main_Analisis()

import numpy as np
import datos_excel as ex
import impedancias as imp

 

V_fuente = np.concatenate(([ex.bus_i_V],[ex.bus_j_V],[imp.imp_total_V]), axis=0)
V_fuente = np.transpose(V_fuente)

I_fuente = np.concatenate(([ex.bus_i_I],[ex.bus_j_I],[imp.imp_total_I]),axis=0)
I_fuente = np.transpose(I_fuente)

Z = np.concatenate(([ex.bus_i_Z],[ex.bus_j_Z],[imp.imp_total_Z]),axis=0)      
Z = np.transpose(Z)

matriz_de_datos = np.concatenate([V_fuente, I_fuente, Z], axis=0)

dato_linea = np.concatenate(([imp.imp_res_Z],[imp.imp_ind_Z], [imp.imp_cap_Z]),axis=0)
dato_linea = np.transpose(dato_linea)


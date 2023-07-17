import numpy as np
import math
import datos_excel as ex



# Impedancias V_fuente

imp_res_V = ex.res_V
imp_ind_V = 1j * ex.w * ex.ind_V
imp_cap_V = np.zeros((len(ex.bus_i_V)), dtype="complex_")
    
for b in range(len(imp_cap_V)):
    if ex.cap_V[b] == 0:

        imp_cap_V[b] = 0

    else:

        imp_cap_V[b] = (-1j) / (ex.w * ex.cap_V[b])

imp_total_V = imp_res_V + imp_ind_V + imp_cap_V

# Si no hay impedancia, se agrega una impedancia infima

for x in range(len(imp_total_V)):
    if imp_total_V[x] == 0:
            imp_total_V[x] == (10**-9) * 1j

print("Impedancia V:", imp_total_V)



# Impedancias I_fuente

imp_res_I = ex.res_I
imp_ind_I = 1j * ex.w * ex.ind_I
imp_cap_I = np.zeros((len(ex.bus_i_I)), dtype="complex_")
    
for b in range(len(imp_cap_I)):
                
    if ex.cap_I[b] == 0:

        imp_cap_I[b] = 0
            
    else:

        imp_cap_I[b] = (-1j) / (ex.w * ex.cap_I[b])

imp_total_I = imp_res_I + imp_ind_I + imp_cap_I
    
# Si no hay impedancia, se agrega una impedancia infima

for i in range(len(imp_total_I)):
    if imp_total_I[i] == 0:
        imp_total_I[i] == 0+(0.000001)*1j

print("Impedancia I:", imp_total_I)



# Impedancias Z

imp_res_Z = ex.res_Z
imp_ind_Z = 1j * ex.w * ex.res_Z
imp_cap_Z = np.zeros((len(ex.bus_i_Z)), dtype="complex_")

for b in range(len(ex.bus_i_Z)):
        
    if ex.cap_Z[b] == 0:

        imp_cap_Z[b] = 0

    else:
        imp_cap_Z[b] = (-1j) / (ex.w * ex.cap_Z[b])

imp_total_Z = imp_res_Z + imp_ind_Z + imp_cap_Z

print("impedancia z:", imp_total_Z)

 

# Conversión de grados a radianes V

for i in range(len(ex.des_V)):
    ex.des_V[i]= (ex.des_V[i] * math.pi)/180

print(ex.des_V)

# Matriz de iguales (Voltaje)

voltajes_x_impedancias = np.zeros((ex.num_nodos_total,1), dtype="complex_")
for i in range(len(ex.bus_i_V)):
    indice = ex.bus_i_V[i]-1
    voltajes_x_impedancias[indice] = (ex.Vpico[i]*(math.cos(ex.des_V[i]) + 1j*math.sin(ex.des_V[i])))/imp_total_V[i] 
voltajes_x_impedancias = np.round(voltajes_x_impedancias,4)

print(voltajes_x_impedancias)


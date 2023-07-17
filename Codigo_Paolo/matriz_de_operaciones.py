import numpy as np
import datos_excel as ex
import impedancias as imp
import matriz_de_datos as md


# Matriz contenedora de los datos

salida_bus = np.zeros((ex.num_nodos_total, ex.num_nodos_total),dtype="complex_")

filas, columnas = md.matriz_de_datos.shape

#admitancias de las lineas (fuera de la diagonal)
for k in range(filas):
    i = int(md.matriz_de_datos[k,0].real-1)
    j = int(md.matriz_de_datos[k,1].real-1)       
    if i == -1 or j == -1:
        continue
    else:
        salida_bus[i,j] = (-1)/(md.matriz_de_datos[k,2])
        salida_bus[j,i] = salida_bus[i,j]

#admitancias de la diagonal
aux = salida_bus.sum(axis=1)
aux = np.diag(aux)
salida_bus = salida_bus - aux


for k in range(filas):
    i = int(md.matriz_de_datos[k,0].real-1)
    j = int(md.matriz_de_datos[k,1].real-1)
    if i == -1 or j == -1:
        if i == -1:
                salida_bus[j,j] = salida_bus[j,j] + np.round(1/md.matriz_de_datos[k,2], 4)
        elif j == -1:
                salida_bus[i,i] = salida_bus[i,i] + np.round(1/md.matriz_de_datos[k,2], 4)

salida_bus = np.round(salida_bus, 4)

print(salida_bus)


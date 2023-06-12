import sys
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np

dirModelo = str(sys.argv[1])

dispositivos = ['Ryzen 5 3500U (1)', 'Ryzen 5 3500U (4)', 'NCS2 (Ubuntu)', 'NCS2 (Raspberry Pi 4)']
dispLectura = ['CPU1', 'CPU4', 'MYRIAD', 'MYRIAD-pi']
dispositivosBase = ['Ryzen 5 3500U (Ubuntu)', 'Raspberry Pi 4']

colores = ['aqua', 'orangered', 'chartreuse', 'indigo']

header = ['Datos', 'Ryzen 5 3500U (1)', 'Ryzen 5 3500U (4)', 'NCS2 (Ubuntu)', 'NCS2 (Raspberry Pi 4)']
nombres_filas = ['tiempo_carga', 'latencia', 'frames', 'media_consumo', 'desviacion_consumo', 'frames_por_w']

data = dict.fromkeys(dispositivos, None)

# function to add value labels
def addlabels(ax, dispositivos, media, desviacion):
    if desviacion:
        for i in range(len(dispositivos)):
            ax.text(i, media[i]//2, str(round(media[i], 2)) + ' ± ' + str(round(desviacion[i], 2)), ha = 'center',
                bbox = dict(facecolor = 'white', alpha = .5), fontsize=13)
    
    else:
        for i in range(len(dispositivos)):
            ax.text(i, media[i]//2, str(round(media[i], 2)), ha = 'center',
                bbox = dict(facecolor = 'white', alpha = .5), fontsize=13)
        

def plot_generic(dispositivos, y_datas, y_error, titles, name, xlabel, ylabels):
    fig = plt.figure(figsize=(17, 10))
    handles = []

    if len(y_datas) == 3:
        gs = fig.add_gridspec(4, 4)
        x = range(len(dispositivos))

        ax1 = plt.subplot(gs[:2, :2])
        ax2 = plt.subplot(gs[:2, 2:])
        ax3 = plt.subplot(gs[2:4, 1:3])

        axs = [ax1, ax2, ax3]

    elif len(y_datas) == 2:
        gs = fig.add_gridspec(4, 2)
        x = range(len(dispositivos))

        ax1 = plt.subplot(gs[1:3, 0])
        ax2 = plt.subplot(gs[1:3, 1])

        axs = [ax1, ax2]

    for k, ax in enumerate(axs):
        bars = ax.bar(dispositivos, y_datas[k], color=colores, edgecolor='black')
        handles.append(bars)

        if titles[k] == '(a) Consumo':
            ax.errorbar(dispositivos, y_datas[k], y_error, fmt='.', color='black')
            addlabels(ax, dispositivos, y_datas[k], y_error)
        else:
            addlabels(ax, dispositivos, y_datas[k], None)

        ax.set_title(titles[k], fontsize=20)
        ax.set_xlabel(xlabel, fontsize=15)
        ax.set_ylabel(ylabels[k], fontsize=15)

        ax.tick_params(axis='both', which='major', labelsize=13)

    plt.tight_layout()
    fig.legend(handles=handles[0], labels=dispositivos, loc='lower left', edgecolor='black')

    plt.savefig(f'{dirModelo}/{name}.png', dpi=500)
    plt.close()


def plot_table(dispositivos, datas, titles, fichero, invertidas):
    fig = plt.figure(figsize=(14, 6))

    plt.rcParams["figure.autolayout"] = True

    gs = fig.add_gridspec(3, 3)

    ax1 = plt.subplot(gs[:1, 1:3])
    ax2 = plt.subplot(gs[1:2, 1:3])
    ax3 = plt.subplot(gs[2:3, 1:3])

    axs = [ax1, ax2, ax3]

    for k, ax in enumerate(axs):
        matriz_calculos = [[dispositivos[0]] + [0]*len(dispositivos),
                        [dispositivos[1]] + [0]*len(dispositivos),
                        [dispositivos[2]] + [0]*len(dispositivos),
                        [dispositivos[3]] + [0]*len(dispositivos)]

        cell_colours = [['w']*(len(dispositivos)+1) for _ in range(len(dispositivos))]

        ax.axis('off')
        ax.axis('tight')

        for i in range(len(dispositivos)):
            for j in range(len(dispositivos)):
                if invertidas[k]:
                    matriz_calculos[i][j+1] = "{0:.2f}".format(datas[k][i]/datas[k][j])
                else:
                    matriz_calculos[i][j+1] = "{0:.2f}".format(datas[k][j]/datas[k][i])

                if float(matriz_calculos[i][j+1]) < 1.0:
                    cell_colours[i][j+1] = 'lightcoral'
                elif float(matriz_calculos[i][j+1]) > 1.0:
                    cell_colours[i][j+1] = 'mediumspringgreen'
                else:
                    cell_colours[i][j+1] = 'khaki'

        ax.set_title(titles[k], fontsize=16)
        tabla = ax.table(cellText=matriz_calculos, colLabels=[''] + dispositivos, loc='center', cellColours=cell_colours)

        for i in range(len(matriz_calculos)):
            for j in range(len(matriz_calculos[i])):
                tabla._cells[(i+1, j)].set_height(0.16)

    plt.savefig(f'{dirModelo}/{fichero}.png', dpi=500, bbox_inches='tight')
    plt.close()
    

# Lectura de datos de consumo base
consumo_base = pandas.read_csv("resultado/consumoBase_merged.csv", names=dispositivosBase, delimiter=' ')
consumo_base_pc = consumo_base['Ryzen 5 3500U (Ubuntu)'].mean()
consumo_base_pi = consumo_base['Raspberry Pi 4'].mean()

# Cálculo de media y desviación para cada dispositivo
medias_consumo = []
desviaciones_consumo = []
frames_por_w = []
fps = []
tiempos_carga = []
latencias = []

for dispositivo, disp_lectura in zip(dispositivos, dispLectura):
    # Lectura de datos de rendimiento y consumo
    throughput = pandas.read_csv(dirModelo + "/benchmark-" + disp_lectura + ".csv", names=[None, dispositivo], delimiter=';')
    consumo = pandas.read_csv(dirModelo + "/consumo-" + disp_lectura + ".csv", names=['consumo'])
    
    # Extracción de datos de rendimiento
    load_time = float(throughput[dispositivo].tolist()[17])
    latency = float(throughput[dispositivo].tolist()[21])
    frames = float(throughput[dispositivo].tolist()[22])

    # Cálculo de media y desviación de consumo
    if dispositivo == 'NCS2 (Raspberry Pi 4)':
        media_consumo = (consumo['consumo'] - consumo_base_pi).mean()
        desviacion_consumo = (consumo['consumo'] - consumo_base_pi).std()
    else:
        media_consumo = (consumo['consumo'] - consumo_base_pc).mean()
        desviacion_consumo = (consumo['consumo'] - consumo_base_pc).std()

    # Cálculo de iteraciones por W
    FPS_por_W = round(frames / media_consumo, 2)

    # Almacenamiento de resultados en listas
    tiempos_carga.append(load_time)                     #Tiempo de carga
    latencias.append(latency)                           #Latencia
    fps.append(frames)                                  #Cantidad de FPS
    medias_consumo.append(media_consumo)                #Media del consumo
    desviaciones_consumo.append(desviacion_consumo)     #Desviacion del consumo
    frames_por_w.append(FPS_por_W)                      #FPS por W

    # Creación de un diccionario con los resultados
    data[dispositivo] = [load_time, latency, frames, media_consumo, desviacion_consumo, FPS_por_W]


#Generación de las gráficas
plot_generic(dispositivos, [latencias, tiempos_carga], None,
            ['(a) Latencias', '(b) Cargas'], 'Tiempos', "Escenario\n",
            ["Tiempo (ms)", "Tiempo (ms)"])

plot_generic(dispositivos, [medias_consumo, fps, frames_por_w], desviaciones_consumo,
            ['(a) Consumo', '(b) Rendimiento', '(c) Eficiencia'], 'Eficiencia', "Escenario\n",
            ["Consumo (W)", "Rendimiento (FPS)", "Eficiencia (FPS / W)"])


#Generación de las tablas
plot_table(dispositivos, [fps, frames_por_w, latencias], ['(a) Rendimiento', '(b) Eficiencia', '(c) Latencia'], 'Tablas', [False, False, True])


# Guardamos el resumen del DataFrame en un archivo CSV en el directorio del modelo
df = pandas.DataFrame(data)

df.insert(0, 'Nombres', nombres_filas)
df.to_csv(f'{dirModelo}/resumen.csv', header=header, index=False, sep=" ")
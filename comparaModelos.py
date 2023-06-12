import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

dirModelo = str(sys.argv[1])

colLabels = ['Implementación', 'Precisión', 'GFLOPs', 'mParams']

dispositivos = ['Ryzen 5 3500U (1)', 'Ryzen 5 3500U (4)', 'NCS2 (Ubuntu)', 'NCS2 (Raspberry Pi 4)']

colores = ['#008fd5', '#fc4f30', '#e5ae37']

compIntelPublic = ['face-detection-retail-0004', 'face-detection-retail-0044']
compFrameworks = ['license-plate-recognition-barrier-0001', 'license-plate-recognition-barrier-0007']
compGFlops = ['single-image-super-resolution-1032', 'single-image-super-resolution-1033', 'text-image-super-resolution-0001']
compParams = ['person-attributes-recognition-crossroad-0230', 'person-attributes-recognition-crossroad-0238']

listaComp = [compIntelPublic, compFrameworks, compGFlops, compParams]
listaCompNames = ['compIntelPublic', 'compFrameworks', 'compGFlops', 'compParams']


def plot_generic(i, dispositivos, y_datas, titles, name, xlabel, ylabels, listaComp):
    dir = f'{dirModelo}/Comparativa{i}_{listaCompNames[i]}'

    fig = plt.figure(figsize=(17, 10))

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
        for i in range(len(y_datas[0])):
            ax.bar([j + i * 0.3 for j in x], y_datas[k][i], width=0.3, align="center", color=colores[i], edgecolor='black')

        if len(y_datas[0]) == 3:
            ax.set_xticks([i + 0.3 for i in x])
        else:
            ax.set_xticks([i + 0.15 for i in x])

        ax.set_title(titles[k], fontsize=20)
        ax.set_xticklabels(dispositivos, fontsize=13)
        ax.set_xlabel(xlabel, fontsize=15)
        ax.set_ylabel(ylabels[k], fontsize=15)

    if not os.path.isdir(dir):
        os.mkdir(dir, 0o777)

    plt.tight_layout()
    fig.legend(listaComp, loc='lower left', edgecolor='black')

    plt.savefig(f'{dir}/{name}.png', dpi=500)
    plt.close()

def plot_table(i, dispositivos, datas, titles, fichero, invertida, listaComp):
    dir = f'{dirModelo}/Comparativa{i}_{listaCompNames[i]}'

    x = range(len(dispositivos))

    if len(datas) == 3:
        fig = plt.figure(figsize=(15, 6))
        plt.rcParams["figure.autolayout"] = True

        gs = fig.add_gridspec(3, 4)

        ax1 = plt.subplot(gs[0, 1:3])
        ax2 = plt.subplot(gs[1, 1:3])
        ax3 = plt.subplot(gs[2, 1:3])

        axs = [ax1, ax2, ax3]

    elif len(datas) == 2:
        fig = plt.figure(figsize=(15, 8))
        plt.rcParams["figure.autolayout"] = True

        gs = fig.add_gridspec(4, 4)

        ax1 = plt.subplot(gs[1, 1:3])
        ax2 = plt.subplot(gs[2, 1:3])

        axs = [ax1, ax2]

    for k, ax in enumerate(axs):
        if len(listaComp) == 3:
            matriz_calculos = [[0] * (len(dispositivos)+1) for _ in range(6)]
            cell_colours = [['w']*(len(dispositivos)+1) for _ in range(6)]
        
        else:
            matriz_calculos = [[0] * (len(dispositivos)+1) for _ in range(2)]
            cell_colours = [['w']*(len(dispositivos)+1) for _ in range(2)]

        ax.axis('off')
        ax.axis('tight')

        h=0

        for i in range(len(listaComp)):
            for j in range(len(listaComp)):
                if i != j:
                    matriz_calculos[h][0] = str(listaComp[i]+' vs\n '+str(listaComp[j]))
                    for s in range(len(dispositivos)):
                        matriz_calculos[h][s+1] = "{0:.2f}".format(datas[k][i][s]/datas[k][j][s])

                        if float(matriz_calculos[h][s+1]) < 1.0:
                            if invertida:
                                cell_colours[h][s+1] = 'mediumspringgreen'
                            else:
                                cell_colours[h][s+1] = 'lightcoral'

                        elif float(matriz_calculos[h][s+1]) > 1.0:
                            if invertida:
                                cell_colours[h][s+1] = 'lightcoral'
                            else:
                                cell_colours[h][s+1] = 'mediumspringgreen'
                                
                        else:
                            cell_colours[h][s+1] = 'khaki'

                    h+=1

                else:
                    continue

        if len(listaComp) != 2:
            ax.set_title(titles[k], pad=27, fontsize=14)
        else:
            ax.set_title(titles[k], fontsize=14)  

        tabla = ax.table(cellText=matriz_calculos, colLabels=['Comparativa'] + dispositivos, loc='center', cellColours=cell_colours)

        for i in range(len(matriz_calculos)):
            for j in range(len(matriz_calculos[i])):
                tabla._cells[(i+1, j)].set_height(0.19)
                tabla.auto_set_column_width([j])            

        tabla.auto_set_font_size(False)  
        tabla.set_fontsize(7)

        tabla.scale(1, 1.25)

    plt.savefig(f'{dir}/{fichero}.png', dpi=500, bbox_inches='tight')
    plt.close()

for j, compList in enumerate(listaComp):

    # Gráfica 1
    medias_consumo_totales = []
    desviaciones_consumo_totales = []
    frames_por_wh_totales = []
    fps_totales = []
    latencias_totales = []
    tiempos_carga_totales = []

    for model in compList:

        medias_consumo = []
        desviaciones_consumo = []
        fps_por_w = []
        fps = []
        tiempos_carga = []
        latencias = []

        fichero_resumen = pd.read_csv(f'{dirModelo}/{model}/resumen.csv', delimiter=' ')

        for dispositivo in dispositivos:

            tiempos_carga.append(fichero_resumen[dispositivo].tolist()[0])
            medias_consumo.append(fichero_resumen[dispositivo].tolist()[3])
            fps_por_w.append(fichero_resumen[dispositivo].tolist()[5])
            fps.append(fichero_resumen[dispositivo].tolist()[2])
            latencias.append(fichero_resumen[dispositivo].tolist()[1])

        medias_consumo_totales.append(medias_consumo)
        desviaciones_consumo_totales.append(desviaciones_consumo)
        frames_por_wh_totales.append(fps_por_w)
        fps_totales.append(fps)
        tiempos_carga_totales.append(tiempos_carga)
        latencias_totales.append(latencias)

    plot_generic(j, dispositivos, [latencias_totales, tiempos_carga_totales],
                 ['(a) Latencias', '(b) Cargas'], 'Tiempo_grafica', "Dispositivo\n",
                 ["Tiempo (ms)", "Tiempo (ms)"], listaComp[j])

    plot_generic(j, dispositivos, [medias_consumo_totales, fps_totales, frames_por_wh_totales],
                 ['(a) Consumo', '(b) Rendimiento', '(c) Eficiencia'], 'Eficiencia_grafica', "Dispositivo\n",
                 ["Consumo (W)", "Rendimiento (FPS)", "FPS / W"], listaComp[j])

    plot_table(j, dispositivos, [latencias_totales, tiempos_carga_totales],
                 ['(a) Latencias', '(b) Cargas'], 'Tiempo_tabla', True, compList)

    plot_table(j, dispositivos, [medias_consumo_totales, fps_totales, frames_por_wh_totales],
                 ['(a) Consumo', '(b) Rendimiento', '(c) Eficiencia'], 'Eficiencia_tabla', False, compList)
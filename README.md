# Evaluación del Intel Neural Stick en entornos Fog de bajo coste - Códigos y resultados

Este repositorio es la estructura final de los códigos desarrollados y resultados obtenidos durante la realización del TFG. Se incluyen varios apartados para explicar la estructura de este repositorio.

Cuando hemos hecho referencia al "directorio de trabajo principal" durante el proyecto, nos referimos a este repositorio.

## 1. Código
Los códigos desarrollados se encuentran en el directorio raíz del repositorio:
* Script ‘demo_OpenVINO.sh’: Script escrito en Bash que permite ejecutar la aplicación de pruebas, entre otras incluidas en OpenVINO, con varios modelos indicados. Se recogerán métricas de rendimiento obtenidas de la ejecución, así como el consumo el escenario en que se ejecuta. 
* Script ‘demo_OpenModelZoo.sh’: Script escrito en Bash que nos permite ejecutar las aplicaciones de demostración incluidas en la herramienta Open Model Zoo, junto a una imagen o vídeo de entrada y modelos que se utilizarán.
* Script ‘benchmarkAnalisis.py’: Script escrito en Python para obtener ilustraciones y tablas individuales de todos los modelos ejecutados. 
* Script ‘comparaModelos.py’: Script escrito en Python para obtener las ilustraciones y tablas comparativas entre los modelos.
* Script ‘benchmarkAnalisis.sh’: Este script ha sido programado en Bash, de forma que nos permitirá ejecutar el resto de los códigos de forma automática, estableciendo el flujo de ejecución de todos los scripts generados. 

## 2. Métricas
Las métricas recogidas durante las ejecuciones se almacenan en carpetas con el nombre de cada modelo bajo el directorio [benchmark_app](https://github.com/VictorHidalgoUCLM/NeuralComputeStick2/tree/master/resultado/benchmark_app), situado en el directorio [resultado](https://github.com/VictorHidalgoUCLM/NeuralComputeStick2/tree/master/resultado), en el directorio raíz del repositorio.
En cada carpeta específica para los modelos encontramos los siguientes ficheros que almacenan las métricas recogidas, por ejemplo para el modelo [face-detection-retail-0004](https://github.com/VictorHidalgoUCLM/NeuralComputeStick2/tree/master/resultado/benchmark_app/face-detection-retail-0004):
* Ficheros con métricas de rendimiento: Se recogen para cada escenario en que se ha ejecutado la aplicación con el modelo las métricas de rendimiento de este. Son las hojas de cálculo que comienzan con el nombre ‘benchmark’.
* Ficheros con métricas de consumo: De la misma forma, encontramos ficheros para cada escenario que recogen los consumos instantáneos de la ejecución de cada modelo. Estos ficheros son hojas de cálculo que comienzan con el nombre ‘consumo’.
* Ficheros resumen: Durante la ejecución del script ‘benchmarkAnalisis.sh’ se genera un fichero resumen para cada modelo, recogiendo las métricas importantes y procesadas de cada uno de los escenarios en que se ha ejecutado el modelo.

## 3. Gráficas
Al igual que con las métricas, encontramos en distintos directorios las gráficas generadas:
* Carpetas que almacenan gráficas para las comparativas: Aquí encontraremos las gráficas separadas por tipo de comparativa, generadas por el script 'comparaModelos.py'. Un ejemplo es la [Comparativa Intel y public](https://github.com/VictorHidalgoUCLM/NeuralComputeStick2/tree/master/resultado/benchmark_app/Comparativa0_compIntelPublic). 
* Carpetas que almacenan gráficas individuales: Aquí encontraremos las gráficas individuales para cada modelo, junto a las métricas recogidas, generadas por el script 'benchmarkAnalisis.py'.

## 4. Ficheros de configuración
En la carpeta raíz del directorio encontramos los siguientes ficheros de configuración:
* Fichero ‘config.cfg’: Este fichero de configuración es el que se utiliza durante las ejecuciones en los escenarios donde el ordenador es el dispositivo anfitrión.
* Fichero ‘configPi.cfg’: Este fichero de configuración es el que se utiliza durante las ejecuciones en los escenarios donde la Raspberry Pi 4 es el dispositivo anfitrión. Es importante cambiar el nombre de este fichero a ‘config.cfg' cuando realicemos las pruebas en la Raspberry. 

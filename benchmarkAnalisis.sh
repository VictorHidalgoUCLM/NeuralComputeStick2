#!/bin/bash

#IP de RaspberryPi
#HOST=192.168.1.139

#SUCCESS=1

#Generamos gŕaficas y tablas para todos los modelos, incluyendo comparaciones
stringarray="face-detection-retail-0004 face-detection-retail-0044 license-plate-recognition-barrier-0001 license-plate-recognition-barrier-0007 person-attributes-recognition-crossroad-0230 single-image-super-resolution-1032 single-image-super-resolution-1033 text-image-super-resolution-0001 person-attributes-recognition-crossroad-0238"


#########Ejecución en pc##########
#bash demo_OpenVINO.sh -a benchmark_app -t 60 $stringarray

#########Ejecución en pi##########
#Comprobación de que raspberry está conectada a internet
# hasta que no haya un ping correcto, no se sale de este bucle
#while [ $SUCCESS -ne 0 ]; do
  #ping -c1 $HOST 1>/dev/null 2>/dev/null
  #SUCCESS=$?
  #echo "Intentado llegar a raspberry..."
#done

#Comandos que ejecuta la raspberry en un fichero de texto 
# "codigoRaspberry.txt", queda como archivo temporal.
#echo "cd Desktop/TFG" > codigoRaspberry.txt
#echo "bash demo_OpenVINO.sh -a benchmark_app -t 60 $stringarray" >> codigoRaspberry.txt

#Ejecutamos código mediante ssh
#ssh pi@$HOST < codigoRaspberry.txt

#rm codigoRaspberry.txt

#########Generación de gráficas y tablas##########
#for m in ${stringarray[@]}; do
  #python3 benchmarkAnalisis.py resultado/benchmark_app/$m
#done

#python3 comparaModelos.py resultado/benchmark_app

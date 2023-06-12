#!/bin/bash

##########################################################
# Código que ejecuta medidor de consumo en una plataforma#
# Analiza el consumo básico del dispositivo, para después#
#  tenerlo en cuenta en las mediciones                   #
##########################################################

#########         Entradas           ############
# -t: Tiempo de ejecución

#Iteramos con "getopts", obteniendo opción -t
# para pasárselo al código específico de cada plataforma
while getopts t: flag; do
  case "${flag}" in
    t) t=${OPTARG};; #Tiempo
  esac
done

./Watts\ up/wattsup -c $t ttyUSB0 watts &> resultado/consumoBase.csv

#!/bin/bash 

##Este script ejecuta una aplicación de OpenModelZoo con varios modelos (es necesario el modelo principal), muesra salida por pantalla.
##También descarga y convierte los modelos si es necesario, y descarga el archivo de entrada si no existe en la ubicación especificada.

#Inicializamos las variables
app=""
input=""
comando=""

# Función para descargar los modelos si es necesario
download_models() {
  # Comprobar si el modelo ya se ha descargado
  if test -d $dirTrabajo/intel/$1 || test -d $dirTrabajo/public/$1; then
    echo "El modelo $1 ya ha sido descargado"
  else
    # Descargar el modelo
    python3 /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/downloader.py --name $1 --precisions FP16
  fi
}

# Función para convertir los modelos si es necesario
convert_models() {
  # Si el modelo es público y no se ha convertido antes
  if test -d $dirTrabajo/public/$1 && ! test -d $dirTrabajo/public/$1/FP16; then
    # Comando para convertir el modelo
    python3 /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/converter.py --name $1
  fi
}

# Cargar la configuración desde un archivo
source config.cfg

#Procesamos parámetros, y hacemos acciones necesarias
while [[ $# -gt 0 ]]; do
  #Selección de opción -a, -i, -m..
  case $1 in
      -a) app=$2; 
          shift;;  # Asignar el siguiente argumento a $app y mover la posición de los argumentos

      -i) if ! test -f $dirTrabajo/test_data/$2; then  # Verificar si el archivo de entrada ya existe
            curl $descargaDatos/$input --create-dirs -o $dirTrabajo/test_data/$2  # Descargar el archivo de entrada
          fi
          input=$dirTrabajo/test_data/$2  # Asignar la ruta completa del archivo de entrada a $input
          shift;;  # Mover la posición de los argumentos

      -m*) comando="$comando $1 $dirTrabajo/intel/$2/FP16/$2.xml"  # Agregar el argumento y la ruta completa del modelo al comando
           download_models $2  # Descargar el modelo si es necesario
           convert_models $2  # Convertir el modelo si es necesario
           shift;;  # Mover la posición de los argumentos

      *)  echo "Opción inválida: $1" >&2  # Si la opción no es válida, mostrar un mensaje de error
          exit 1  # Salir del script con código de error
          ;;
  esac
  shift  # Mover la posición de los argumentos
done

#Ejecutamos el modelo
$dirOMZ/$app -i $input $comando
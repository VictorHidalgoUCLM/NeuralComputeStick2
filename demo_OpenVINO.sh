#!/bin/bash

##Script que recibe argumentos por línea de comandos y realiza varias tareas de procesamiento de modelos utilizando la herramienta OpenVINO.
##Se procesa cada modelo, creando un directorio para los resultados y descargando y convirtiendo el modelo si es necesario.
##En caso de encontrarnos en raspberrypi, los obtenemos de otro sitio.
##Se recorre una lista de dispositivos de inferencia, se ejecuta un comando de OpenVINO en función del tipo de dispositivo y
## se analiza la salida para iniciar el medidor de consumo cuando comience la inferencia. La salida se formatea para ser utilizada por otros scripts.

# Variables para los argumentos de la línea de comandos
app=""
time=""
comando=""
models=()

# Procesar los argumentos de la línea de comandos
while getopts "a:t:" opt; do
  case $opt in
    a) app="$OPTARG";; #Nombre de la aplicación
    t) time="$OPTARG";; #Tiempo de ejecución
    \?) echo "Opción inválida: -$OPTARG" >&2; exit 1;;
    :) echo "La opción -$OPTARG requiere un argumento." >&2; exit 1;;
  esac
done

# Procesar los argumentos posicionales
shift $((OPTIND-1))

# Comprobar si se han pasado los argumentos requeridos
if [[ -z "$app" || -z "$time" || $# -eq 0 ]]; then
  echo "Faltan parámetros obligatorios. Uso: demo_OpenVINO.sh -a <app> -t <tiempo> <modelo> <...>" >&2
  exit 1
else
  models=("$@") # Almacenar los modelos en un array
fi

# Función para descargar los modelos si es necesario
download_models() {
  # Comprobar si el modelo ya se ha descargado
  if test -d $dirTrabajo/intel/$1 || test -d $dirTrabajo/public/$1; then
    echo "El modelo $1 ya ha sido descargado"
  else
    # Descargar el modelo
    python3 /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/downloader.py --name $1
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

# Si se está ejecutando en una Raspberry Pi, copiar los archivos necesarios
if [ "$dispositivo" = "raspberrypi" ]; then
  scp -r pc@192.168.1.131:/home/pc/Escritorio/TFG/intel /home/pi/Desktop/TFG
  scp -r pc@192.168.1.131:/home/pc/Escritorio/TFG/public /home/pi/Desktop/TFG
fi

# Procesar cada modelo
for model in "${models[@]}"; do
  echo "Procesando modelo $model"

  # Crear el directorio para los resultados
  mkdir -p $dirTrabajo/resultado/$app/$model

  # Si se está ejecutando en una PC, descargar y convertir el modelo
  if [ "$dispositivo" = "pc" ]; then
    echo "Descargando y convirtiendo modelo $model"
    download_models $model
    convert_models $model
  fi

  # Comprobar si el modelo está en la carpeta "public" o "intel"
  if test -d $dirTrabajo/public/$model; then
    ruta=public
  elif test -d $dirTrabajo/intel/$model; then
    ruta=intel  
  fi

  #Recorremos los dispositivos en los que queremos ejecutar
  for iterador in ${dispositivosInferencia[@]}; do
    #Ejecutamos un comando de OpenVINO en función del tipo de dispositivo al que va dirigido
    case "$iterador" in
      "CPU1")
        comando="$dirAplicaciones/$app -m $dirTrabajo/$ruta/$model/FP16/$model.xml -t $time -report_type "no_counters" -api sync -report_folder $dirTrabajo/resultado/$app/$model"
        ;;
      "CPU4")
        comando="$dirAplicaciones/$app -m $dirTrabajo/$ruta/$model/FP16/$model.xml -t $time -report_type "no_counters" -report_folder $dirTrabajo/resultado/$app/$model"
        ;;
      "MYRIAD")
        comando="$dirAplicaciones/$app -m $dirTrabajo/$ruta/$model/FP16/$model.xml -t $time -d MYRIAD -report_type "no_counters" -report_folder $dirTrabajo/resultado/$app/$model"
        ;;
      *)
        echo "Error: dispositivo no reconocido"
        exit 1
        ;;
    esac

    #Analizamos la salida de la ejecución para iniciar el medidor de consumo cuando inicie la inferencia, ignorando tiempo de carga
    $comando | while read -r line; do
      if echo "$line" | grep -w -q "Measuring performance"; then
        $dirTrabajo/Watts\ up/wattsup -c $time ttyUSB0 watts | tee $dirTrabajo/resultado/$app/$model/consumo-$iterador.csv >/dev/null
      fi
      
      if echo "$line" | grep -w -q "Dumping statistics report"; then
        echo "Terminado"
      fi
    done

    sleep 10

    #Formateamos la salida para otros scripts
    cp $dirTrabajo/resultado/$app/$model/benchmark_report.csv $dirTrabajo/resultado/$app/$model/benchmark-$iterador.csv
  done     

  rm $dirTrabajo/resultado/$app/$model/benchmark_report.csv
done

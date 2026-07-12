
# Guante Inteligente Traductor de Lengua de Signos

## Requisitos

Antes de ejecutar la aplicación es necesario disponer de:

* Python 3.14 o superior.
* Un microcontrolador Arduino Nano ESP32 programado con el firmware del proyecto.
* Un guante instrumentado con sensores de flexión y una unidad de medida inercial (IMU).
* Un ordenador con Windows.
* Conexión entre el Arduino y el ordenador mediante:

  * Cable USB (recomendado), o
  * Conexión WiFi previamente configurada.

> **Importante:** ningún otro programa (Arduino IDE, monitor serie, etc.) debe estar utilizando el puerto serie mientras se ejecuta la aplicación.

---

## Instalación

La aplicación incluye un ejecutable que automatiza la configuración del entorno.

1. Descargue el proyecto.
2. Ejecute el archivo `.exe`.
3. En la primera ejecución:

   * Se comprobará si existe un entorno virtual.
   * Si no existe, se creará automáticamente.
   * Se instalarán todas las dependencias necesarias.

Este proceso únicamente se realiza la primera vez.

---

## Puesta en marcha

1. Conecte el Arduino al ordenador mediante USB o asegúrese de que la conexión WiFi esté correctamente configurada.
2. Compruebe que todos los sensores están correctamente conectados al Arduino.
3. Ejecute la aplicación.
4. Seleccione el modo de funcionamiento deseado:

   * **Recolección de datos:** permite generar archivos CSV para crear nuevos conjuntos de datos.
   * **Traducción en tiempo real:** procesa los datos recibidos desde el guante y muestra la predicción del gesto.

---

## Recomendaciones de uso

* Ajuste correctamente el guante antes de comenzar.
* No desconecte el Arduino mientras la aplicación esté en funcionamiento.
* Evite ejecutar simultáneamente aplicaciones que utilicen el mismo puerto serie.

---

## Resolución de problemas

### No se reciben datos del Arduino

* Compruebe que el cable USB funciona correctamente.
* Verifique que ningún otro programa esté utilizando el puerto serie.
* Asegúrese de que el firmware del Arduino está cargado correctamente.

### Error relacionado con la IMU

Si la unidad de medida inercial deja de responder durante el funcionamiento, reinicie el Arduino utilizando el botón **RESET** de la placa.

### Los sensores no responden correctamente

Compruebe el estado de los cables y de las conexiones de los sensores, ya que pueden deteriorarse debido a la flexión repetida del guante.

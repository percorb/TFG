# Guion completo — Defensa TFG (palabra por palabra)

Guion corrido, diapositiva a diapositiva, siguiendo el orden real de `defensa_tfg.tex` (18 diapositivas). Tiempos orientativos para encajar en 25 minutos — la demo va al final, fuera de este reparto. Es un punto de partida: adáptalo a tu forma de hablar, no lo memorices literal.

---

### 1. Portada — 0,5 min

"Buenos días / buenas tardes. Mi nombre es David Periñán Corbacho y voy a presentar mi Trabajo de Fin de Grado: *Guante traductor de lengua de signos con Arduino*."

---

### 2. Índice — 0,5 min

"Antes de empezar, un vistazo rápido a la estructura de la presentación: motivación y objetivos, estado del arte, análisis y diseño del sistema, montaje del guante, el proceso de aprendizaje de gestos, la aplicación de escritorio, las pruebas realizadas y, para cerrar, las conclusiones."

---

### 3. Introducción — 1,5 min

"El proyecto parte de una pregunta sencilla: ¿cómo facilitar la comunicación entre quienes usan lengua de signos española y quienes no la conocen?

La propuesta es un guante inteligente que actúa de puente: capta los signos que hace la mano y los convierte en texto en tiempo real. Ese es, en una frase, el proyecto completo — un dispositivo que traduce LSE a texto."

---

### 4. Motivación y Objetivos — 2,5 min

"¿Por qué este proyecto? Hay varios colectivos para los que la lengua de signos es su medio de comunicación principal — no solo personas sordas, también, por ejemplo, personas con TEA no verbal o con parálisis cerebral. El problema es que fuera de esos colectivos, el conocimiento de la LSE es muy reducido, y eso genera una barrera real en el día a día: en una consulta médica, en una tienda, en cualquier gestión cotidiana.

El objetivo del proyecto es, precisamente, construir un guante inteligente capaz de traducir la lengua de signos española a texto en tiempo real. Y para llegar ahí hace falta cubrir todo el ciclo: diseñar y montar el hardware, generar un dataset propio —porque no existe ninguno público para LSE—, entrenar y seleccionar el modelo de machine learning más adecuado, y construir una aplicación que haga la traducción en tiempo real."

---

### 5. Estado del Arte — Hardware — 0,5 min

"Antes de entrar en mi propuesta, un repaso muy breve a qué se ha hecho hasta ahora. En cuanto a hardware, la mayoría de guantes similares combinan sensores de flexión con un IMU — normalmente un MPU6050 — montados sobre microcontroladores como ESP32, Arduino Nano o Arduino Mega. Mi propuesta sigue esa misma línea: ESP32 con sensores flex y MPU6050."

---

### 6. Estado del Arte — Software y resultados — 0,5 min

"En cuanto al software, los enfoques varían bastante: desde sistemas simples basados en umbrales fijos, hasta modelos de deep learning como CNN, BiLSTM o Transformers, pasando por modelos de machine learning más clásicos como Random Forest o KNN. Las precisiones reportadas van del entorno del 82% hasta cerca del 99%. Mi proyecto, con Random Forest, alcanza un 99,74% — lo detallo más adelante."

---

### 7. Estado del Arte — Análisis — 0,5 min

"Dos ideas se repiten en casi todos estos trabajos: primero, que la inmensa mayoría están orientados a ASL, la lengua de signos americana — apenas hay trabajos sobre LSE. Y segundo, que el hardware converge en la misma combinación: sensores flex más IMU sobre ESP32 o Arduino.

De ahí parte mi trabajo: al no existir datasets públicos para LSE, necesitaba construir el sistema completo desde cero — hardware, dataset y software."

---

### 8. Análisis y Diseño — Requisitos — 1,5 min

"Con eso claro, pasamos al diseño. Definí un conjunto de requisitos funcionales: el sistema debe capturar los datos de los sensores, almacenarlos en un dataset en formato CSV, clasificar los signos mediante machine learning, mostrar la traducción en tiempo real, y permitir la comunicación tanto por USB como por WiFi.

Y unos requisitos no funcionales: baja latencia, para que la traducción se sienta realmente en tiempo real; una interfaz gráfica intuitiva; y fiabilidad ante errores de comunicación, para que un fallo puntual de conexión no tire abajo la aplicación."

---

### 9. Análisis y Diseño — Arquitectura — 1,5 min

"La arquitectura se divide en dos partes claras. Por el lado hardware: el Arduino Nano ESP32, los sensores flex combinados con el MPU6050, y una PCB personalizada que centraliza todas las conexiones. Por el lado software: una aplicación en Python, comunicación USB o WiFi con el guante, y el modelo Random Forest como motor de clasificación.

El flujo de datos es directo: los sensores generan la señal, el ESP32 la envía al PC, el modelo Random Forest la clasifica, y el resultado se muestra como texto."

---

### 10. Montaje del Guante — Componentes — 2 min

"Entrando ya en el hardware: el guante es un guante deportivo elástico normal, sobre el que he montado cinco sensores de flexión — cuatro de 7 cm para índice, corazón, anular y meñique, y uno de 5 cm para el pulgar, que tiene un recorrido de movimiento distinto.

Como cerebro del sistema uso un Arduino Nano ESP32, que integra WiFi y Bluetooth de fábrica, así que no necesito módulos adicionales para la comunicación inalámbrica. Para el movimiento de la mano incorporo un MPU6050, que combina acelerómetro y giroscopio y se comunica por bus I2C.

Todo esto va soldado sobre una PCB propia de 3 por 5,5 centímetros que diseñé en KiCad, en lugar de dejar el cableado suelto sobre una protoboard."

---

### 11. Montaje del Guante — Sensores de flexión — 1,5 min

"¿Cómo funciona exactamente cada sensor de flexión? Cada uno forma un divisor de tensión junto con una resistencia fija de 10 kilo-ohmios. Al doblar el dedo, la resistencia del sensor cambia, lo que hace variar la tensión de salida — y esa tensión es la que el ESP32 lee por sus entradas analógicas.

¿Por qué me decidí por una PCB propia en vez de una protoboard? Por dos motivos: fiabilidad — menos cables sueltos, menos falsos contactos — y ergonomía, porque el usuario necesita mover la mano con libertad mientras hace los signos, y un cableado voluminoso lo dificulta."

---

### 12. Aprendizaje de Gestos — Dataset — 1,5 min

"Con el hardware ya montado, el siguiente paso es enseñarle al sistema a reconocer los gestos. Para eso generé un dataset propio de 4.800 muestras repartidas en 32 clases, que incluyen el alfabeto de la LSE y varios signos de palabras completas. Como comentaba antes, esto fue necesario porque no existe ningún dataset público para LSE.

Cada muestra no es una lectura instantánea, sino una ventana de 10 lecturas consecutivas, de la que extraigo 18 características — medias, desviaciones típicas, ángulos de inclinación, magnitudes de movimiento.

Con ese dataset comparé 6 algoritmos de clasificación: Random Forest, árbol de decisión, regresión logística, KNN, SVM y Naive Bayes gaussiano, todos evaluados con validación cruzada y con sus hiperparámetros optimizados."

---

### 13. Aprendizaje de Gestos — Resultados — 2,5 min

"¿Y qué resultados dieron? Random Forest fue el que mejor se comportó, con un 99,74% tanto de accuracy como de F1-score. Muy cerca quedó SVM, con un 99,44%, y la regresión logística, con un 99,31%. Por debajo, árbol de decisión y Naive Bayes rondando el 98%, y KNN algo más atrás, en torno al 96,6%.

Más allá de la precisión, me fijé también en los tiempos. Random Forest es el que más tarda en entrenar — unos 3,1 segundos —, pero eso es irrelevante en producción porque el entrenamiento se hace una sola vez, de forma offline. Lo que sí importa es el tiempo de predicción, y ahí Random Forest tarda solo 0,034 segundos por muestra — perfectamente compatible con una traducción en tiempo real.

KNN, en cambio, es el más lento prediciendo, porque en cada inferencia tiene que calcular la distancia contra todo el dataset — por eso, pese a su sencillez, lo descarté.

En conjunto, Random Forest es el que mejor equilibra precisión y coste computacional, así que es el modelo que integré en la aplicación final."

---

### 14. Aplicación de Escritorio — 2 min

"Todo este modelo se integra en una aplicación de escritorio desarrollada en Python con CustomTkinter. Tiene dos modos de uso: uno para la adquisición de datos, que es el que usé para construir el propio dataset, y otro para la traducción en tiempo real. La conexión con el guante puede hacerse por USB o por WiFi, mediante sockets TCP, a elección del usuario.

Por dentro, la aplicación usa una arquitectura multihilo, de forma que la lectura de sensores, el entrenamiento y la inferencia se ejecutan en hilos separados y no bloquean la interfaz. Además, el clasificador no se queda solo con la predicción más probable: muestra las 3 clases con mayor probabilidad, y aplica un suavizado sobre las últimas 7 predicciones para evitar que la salida "parpadee" entre signos parecidos."

---

### 15. Pruebas del Sistema — 1,5 min

"Para validar que todo esto funciona como debía, seguí una estrategia de pruebas en tres niveles: unitarias, de integración y de sistema, repitiéndolas cada vez que introducía un cambio relevante en el código.

Las pruebas unitarias, hechas con pytest, se centran en los módulos con lógica propia — la comunicación con el Arduino, el preprocesamiento de datos, el modelo Random Forest y las interfaces —, usando mocks para no depender del hardware físico en cada ejecución.

Las pruebas de sistema, tanto funcionales como no funcionales, verifican directamente el cumplimiento de los requisitos que planteé al principio — cierran el círculo entre lo que dije que iba a construir y lo que finalmente se comprobó que funciona."

---

### 16. Conclusiones — Objetivos alcanzados — 1,5 min

"Para cerrar, un resumen de lo conseguido. Tengo un guante funcional, con cinco sensores de flexión más IMU integrados sobre una PCB propia. Una aplicación de escritorio completa, con adquisición de datos y traducción en tiempo real. Un dataset propio de 4.800 muestras en 32 clases. Un modelo Random Forest seleccionado tras una comparativa rigurosa, con un 99,74% de accuracy. Y todo ello validado mediante pruebas unitarias, de integración y de sistema."

---

### 17. Conclusiones — Trabajo futuro — 1,5 min

"Como líneas de trabajo futuro, destaco cuatro: añadir salida de audio, para que el texto se pueda convertir también en voz; conseguir un despliegue autónomo en el propio microcontrolador, sin depender de un PC, junto con una app móvil por Bluetooth; avanzar hacia el reconocimiento de frases completas y no solo de signos aislados; y ampliar tanto el vocabulario como el número de usuarios que aportan datos, para mejorar la generalización del sistema a otras manos."

---

### 18. Cierre — 0,5 min

"Con esto concluyo la presentación. Creo que el proyecto demuestra que es viable traducir lengua de signos española a texto en tiempo real, con hardware de bajo coste y un modelo de machine learning clásico — y deja una base sólida sobre la que seguir trabajando en las líneas que acabo de comentar. Muchas gracias por su atención, quedo a su disposición para lo que necesiten."

---

## Después del cierre: demostración en vivo

Como la demo va al final, aquí tienes una checklist rápida antes de lanzarte:

- Ten el guante ya conectado y probado (USB o WiFi) **antes** de empezar la defensa, para no perder tiempo emparejando en directo.
- Anuncia brevemente qué vas a hacer: "Para terminar, les voy a mostrar el sistema funcionando en tiempo real" — y haz 2-3 signos representativos (algo del alfabeto y, si tienes, alguna palabra completa) para que se vea tanto la robustez como la variedad del vocabulario.
- Si algo falla en directo, no te pares a depurar delante del tribunal — coméntalo con naturalidad ("a veces la conexión WiFi tarda unos segundos") y seguí adelante o cambia a USB como plan B.

## Notas de práctica

- Este guion completo, leído con calma, ronda los 24 minutos — deja margen de 1 minuto de colchón antes de la demo.
- Practícalo en voz alta al menos 2-3 veces con cronómetro; verás rápido qué bloques te salen más largos de lo escrito y podrás recortar sobre la marcha.
- Las diapositivas de Estado del Arte (5, 6 y 7) están pensadas para pasar rápido — no te detengas a leer las tablas fila por fila, son de apoyo visual mientras hablas.

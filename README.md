# Trabajo Practico final de la materia Simulacion de Eventos Discretos 
## "Comparando Estrategias de Vacunacion con EB-DEVS"

En este repositorio se encuentra el código desarrollado durante el trabajo, el reporte final y un video de los resultados mencionados en el mismo. 

Dado que la cantidad de simulaciones realizadas durante la evaluacion son más de 7 mil, con 20 reintentos para promediar cada una, realizamos un script que ejecuta cada configuración por separado, así es posible reproducir algún comportamiento de interés y/o facilitar la extensión del trabajo con otras estrategias de vacunación y/o distribuciones de grado. 

### Como ejecutar el trabajo

Es un requerimiento del proyecto la instalación de EB-DEVS, descripta en EB-DEVS-README.md

Cada configuracion de estrategia, distribucion y parametros se puede ejecutar mediante el comando:

`python3 experiment.py {*vaccination_strategy*} {*graph_distribution*} {*vaccination_parameters*}`

En el código por defecto se encuentran las siguientes estrategias, distribuciones y parámetros:

|vaccination_strategy | Descripción|
| ----------- | ----------- |
| `default_strategy` | los agentes se vacunan con intensidad exponencial con media definida en la distribucion de grado |
| `degree_based_strategy` | los agente se vacunan con intensidad exponencial con media en su grado asignado |
| `double_degree_based_strategy` | los agente se vacunan con intensidad exponencial con media en una exponencial con media en su grado asignado |
| `triple_degree_based_strategy` | los agente se vacunan con intensidad exponencial con media en una exponencial con media con media en una exponencial con media en su grado asignado |



|graph_distribution | Descripción| Media | Tamaño del grafo |
| ----------- | ----------- | ----------- | ----------- |
| `bimodal` | El grafo tiene distribución de grado bimodal con probabilidad 4/5 Poisson(3), y 1/5 grado 13 | 5.0 | 300 | 
| `regular_5` | Todos los agentes tienen grado 5 | 5.0 | 300 |
| `poisson_5` | Los agentes tienen una distribución de grado Poisson 5 | 5.0 | 300 | 
| `power_law` | Los agentes siguen una distribución Power Law (con parametros explicados en el reporte)| 5.0 | 300 |



|vaccination_parameters | Descripción|
| ----------- | ----------- |
| `vaccine_factors_100` | ejecuta la simulacion con 100 factores de escala linealmente espaciados entre [0.001,0.5], sin límite de vacunas disponibles |
| `vaccine_factors_100_10` | ejecuta la simulacion con 100 factores de escala linealmente espaciados entre [0.001,0.5], con límite de vacunas disponibles en 10% de la población |
| `vaccine_factors_100_25` | ejecuta la simulacion con 100 factores de escala linealmente espaciados entre [0.001,0.5], sin límite de vacunas disponibles en 25% de la población |
| `vaccine_factors_100_50` | ejecuta la simulacion con 100 factores de escala linealmente espaciados entre [0.001,0.5], sin límite de vacunas disponibles en 50% de la población |


### Resultados
Cada simulación produce sus resultados dentro de la carpeta `results/` en un archivo .png que sigue el siguiente formato:
  `{distribution}_{strategy}_{factors}.png`


Por ejemplo el comando:
  `python3 experiment.py double_degree_based_strategy power_law vaccine_factors_100_50`

Producirá 100 archivos en `results/` de la pinta:
  `results/power_law_double_degree_based_strategy_s=0.001_limit=0.50.png`

Dado que es complejo evaluar y comparar estos resultados a simple vista, realizamos videos que muestran frame a frame la variación de los parámetros de escala de cada distribución, y estrategia. Para ello ejecutamos el siguiente script con la tool `ffmpeg`

`ffmpeg -framerate 1/0.5 -pattern_type glob -i 'results/power_law_default_strategy_s=0.*_limit=0.50.png' -c:v libx264 -r 30 -pix_fmt yuv420p power_law_0.50_default.mp4`

Luego a su vez es posible integrar hasta 4 videos sincronizadamente (como lo estan los videos reportados en el archivo results-videos.zip), mediante el comando 

`ffmpeg -i power_law_0.50_default.mp4 -i power_law_0.50_1.mp4    -i power_law_0.50_2.mp4  -i power_law_0.50_3.mp4  -filter_complex \                                   
"[0:v]pad=iw:ih+3[tl]; \
 [tl][1:v]vstack,pad=iw+10:ih[l]; \
 [2:v]pad=iw:ih+3[tr]; \
 [tr][3:v]vstack[r]; \
 [l][r]hstack" \
power_law_0.50-all-strategies.mp4`








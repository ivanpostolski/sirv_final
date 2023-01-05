# This is a final project of a course of discrete simulations   
## "Comparing vaccination strategies using EB-DEVS"

In this repository we condense the simulation code, report and generated media (videos) of the simulations. Given that the amount of simulations run are over 7 thousand, each with 20 retries to average results, we made an script to run each simulation configuration separately. In this way is possible to reproduce certain behaviours of interest and/or extend the current work with different vaccination strategies. 

### How to run

Requirements: install EB-DEVS, as explained in EB-DEVS-README.md

Each strategy configuration, graph distribution and parameters is executed by using the following command:

`python3 experiment.py {*vaccination_strategy*} {*graph_distribution*} {*vaccination_parameters*}`

We provide ootb the following strategies, distributions and parameters: 

|vaccination_strategy | Description |
| ----------- | ----------- |
| `default_strategy` | agents get vaccinated following an exponential distribution with mean equal to the degree distribution mean  |
| `degree_based_strategy` | agents get vaccinated following an exponential with mean equal to their connection degree |
| `double_degree_based_strategy` | agents get vaccinated following an exponential with mean equal to an exponential with mean equal to their connection degree |
| `triple_degree_based_strategy` | agents get vaccinated following an exponential with mean equal to an exponential with mean equal to an exponential with mean equal to their connection degree |



|graph_distribution | Description | Mean | Graph Size |
| ----------- | ----------- | ----------- | ----------- |
| `bimodal` | The graph follows has a degree distribution that is bimodal, 4/5 Poisson(3) and 1/5 fixed degree 13 | 5.0 | 300 | 
| `regular_5` | Every agent have degree 5 | 5.0 | 300 |
| `poisson_5` | Agents follow a Poisson distribution with mean 5 | 5.0 | 300 | 
| `power_law` | Agents follow a Power Law distribution (parameters further explained at the attached report)| 5.0 | 300 |



|vaccination_parameters | Description |
| ----------- | ----------- |
| `vaccine_factors_100` | runs the simulation with 100 scale factors linearly spaced between [0.001,0.5], w/o vaccination limit |
| `vaccine_factors_100_10` | runs the simulation with 100 scale factors linearly spaced between [0.001,0.5], with a vaccination limit set at 10% of the overall population size |
| `vaccine_factors_100_25` | runs the simulation with 100 scale factors linearly spaced between [0.001,0.5], with a vaccination limit set at 25% of the overall population size |
| `vaccine_factors_100_50` | runs the simulation with 100 scale factors linearly spaced between [0.001,0.5], with a vaccination limit set at 50% of the population size |

### File descriptions

--`experiment.py` provides the main entrypoint to run experiments

-- `model.py`  has the EB-DEVS model made to simulate a vaccination strategy

-- `vaccination_strategies.py` provided vaccination strategies and degree distributions

-- `TP.pdf` overall work report (in spanish), with detailed motivation, and relevant findings from the simulations 

-- `results-videos.zip` resulting simulation videos in .mp4 format 


### Results
Each simulation places their output into the  `results/` folder, within a .png file with the following naming format  
  `{distribution}_{strategy}_{factors}.png`

For instance, the command
  `python3 experiment.py double_degree_based_strategy power_law vaccine_factors_100_50`

Will produce 100 files in `results/`, that would look like:
  `results/power_law_double_degree_based_strategy_s=0.001_limit=0.50.png`

Given that is complex to assess and compare these results at plain sight, we collapse these results in a video where each frame represents a variation of the scale factor parameter, and strategy. To build these videos we use the `ffmpeg` tool, as the following script: 

`ffmpeg -framerate 1/0.5 -pattern_type glob -i 'results/power_law_default_strategy_s=0.*_limit=0.50.png' -c:v libx264 -r 30 -pix_fmt yuv420p power_law_0.50_default.mp4`

Then it is possible to integrate up to 4 videos sincronized, to watch different strategies at the same time. Using the following script.

`ffmpeg -i power_law_0.50_default.mp4 -i power_law_0.50_1.mp4    -i power_law_0.50_2.mp4  -i power_law_0.50_3.mp4  -filter_complex \                                   
"[0:v]pad=iw:ih+3[tl]; \
 [tl][1:v]vstack,pad=iw+10:ih[l]; \
 [2:v]pad=iw:ih+3[tr]; \
 [tr][3:v]vstack[r]; \
 [l][r]hstack" \
power_law_0.50-all-strategies.mp4`



# Trabajo Práctico final de la materia Simulación de Eventos Discretos 
## "Comparando Estrategias de Vacunacion con EB-DEVS"

En este repositorio se encuentra el código desarrollado, el reporte y videos de las simulaciones mencionados en el mismo, para el trabajo final de la materia [Simulación de Eventos Discretos](https://modsimu.exp.dc.uba.ar/sed/index.php) de la Universidad de Buenos Aires.

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

### Detalle de Archivos Relevantes

--`experiment.py` contiene la api para correr experimentos

-- `model.py`  contiene el modelo EB-DEVS desarrollado para simular las distintas estrategias de vacunación

-- `vaccination_strategies.py` estrategias de vacunación propuestas y distribuciones de grado

-- `TP.pdf` reporte general del trabajo, con detalle sobre la motivación, y los hallazgos obtenidos a partir de las simulaciones 

-- `results-videos.zip` los resultados de las simulaciones en videos .mp4 


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








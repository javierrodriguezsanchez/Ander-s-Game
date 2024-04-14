# Estrategias para guerras medievales: El juego de Ander

En un contexto medieval, donde hay n reinos en guerra, se busca saber cual es la mejor estrategia a seguir por los reyes para salir victoriosos. En este contexto, para evitar conflictos historicos o culturales, lo desarrollaremos en una tierra lejana llamada Ander, donde existen n reinos anonimos.

# Sistema

Un reino consta de un rey, el pueblo al que gobierna, su castillo/fortaleza y un ejercito. Los reinos todos inician en guerra por conveniencia. Un reino puede mejorar sus murallas o aumentar su ejercito. Pueden atacar o aliarse a otros reinos, el objetivo de cada uno es salir airoso de la pelea.

### Modelo usado

El modelo usado para representar el sistema consiste en un accionar por turnos de cada reino. La poblacion estara clasificada segun que tan grande es (dado por niveles del 0 al 10) y su castillo/muralla tendra un indice de fortaleza. El ejercito estara dividido en tropas cada una con un tamaño. La poblacion de un reino asumimos que esta en constante cambio, y todos los turnos variara en tamaño, con mayor probabilidad de permanecer cerca del valor anterior. Durante un turno los reyes pueden ordenar a su poblacion a reforzar sus murallas o a reclutar tropas, segun permita el tamaño del pueblo; y ordenar a sus tropas a atacar otros reinos. Para destruir un reino debes matar a su rey. Para esto primero hay que destruir su ejercito, luego sus murallas, luego su pueblo y finalmente ordenar matarlo. Si dos tropas pelean, la mas fuerte gana, pero pierde en fuerza igual al nivel de la tropa destruida. Si una tropa ataca una muralla, la muralla resiste, pero pierde resistencia igual a la mitad del nivel de la tropa que la asedia. Si un pueblo es atacado por una tropa, este quedara diezmado en una cantidad igual al nivel de la tropa.

Los reyes consistiran en agentes, los cuales contienen conocimiento basico de como manejar a su reino y el estado actual de este y de los reinos enemigos en todo momento. Ademas, cada rey tiene niveles de relacion con el resto de los reinos, los cuales inician siendo malos con todo, pero dichas relaciones pueden mejorar. Un rey solo conoce la relacion que tienen otros con el y las relaciones no son simetricas. Entre las cosas que afectan una relacion esta: entrar en alianza(aumento grande), que ataquen a un enemigo(aumento minimo), que ataquen a un aliado(disminucion minima) recibir ataque a una tropa(disminucion estandar), recibir ataque a la muralla(disminucion alta),  recibir ataque al pueblo(disminucion enorme), ser traicionado(disminucion maxima). Dos reinos pueden entrar en una alianza, la cual queda como un pacto de no agresion por 3 turnos. Una traicion ocurre cuando un aliado ataca a otro.

Las decisiones sobre la alianza y que acciones seran tomadas en un turno, conforman la estrategia que sigue un rey. El objetivo de nuestro modelo es encontrar la mejor estrategia.

### Ventajas del modelo utilizado

Modelo simple y escalable a todos los niveles. Permite dar gran diversidad de estrategias a probar en un gran numero de condiciones iniciales.

### Limitaciones y desventajas

Las decisiones de los reinos no se realizan en tiempo real, lo cual afecta el realismo del modelo y no toma en cuenta la velocidad de la toma de decision, factor crucial en una guerra. La ausencia de mapa y de recursos tambien hace que no se tomen en cuenta costos de ataque un reino o fortalecimiento de las murallas. El conocimiento de los estados de los reinos ajenos no es realista, ya que en el sistema el conocimiento de los reyes suele ser limitado. Una tropa numericamente superior no siempre es la que sale victoriosa de un combate, quitandole lugar a la incertidumbre. El caracter centralizado de los reinos tambien es una suavizacion del problema, haciendo que todas las ordenes de este se ejecuten, y no hayan controversias internas.

### Aspectos mejorables

Los siguientes aspectos no fueron incluidos en el modelo por falta de tiempo, pero son perfectamente integrables:

- La adicion de capacidades especiales: cada reino tendria una capacidad extra y distintiva que le permitiera distinguirse del resto de los reinos (se pudiera ver como cierta tecnologia que contengan, una especie de arte marcial, un don divino o una raza), que le permita extender las reglas establecidas y otorgarles cierta ventaja.

- La comunicacion entre aliados: en una alianza, un rey puede recomendarle a un aliado suyo que acciones realizar en su turno, y decidir que hacer auxiliado ademas basado en las sugerencias de los aliados

# Implementacion

El codigo de la aplicacion que permite la simulacion se encuentra en la carpeta src.

### Modelo:

Todas las descripciones y la logica de un reino se encuentra en la clase Kingdom en el archivo Simulation_Model/Reigns.py. De aqui vale la pena destacar el metodo actions, el cual devuelve una lista con todas las ordenes inmediatas que puede dar un rey, y la clase act, que dado una accion la ejecuta. La clase esta diseñada de tal manera de que pueda ser extensible para agregar nuevas funcionalidades al modelo en caso de ser necesario.

### Agente:

Los agentes del modelo serian los reyes, y estan representados en la clase Agent/Agent.py. Estos contienen como propiedad una base de conocimientos simple, representada en Agent/Knowledge_Base.py.

### Base de Conocimientos de los agentes

Esta cuenta con dos metodos fundamentales: Learn y Think. El primero permite al agente guardar toda aquella informacion que sea util para este, como la estrategia que seguiran, el numero de reinos y la informacion de estos, el estado actual de la geopolitica y las acciones realizadas por otros reinos. El segundo permite a un agente tomar sus decisiones dado su conocimiento, como las acciones que realizara durante su turno, sus consecuencias inmediatas y con que reinos aliarse.

### Toma de decisiones:

Las decisiones de un rey consistiran en una busqueda informada de cual seria el mejor camino para su reino, donde buscaria entre todos los posibles finales cuales son los que mas le conviene seguir, de esta forma, este elige cual seria las decisiones obtimas en funcion de su estrategia.

### Estrategias de un agente

Un agente tiene una estrategia, y nuestro objetivo es encontrar la mas conveniente. Todas estas estrategias se encuetran en la carpeta Strategies y heredan de la clase Strategy en Strategies/Strategy.py. Y permite implementar la toma de decision a su forma.

### Simulador

<p style="color: red">Chamacho, todo tuyo</p>

### LLM

Para un mejor analisis de los resultados, utilizamos LLM para resumir el historial del juego y crear una historia mas amena y legible en vista la interpretacion de las decisiones tomadas por los agentes, y entender que decidieron hacer y en que contexto. Dando la facilidad de tener una idea del desarrollo de la simulacion.

<p style="color: red">Camacho, te la deje servida</p>

# Analisis de las simulaciones realizadas

Volviendo a la pregunta inicial: cual es la mejor estrategia. Para saber esto, buscamos resolverlo inicialmente para el caso n=2, n=3, n=4. Y las estrategias usadas fueron las siguientes:

<p style="color: red">Luis todo tuyo</p> 

### Resultados obtenidos para n=2

Se realizaron simulaciones haciendo todos los posibles emparejamientos entre pares de estrategias. Cada par se enfrentará 20 veces, 10 veces saliendo uno de primero y las otras 10 se invierte el orden. En este caso es importante analizar ambos resultados ya que al ser solo 2 reinos, el primero que mueve tiene una ligera ventaja sobre el otro. Estos fueron los resultados de las simulaciones:

| Reino 1 | Reino 2 | Resultado |
| :-------: | :-------: | :-------------: |
| Allies | Always Attack | 4 - 6 |
| Always Attack | Allies | 8 - 2 |
| Allies | Attack Weak | 3 - 7 |
| Attack Weak | Allies | 6 - 4|
| Allies | Current Situation | 9 - 1 |
| Current Situation | Allies | 2 - 8 |
| Allies | Defend | 10 - 0 |
| Defend | Allies | 3 - 7 |
| Allies | Do Nothing | 10 - 0 |
| Do Nothing | Allies | 0 - 10 |
| Allies | Focus | 6 - 4 |
| Focus | Allies | 7 - 3 |
| Allies | Random | 8 - 2 |
| Random | Allies | 3 - 7 |
| Always Attack | Attack Weak | 7 - 3 |
| Attack Weak | Always Attack | 7 - 3 |
| Always Attack | Current Situation | 7 - 3 |
| Current Situation | Always Attack | 5 - 5 |
| Always Attack | Defend | 9 - 1 |
| Defend | Always Attack | 4 - 6 |
| Always Attack | Do Nothing | 10 - 0 |
| Do Nothing | Always Attack | 0 - 10 |
| Always Attack | Focus | 8 - 2 |
| Focus | Always Attack | 7 - 3 |
| Always Attack | Random | 10 - 0 |
| Random | Always Attack | 1 - 9 |
| Attack Weak | Current Situation | 8 - 2 |
| Current Situation | Attack Weak | 3 - 7 |
| Attack Weak | Defend | 9 - 1 |
| Defend | Attack Weak | 3 - 7 |
| Attack Weak | Do Nothing | 10 - 0 |
| Do Nothing | Attack Weak | 0 - 10 |
| Attack Weak | Focus | 5 - 5 |
| Focus | Attack Weak | 6 - 4 |
| Attack Weak | Random | 10 - 0 |
| Random | Attack Weak | 2 - 8 |
| Current Situation | Defend | 9 - 1 |
| Defend | Current Situation | 1 - 9 |
| Current Situation | Do Nothing | 10 - 0 |
| Do Nothing | Current Situation | 0 - 10 |
| Current Situation | Focus | 3 - 7 |
| Focus | Current Situation | 5 - 5 |
| Current Situation | Random | 8 - 2 |
| Random | Current Situation | 5 - 5 |
| Defend | Do Nothing | 10 - 0 |
| Do Nothing | Defend | 0 - 10 |
| Defend | Focus | 2 - 8 |
| Focus | Defend | 9 - 1 |
| Defend | Random | 5 - 5 |
| Random | Defend | 6 - 4 |
| Do Nothing | Focus | 0 - 10 |
| Focus | Do Nothing | 10 - 0 |
| Do Nothing | Random | 0 - 10 |
| Random | Do Nothing | 10 - 0 |
| Focus | Random | 9 - 1 |
| Random | Focus | 3 - 7 |

**Resumen:**

En total se realizaron 560 simulaciones. Cada estrategia participa en 140, de ellas, 70 saliendo de 1ro y 70 de 2do.

| # | Estrategia | Ganadas como 1ro | Ganadas como 2do | Total |
| :----: | :----: | :----: | :----: | :----: |
| 1 | Attack Weak | 55 | 46 | 101 |
| 2 | Always Attack | 59 | 42 | 101 |
| 3 | Focus | 53 | 43 | 96 |
| 4 | Allies | 50 | 41 | 91 |
| 5 | Current Situation | 40 | 35 | 75 |
| 6 | Random | 30 | 20 | 50 |
| 7 | Defend | 28 | 18 | 46 |
| 8 | Do Nothing | 0 | 0 | 0 |


### Resultados obtenidos para n=3

De forma similar al caso anterior se hicieron simulaciones con cada posible trío de estrategias (20 simulaciones con cada uno) para probar su efectividad en todos los escenarios posibles. La diferencia es que esta vez no consideramos todos los órdenes posibles de salida principalmente para no tener un número excesivo de simulaciones, para esto hicimos que antes de cada simulación se eligiera el orden de los turnos de manera aleatoria, es decir, en las 20 simulaciones de un trio de estrategias estas tienen un orden aleatorio, lo que nos permite hacer un análisis más general. Estos fueron los resultados:

| Reino 1 | Reino 2 | Reino 3 | Resultado |
| :-------: | :-------: | :-------: | :-------:|
| Allies | Always Attack | Attack Weak | 7 - 6 - 7 |
| Allies | Always Attack | Current Situation | 10 - 5 - 5 |
| Allies | Always Attack | Defend | 8 - 7 - 5 |
| Allies | Always Attack | Do Nothing | 6 - 14 - 0 |
| Allies | Always Attack | Focus | 6 - 7 - 7 |
| Allies | Always Attack | Random | 6 - 11 - 3 |
| Allies | Attack Weak | Current Situation | 11 - 6 - 3 |
| Allies | Attack Weak | Defend | 6 - 9 - 5 |
| Allies | Attack Weak | Do Nothing | 8 - 12 - 0 |
| Allies | Attack Weak | Focus | 5 - 11 - 4 |
| Allies | Attack Weak | Random | 7 - 8 - 5 |
| Allies | Current Situation | Defend | 7 - 6 - 7 |
| Allies | Current Situation | Do Nothing | 13 - 7 - 0 |
| Allies | Current Situation | Focus | 5 - 3 - 12 |
| Allies | Current Situation | Random | 11 - 6 - 3 |
| Allies | Defend | Do Nothing | 12 - 8 - 0 |
| Allies | Defend | Focus | 6 - 6 - 8 |
| Allies | Defend | Random | 7 - 11 - 2 |
| Allies | Do Nothing | Focus | 10 - 0 - 10 |
| Allies | Do Nothing | Random | 16 - 0 - 4 |
| Allies | Focus | Random | 6 - 9 - 5 |
| Always Attack | Attack Weak | Current Situation | 9 - 8 - 3 |
| Always Attack | Attack Weak | Defend | 9 - 8 - 3 |
| Always Attack | Attack Weak | Do Nothing | 15 - 5 - 0 |
| Always Attack | Attack Weak | Focus | 8 - 6 - 6 |
| Always Attack | Attack Weak | Random | 7 - 10 - 3 |
| Always Attack | Current Situation | Defend | 9 - 7 - 4 |
| Always Attack | Current Situation | Do Nothing | 14 - 6 - 0 |
| Always Attack | Current Situation | Focus | 9 - 4 - 7 |
| Always Attack | Current Situation | Random | 13 - 7 - 0 |
| Always Attack | Defend | Do Nothing | 13 - 7 - 0 |
| Always Attack | Defend | Focus | 5 - 8 - 7 |
| Always Attack | Defend | Random | 11 - 7 - 2 |
| Always Attack | Do Nothing | Focus | 9 - 0 - 11 |
| Always Attack | Do Nothing | Random | 13 - 0 - 7 |
| Always Attack | Focus | Random | 10 - 6 - 4 |
| Attack Weak | Current Situation | Defend | 10 - 7 - 3 |
| Attack Weak | Current Situation | Do Nothing | 17 - 3 - 0 |
| Attack Weak | Current Situation | Focus | 7 - 6 - 7 |
| Attack Weak | Current Situation | Random | 11 - 4 - 5 |
| Attack Weak | Defend | Do Nothing | 12 - 8 - 0 |
| Attack Weak | Defend | Focus | 10 - 4 - 6 |
| Attack Weak | Defend | Random | 15 - 1 - 4 |
| Attack Weak | Do Nothing | Focus | 7 - 0 - 13 |
| Attack Weak | Do Nothing | Random | 16 - 0 - 4 |
| Attack Weak | Focus | Random | 13 - 5 - 2 |
| Current Situation | Defend | Do Nothing | 12 - 8 - 0 |
| Current Situation | Defend | Focus | 6 - 5 - 9 |
| Current Situation | Defend | Random | 5 - 11 - 4 |
| Current Situation | Do Nothing | Focus | 7 - 0 - 13 |
| Current Situation | Do Nothing | Random | 12 - 0 - 8 |
| Current Situation | Focus | Random | 7 - 11 - 2 |
| Defend | Do Nothing | Focus | 6 - 0 - 14 |
| Defend | Do Nothing | Random | 12 - 0 - 8 |
| Defend | Focus | Random | 8 - 9 - 3 |
| Do Nothing | Focus | Random | 0 - 17 - 3 |

**Resumen:**

Se realizaron en total 1120 simulaciones, cada estrategia participa en 420.

| # | Estrategia | Victorias | 
| :------: |:-------: | :-------: | 
| 1 | Attack Weak | 208 |
| 2 | Always Attack | 204 |
| 3 | Focus | 191 |
| 4 | Allies | 173 |
| 5 | Defend | 137 |
| 6 | Current Situation | 126 |
| 7 | Random | 81 |
| 8 | Do Nothing | 0 |

### Resultados obtenidos para n=4


### Analisis de los resultados

# Conclusiones
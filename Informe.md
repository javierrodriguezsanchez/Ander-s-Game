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


### Resultados obtenidos para n=3


### Resultados obtenidos para n=4


### Analisis de los resultados

# Conclusiones
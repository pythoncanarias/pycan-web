## Cómo contribuir a este proyecto

Si quieres contribuir a este proyecto, hay muchas cosas que puedes hacer.
Tenemos una etiqueta en los _issues_ del [repositorio de este
proyecto](https://github.com/pythoncanarias/pycan-web/issues) para 
[aquellas tareas que pensamos que son un buen punto de partida](https://github.com/pythoncanarias/pycan-web/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
para empezar a contribuir
al desarrollo.

Además de las tareas propias de desarrollo, hay muchas otras formas de ayudar,
una de las principales es aportar nuevas ideas para mejorar la web, así
como avisarnos de cualquier error que encuentres en la misma.

Para contribuir como desarrollador, en el documento [README.md](README.md) se
explica como montar un entorno de desarrollo propio unsado _Docjer_ y
_Docker Compose_.

## Notas para los desarrolladores

El desarrollo consiste en una aplicación Django, y algunas partes de _frontend_
escritas en _javascript_ plano. Por el momento no nos hemos decidido a usar
ningún _framework_, aunque algunos del equipo tenemos una cierta preferencia
por [vue.js](https://vuejs.org/).

Se ha intentado seguir en lo posible las practicas habituales en Django, pero
en algunos casos se han realizado algunas modificaciones sobre lo que podría
ser un proyecto Django _estándar_. Explicaremos estas divergencias en las
siguientes secciones.

### Todas las aplicaciones están en la carpeta `apps`

Como hay muchas aplicaciones o _apps_, se trasladaron todas a una única
carpeta `apps`, para reducir la cantidad de _ruido_ que se encontraba en
la carpeta raíz. Si crees necesario añadir una nueva _app_, créala por favor al
mismo nivel que las actuales.

### Estilo de código

Intentamos adaptarnos lo más posible a la recomendaciones del
[PEP-8](https://www.python.org/dev/peps/pep-0008/), pero somos más flexibles en
el tema de la longitud de caracteres de la linea, intentamos mantenerlo por
debajo de 96 caracteres por línea.

Algunos de nosotros usamos la herramienta [black](https://github.com/psf/black)
para formatear el código, pero no se considera obligatorio.

### Dependecias

Intentamos mantener el número de dependencias bajo. Un alto número de
dependencias frena las actualizaciones generales, que es un objetivo que
queremos mejorar. Eso no significa que no se acepten nuevas dependencias, pero
si pedimos que analices primero si las ventajas de usar esa nueva librería
realmente nos aportan una funcionalidad importante.

### Mantener la lógica de negocio fuera de los modelos y de las vistas

Intentamos (Pero no siempre conseguimos) mantener el código de los modelos y de
las vistas lo más sencillo y directo posible. Mantenemos la idea de que es
preferible tener las reglas de negocio y el código más importante en ficheros
de servicios aparte, donde un fichero de servicios es simplemente un fichero
Python en el que se incorpora todo el código relativo a un dominio o
aplicación.

### Asigna nombres únicos a ficheros, clases y funciones

Excepción hecha de los nombres de las variables locales a funciones y métodos,
cada entidad con nombre en nuestro código debería tener un nombre único.

Hay muchas razones para esto, pero veamos por ejemplo las clases. Si nos
encontramos con una nueva clase mientras examinamos el código, lo deseable es
que una búsqueda o un _grep_ por el nombre de la clase nos devuelva será la
definición y los usos de la misma. Cualquier otra cosa que aparezca será ruido.
Si tengo dos clases con el mismo nombre en ficheros diferentes, esto solo
complica el entender en que contextos y de que forma se usa cada una de las
clases. Razones similares se pueden argumentar para las funciones, métodos
(Excepto en casos de herencia, claro) y variables o constantes globales.

### Preferimos funciones antes que clases

En general, recomendamos usar funciones para las vistas, mejor que vistas
basadas en clases. En ningún caso debe entenderse esta recomendación como una
prohibición de usar _CBV_, Es solo que preferimos usarlas para casos sencillos
y/o triviales, y usar funciones para todo lo demás. 

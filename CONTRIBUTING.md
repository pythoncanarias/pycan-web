## Contribuyendo a este proyecto

Si quieres contribuir a este proyecto, hay muchas cosas que puedes hacer.
Tenemos una etiqueta en los _issues_ del [repositorio de este
proyecto](https://github.com/pythoncanarias/pycan-web/issues) para
[aquellas tareas que pensamos que son un buen punto de partida](https://github.com/pythoncanarias/pycan-web/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
para empezar a contribuir
al desarrollo.

Si es la primera vez que vas a contribuir a un proyecto de _software_ libre,
quizá te sea de ayuda este documento: [cómo hacer tu primera contribución a
Python Canarias](docs/first-contrib.md).

Además de las tareas propias de desarrollo, hay muchas otras formas de ayudar,
una de las principales es aportar nuevas ideas para mejorar la web, así
como avisarnos de cualquier error que encuentres en la misma. Esto lo puedes hacer creando un nuevo _issue_ [en la sección correspondiente de GitHub](https://github.com/pythoncanarias/pycan-web/issues).

Para contribuir como desarrollador/a, hemos preparado un manual donde se explica [cómo montar un entorno de desarrollo](docs/dev.md) propio usando _Docker_ y _Docker Compose_.

## Sobre el idioma a usar en este proyecto

Estamos trabajando para definir los idiomas a usar en las distintas partes del
proyecto, ya que ahora mismo hay una mezcla un poco aberrante entre inglés y
español. Nuestro objetivo es ir migrando toda la documentación del proyecto a
español, y reservar el inglés solo para las cuestiones que atañan al código
directamente.

Por tanto, si quieres aportar en las secciones de documentación, aunque
encuentres el texto en inglés, puedes incluir lo nuevo en español, ya que la
idea es ir traduciendo todos esos documentos hasta conseguir el estado mostrado
en la siguiente tabla:

| Área                  | Idioma |
| --------------------- | ------ |
| Variables en código   | 🇬🇧     |
| Comentarios en código | 🇬🇧     |
| _Commits_             | 🇬🇧     |
| README                | 🇪🇸     |
| Documentación         | 🇪🇸     |
| _Issues_              | 🇪🇸     |
| Etiquetas de _issues_ | 🇪🇸     |
| _Pull Requests_       | 🇪🇸     |
| Texto de la web       | 🇪🇸     |

## Notas para desarrolladores

El desarrollo consiste en un proyecto Django, y algunas partes de _frontend_
escritas en _javascript_ plano. Por el momento no nos hemos decidido a usar
ningún _framework_, aunque algunos del equipo tenemos una cierta preferencia
por [vue.js](https://vuejs.org/).

Se ha intentado seguir en lo posible las [buenas prácticas habituales de Django](https://django-best-practices.readthedocs.io/en/latest/), pero
en algunos casos se han realizado modificaciones sobre lo que podría
considerarse un proyecto Django _estándar_. Explicaremos estas divergencias en las
siguientes secciones.

### Organización de código de las aplicaciones de Django

Como hay muchas aplicaciones o _apps_, las tenemos todas todas bajo una única
carpeta `apps`, para reducir la cantidad de _ruido_ en
la carpeta raíz. Si crees necesario añadir una nueva _app_, [lee este documento con atención](docs/new-app.md).

### Estilo de código

Intentamos adaptarnos lo más posible a la recomendaciones del
[PEP-8](https://www.python.org/dev/peps/pep-0008/), pero somos más flexibles en
el tema de la longitud de caracteres de la línea, intentamos mantenerlo por
debajo de 96 caracteres por línea.

Algunos de nosotros usamos la herramienta [black](https://github.com/psf/black)
para formatear el código, pero no se considera obligatorio.

Así mismo, existen herramientas como [flake8](https://flake8.pycqa.org/en/latest/) que detectan divergencias del estilo de código frente a los estándares establecidos.

### Dependencias

Intentamos mantener el número de dependencias bajo. Un alto número de
dependencias frena las actualizaciones generales, que es un objetivo que
queremos mejorar. Eso no significa que no se acepten nuevas dependencias, pero
sí que pedimos que analices primero si las ventajas de usar esa nueva librería
realmente nos aportan una funcionalidad importante.

### Separación entre lógica de negocio, modelos y vistas

Intentamos (pero no siempre conseguimos) mantener el código de los modelos y de
las vistas lo más sencillo y directo posible. Mantenemos la idea de que es
preferible tener las reglas de negocio y el código más importante en ficheros
de servicios aparte, donde un fichero de servicios es simplemente un fichero
Python en el que se incorpora todo el código relativo a un dominio o
aplicación.

Veamos, por ejemplo, la _app_ `notice`, que se usa para enviar notificaciones
a los miembros ante determinados eventos, como por ejemplo el aviso un mes
antes de que se venza su permanencia a la organización.

En la clase `apps.notice.models.Notice` se definen algunos métodos, pero
solo aquellos que afectan o cambian el estado del propio modelo, sin
ninguna tercera parte implicada. En concreto, no existe un método
para enviar la notificación en sí.

Este acto de enviar la notificación está implementado por separado, dentro del
módulo `apps.notica.tasks`, primero porque es relativamente complejo y segundo,
e incluso más importante, porque involucra a más elementos que el `notice` en
cuestión: implica saber de la existencia de un sistema de colas, del subsistema
de envío de mensajes ([sendgrid](https://sendgrid.com/) en nuestro caso), etc.

En resumen, se recomienda que las clases definan métodos unicamente para
consultar o cambiar su estado interno, pero que cualquier interacción con
otras clases o componentes debe realizarse fuera de la clase, preferiblemente
en un módulo aparte.

### Asigna nombres únicos a las clases

Hay muchas razones para esto, pero veamos solo una. Si nos encontramos con una
nueva clase mientras examinamos el código, lo deseable es que una búsqueda o un
_grep_ por el nombre de la clase nos devuelva solo la definición y los usos de
la misma. Cualquier otra cosa que aparezca será ruido. Si tengo dos clases con
el mismo nombre en ficheros diferentes, esto solo complica el entender en que
contextos y de que forma se usa cada una de las clases. Razones similares se
pueden argumentar para las variables o constantes globales.

De la misma forma que no existe en español dos sinónimos que signifiquen
_exactamente_ lo mismo (Siempre hay algún matiz que los diferencia) no deberían
existir en nuestro programa dos clases que se llamen exactamente iguales,
porque, si fuera así, ¿por qué no son la misma?

Tenemos ahora mismo en nuestro código un ejemplo de dos clases con el mismo
nombre, la clase `Membership` en `organization.models` y la clase
`Membership` en el módulo `members.models`. Es verdad que el programa
funciona, porque las clases están aisladas en sus propios módulos, pero hubiera
sido preferible haber buscado otro nombre que no estuviera en conflicto con uno
ya existente (`@jileon`: Yo lo sé bien ya que fui yo el que creó la clase
duplicada).

### Funciones vs clases para vistas

Para las vistas, preferimos, en general, usar funciones en vez de vistas
basadas en clases. En ningún caso debe entenderse esta recomendación como una
prohibición de usar _CBV_, es solo que preferimos usarlas para casos sencillos
y/o triviales, y usar funciones para todo lo demás.

### Nombres de ramas y commits

A la hora de crear una rama para contribuir en este proyecto hemos de seguir
la nomenclatura propuesta. Para una tarea como
["[389]Añadir un blog"][add-blog-issue] tendremos que crear la rama de la
siguiente forma `git checkout -b 389-add-blogs`. Es decir, ponemos como primera
parte el número de la issue, luego el nombre en el idioma que más cómodo nos sea.

[add-blog-issue]:https://github.com/pythoncanarias/pycan-web/issues/389

```bash
git checkout -b <issue number>-<issue-name>
```

En cuanto a los commits, este proyecto sigue la guía definida en
semantic commit messages la cual se basa en una primera parte donde explicamos
qué estámos haciendo, el scope. Este puede ser `feat`, `fix`, `docs` entre
otros. Y, a continuación, el mensaje del commit explicativo.

Scopes aceptados:

- `feat`: nueva funcionalidad para el usuario, no funcionalidades para scripts de compilación.
- `fix`: solución a un fallo para el usuario, no fallos de scripst de compilación.
- `docs`: cambios en la documentación.
- `style`: formateado, faltas de puntos y coma, etc. No cambios en código de producción.
- `refactor`: refactor de código en producción. Por ejemplo, cambio de nombre de variable.
- `test`: añadir test faltantes, refactorizar test. No cambios en código de producción.
- `chore`: actualización de tareas rutinarias, etc. No cambios en código de producción.

```bash
git commit -m 'feat: add blog template'
```

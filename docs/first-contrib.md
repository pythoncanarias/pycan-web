## Cómo hacer tu primera contribución a Python Canarias <!-- omit in toc -->

Antes que nada, gracias por tu interés, solo estar aquí ya significa bastante para
nosotrxs. Hacer una contribución al _software_ libre es muy interesante, no
solo para contribuir a la comunidad, sino como una forma de aprender y
adquirir nuevas competencias, y a la vez de formar parte de nuestra comunidad.

- [Primer paso: empezar con Git y GitHub](#primer-paso-empezar-con-git-y-github)
- [Segundo paso: hacer un _fork_ del repositorio](#segundo-paso-hacer-un-fork-del-repositorio)
- [Tercer paso: clonar el repositorio](#tercer-paso-clonar-el-repositorio)
- [Cuarto paso: crear una nueva rama](#cuarto-paso-crear-una-nueva-rama)
- [Quinto paso: incorporar tus cambios](#quinto-paso-incorporar-tus-cambios)
- [Sexto paso: exportar o entregar (_push_) los cambios locales al repositorio](#sexto-paso-exportar-o-entregar-push-los-cambios-locales-al-repositorio)
- [Séptimo paso: crear un _Pull Request_](#séptimo-paso-crear-un-pull-request)

### Primer paso: empezar con Git y GitHub

Lo primero que necesitas es un conocimiento, aunque sea básico, de Git y GitHub.
Si no sabes nada de Git ni de GitHub, te recomendamos el tutorial
de [La guía para principiantes de Git y Github de FreeCodeCamp](https://www.freecodecamp.org/espanol/news/guia-para-principiantes-untitled/).

También necesitarás una cuenta en [GitHub](https://github.com/), que es donde
tenemos almacenado el código fuente de nuestro proyecto. Si no tienes cuenta
puedes crearte una sin problemas, es totalmente gratuito.

Nuestro proyecto está alojado en la siguiente página:

[https://github.com/pythoncanarias/pycan-web](https://github.com/pythoncanarias/pycan-web) 🚀

### Segundo paso: hacer un _fork_ del repositorio

Con tu cuenta de GitHub, ahora puedes hacer un _fork_ de nuestro proyecto en tu
repositorio. Este _fork_ es simplemente una copia de nuestro repositorio, que
es independiente del original, en el sentido de que puedes realizar los
cambios que quieras en el mismo y no tendrán efecto ninguno en nuestro código.
Así puedes experimentar y jugar con el código sin miedo a romper nada.

Para hacer el _fork_, asegúrate de que estás validado correctamente en _GitHub_
con tu cuenta, y simplemente visita con tu navegador nuestro repositorio.
Una vez allí, solo tienes que pulsar el botón con la leyenda _Fork_.

![Github Fork](./assets/github-fork.png)

El nuevo repositorio, el tuyo, tendrá una URL como esta:

```
https://github.com/<tu-nombre-de-usuario>/pycan-web
```

### Tercer paso: clonar el repositorio

Ahora tienes el código en tu propio repositorio en _GitHub_. El siguiente
paso es descargar el código en una carpeta de tu ordenador, un sitio
donde puedas trabajar cómodamente con él.

Esta operación se conoce como _clonado_ del repositorio. Para ello, abre una
terminal y escribe el siguiente comando:

```shell
git clone https://github.com/<tu-nombre-de-usuario>/pycan-web.git
```

Ahora ya tienes una copia local de tu repositorio en tu disco duro.

Este repositorio local está vinculado con tu propia copia de nuestro
repositorio. Puedes también vincularlo con el repositorio original; esto será
cómodo especialmente al final, cuando queremos incorporar los cambios que hayas
hecho en nuestro repositorio. Para vincular con el repositorio original, usa el
siguiente comando:

```shell
git remote add upstream https://github.com/pythoncanarias/pycan-web
```

### Cuarto paso: crear una nueva rama

Para crear una rama usaremos el siguiente comando:

```shell
git checkout -b <nombre de la nueva rama>
```

Ahora estamos situados en una nueva rama. Todos los cambios que hagamos ahora
se quedan dentro de esta rama hasta que se pueda reunificar esta rama con la
rama principal, o bien se borre esta rama y descartemos todos los cambios que
hubiera en ella.

### Quinto paso: incorporar tus cambios

Aquí es donde haces tu magia: realiza los cambios que creas oportunos,
los pruebas si puedes y los vas añadiendo a la rama. Puedes usar `git status` para
obtener un breve informe de la situación actual de la rama en la que estás.

Supongamos que has cambiado parte del texto del fichero `README.md`. Podemos
añadir este fichero al área de trabajo con:

```shell
git add README.md
```

Cada vez que modifiques el código, el comando `add` tiene que ser ejecutado otra
vez para que los últimos cambios se tengan en cuenta en el área de trabajo.

Existe la forma abreviada `git add -u` para que añada al área de trabajo todos
los ficheros que hayan sido actualizados (`-u` por _updated_). También es útil el
_flag_ `-v` para que me muestre un listado de los ficheros añadidos, o sea que
quedaría así: `git add -uv`.

Cuando estés segura de tus cambios, puedes confirmarlos con la
orden `commit` de Git:

```shell
git commit -m "Comentario describiendo los cambios realizados"
```

> Nota: No es necesario que hagas un único _commit_ al final, puedes realizar todos
> los commits que quieras, pero si es verdad que el paso previo a subir el código
> al repositorio debe ser un `commit`. Si no lo hacemos así, quedarían cambios
> el el área de trabajo no confirmadas y, por tanto, ignoradas en el siguiente
> paso, en el `push`.

### Sexto paso: exportar o entregar (_push_) los cambios locales al repositorio

Como se comentó antes, el comando básico aquí es `push`:

```shell
git push -u origin <nombre de la rama>
```

Este paso crea la rama en el repositorio remoto y sube todos los
cambios que estén confirmados en el área de trabajo.

### Séptimo paso: crear un _Pull Request_

Una vez que tus cambios están en tu repositorio, están listos para
realizar un _Pull Request_, que básicamente es una solicitud hecha para
incorporar los cambios incluidos desde una rama a otra rama.

En este caso, lo que debemos hacer es un _Pull Request_ indicando que queremos
incorporar los cambios realizados en nuestra rama hacia la rama `main` del
repositorio original (Es decir, el repositorio de Python Canarias desde
el cual se hizo el _fork_ en el paso dos).

Para ello, abrimos el navegador apuntando a nuestro repositorio en GitHub y
pulsamos el botón que reza "_Compare and Pull Request_". Si todo ha ido bien
nosotros, los mantenedores del repositorio original, seremos notificados
de los cambios y podremos revisarlos. Si los encontramos adecuados,
los incorporaremos en la rama de producción. En caso contrario se hará una revisión solicitando una serie de cambios que puedes aportar en la misma rama que has utilizado.

**¡Felicidades, acabas de realizar tu primera aportación a Python Canarias!** 🎉

### Enlaces de interés <!-- omit in toc -->

- [La guía para principiantes de Git y Github](https://www.freecodecamp.org/espanol/news/guia-para-principiantes-untitled/) de FreeCodeCamp.

- [Hacktoberfest](https://hacktoberfestes.dev/).

- [Make your first open source contribution](https://markodenic.com/make-your-first-open-source-contribution/) de Marko Denic.

- [Recursos de Programación](https://github.com/Acadeller/recursos-programacion).

# Añadir una nueva sección (aplicación) al proyecto

Normalmente, cuando se necesita una nueva aplicación (sección) en un projecto de Django, se puede crear así:

```console
$ ./manage.py startapp <app>
```

Basados en el diseño de nuestro proyecto, se deben llevar a cabo algunos pasos adicionales para lograr visualizar la aplicación correctamente:

1. Añadir `<app>` a la constante `APPS` en [gulp/config.js](gulp/config.js).
2. Crear el archivo `<app>/static/<app>/css/main.scss` con, al menos, el siguiente contenido: `@import "commons/static/commons/css/base";`
3. Crear el archivo de la plantilla base en `<app>/templates/<app>/base.html` el cual se extiende desde [commons/templates/base.html](commons/templates/base.html) como `base.html` y se enlaza a la hoja de estilos `<app>/custom.min.css` (_este archivo es generado por gulp_)
4. Para poder crear el elemento correspondiente en el menú de la cabecera, añadir la entrada a la aplicación en [commons/templates/header.html](commons/templates/header.html).

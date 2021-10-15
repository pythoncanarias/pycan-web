# Añadir una nueva aplicación al proyecto

Los proyectos Django se organizan internamente en aplicaciones. Cada aplicación representa una sección o parte de nuestro proyecto. En el caso de que necesitemos añadir una nueva aplicación tendremos que hacer uso de las herramientas que Django nos proporciona:

```console
$ mkdir apps/<app>  # tenemos las apps en su propia carpeta
$ ./manage.py startapp <app> apps/<app>
```

Basados en el diseño de nuestro proyecto, se deben llevar a cabo algunos pasos adicionales para lograr visualizar la aplicación correctamente.

1. Añadir `<app>` a la lista `INSTALLED_APPS` en `main/settings.py`.
1. Añadir `<app>` a la constante `APPS` en [gulp/config.js](gulp/config.js).
1. [Configurar plantillas](#plantillas).
1. [Añadir estilos CSS](#estilos-css) (si procede).
1. [Añadir código JS](#código-js) (si procede).
1. Para poder crear el elemento correspondiente en el menú de la cabecera, añadir la entrada a la aplicación en [commons/templates/header.html](commons/templates/header.html).

## Plantillas

Se recomienda la creación de una plantilla `<app>/templates/<app>/base.html` para la nueva `<app>` con este esqueleto:

```django
{% extends "base.html" %} <!-- commons/base.html -->

{% load utils %}

<!-- Sólo en el caso de necesitar estilos propios css -->
{% block style %}
  <link rel="stylesheet" href="{{ assets|get_asset_key:'<app>/custom.min.css' }}">
{% endblock style %}

<!-- Sólo en el caso de necesitar código propio js -->
{% block js %}
  <script src="{{ assets|get_asset_key:'<app>/custom.min.js' }}"></script>
{% endblock js %}
```

> `custom.min.css` y `custom.min.js` son ficheros generados automáticamente por el proceso `gulp` que corre en background.

El resto de plantillas de la aplicación, al menos, deberían extender la plantilla base y se recomienda que incluyan una directiva definiendo su propia clase CSS para evitar conflictos posteriores:

```django
{% extends "<app>/base.html" %}

{% block body_class %}<app>-<subsection>{% endblock %}

...

```

## Estilos CSS

En el caso de que se necesiten estilos CSS se debe crear el archivo `<app>/static/<app>/css/main.scss` con, al menos, el siguiente contenido:

```scss
@import "commons/static/commons/css/base";

.<app>-<subsection> {
   ...
}
```

> Se recomienda crear nuevos ficheros `.scss` e importarlos desde `main.scss` para modularizar el código.

## Código JS

En el caso de que se necesite código JS se debe crear el archivo `<app>/static/<app>/js/main.js`

> Se recomienda crear nuevos ficheros `.js` e importarlos desde `main.js` para modularizar el código.

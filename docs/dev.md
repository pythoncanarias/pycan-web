# Configuración para desarrollo

## Entorno de Docker

Este proyecto tiene requisitos variados que hacen altamente recomendable configurar un entorno de desarrollo usando [Docker Compose](https://docs.docker.com/compose/).

1. Clona este repositorio.
2. Inicia los contenedores:
   ```console
   $ docker-compose up  # Deja esto ejecutando y abre una nueva pestaña
   ```
3. Ejecuta las migraciones de la base de datos:
   ```console
   $ docker-compose exec web ./manage.py migrate
   ```
4. Añade datos iniciales de pruebas a la base datos (necesitarás esto para testear la app):
   ```console
   $ docker-compose exec web ./manage.py dbload
   ```

---

> Si dispones de un volcado de la base de datos de pruebas o producción, puedes cargarlo así, en sustitución de los pasos 3 y 4:

```console
$ docker-compose exec -T database /bin/bash -c \
'PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB' < /path/to/db_dump.sql
```

> Para reproducir este último paso más adelante, asegúrate primero de borrar el volumen de la base datos con: `docker volume rm pycan-web_database-data`.

---

5. Crea un superusuario:
   ```console
   $ docker-compose exec web ./manage.py create_default_admin  # admin | admin
   ```

Eso es todo, ahora puedes visitar http://localhost:8000/

> Nótese que tanto la base de datos y la app web enlazan sus puertos de los contenedores a los del sistema host. Si tienes conflictos con puertos, puedes exportar las variables de entorno `PYCAN_DB_PORT` y, `PYCAN_APP_PORT` con los puertos elegidos en el sistema host para, respectivamente, la base de datos y la app, antes de ejecutar `docker-compose up`.

### Interfaz Administrativa

Puedes acceder a la interfaz administrativa de Django yendo a https://docs.docker.com/compose/ y usando las credenciales `admin` / `admin`.

### Multimedia

Si dispones de ficheros multimedia para testing o como copias de producción, puedes ponerlos en el directorio `$PROJECT/media`. Hay un volumen de Docker Compose configurado para cargarlos desde ahí.

## Estilo de código

Intentamos homogeneizar nuestro estilo de código en Python:

- Indentado con 4 espacios.
- Máximo ancho de línea: 79 caracteres.
- Orden de imports como indica [PEP8](https://www.python.org/dev/peps/pep-0008/#imports).
- Linter de Python: [Flake8](https://flake8.pycqa.org/en/latest/)
- Autoformateador de Python: [Black](https://github.com/psf/black)

## VSCode y Docker

Si usas [Visual Studio Code](https://code.visualstudio.com/), puedes enlazar un contenedor remoto y configurar el IDE para usarlo.

Para usar el entorno de desarrollo Docker Compose en VSCode, instala la extensión [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

El directorio `.devcontainer` contiene la configuración necesaria para dar soporte a esta integración. Sigue [estas instrucciones](https://code.visualstudio.com/docs/remote/containers) para habilitarlo.

> Python Malaga tiene un buen [tutorial de cómo configurar VSCode usando Docker](https://www.youtube.com/watch?v=mxpq0ntJ8T8).

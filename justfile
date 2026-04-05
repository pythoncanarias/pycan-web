# Ejecutar comprobaciones del proyecto Django + Flake8 + Vulture
check:
    python manage.py check
    # python manage.py validate_templates # Esperar a Django 4.
    flake8 --count **/*.py
    ruff check .


# Borrar ficheros temporales y espurios
clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -r "{}" \;
    find . -type d -name ".sass-cache" -exec rm -r "{}" \;



# Ejecutar el servidor en modo producción
run: check static
    python manage.py runserver


# Ejecutar el servidor en modo desarrollo
rundev: static
    DEBUG=yes python manage.py runserver_plus


# Abre una shell python con el entorno de Django cargado
shell:
    python manage.py shell_plus


# Actualiza contenidos estáticos
static:
    python manage.py collectstatic --no-input
    #sass --sourcemap=none bulma/custom.scss:commons/static/commons/vendor.min.css
    #sass --sourcemap=none about/static/about/css/main.scss:about/static/about/custom.min.css


# [Re]crear el fichero ctags
tags:
    ctags -R --exclude=@ctags-exclude-names.txt .


# Muestas las versiones de Python y Django
versions:
    python -V
    python -c "import django; print(django.__version__)"
    psql --version
    python -m site

# Mostrar migraciones Django
showmigrations $APP='': check
    python manage.py showmigrations {{APP}}

alias sm := showmigrations

# Crear nuevas migraciones Django
makemigrations $APP='': check
    python manage.py makemigrations {{APP}}

alias mm := makemigrations

# Ejecutar migraciones Django
migrate $APP='': check
    python manage.py migrate {{APP}} --database default
    python manage.py migrate {{APP}} --database test_default

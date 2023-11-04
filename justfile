# Ejecutar comprobaciones del proyecto Django + Flake8 + Vulture
check:
    python manage.py check
    python manage.py validate_templates
    flake8 --count **/*.py

# Detectar código sospechoso, confuso o incompatible
lint:
    ruff --quiet .
    vulture .


# Borrar ficheros temporales y espurios
clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -r "{}" \;
    find . -type d -name ".sass-cache" -exec rm -r "{}" \;


# Ejecuta las migraciones pendientes"
migrate:
    python manage.py migrate


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

# Ejecutar comprobaciones del proyecto Django + Flake8 + Vulture
check:
    python manage.py check
    flake8 --count **/*.py
    ruff check .
    # vulture . --exclude node_modules/


# Borrar ficheros temporales y espurios
clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -r "{}" \;
    find . -type d -name ".sass-cache" -exec rm -r "{}" \;
    rm -r .ruff_cache/


# Ejecutar el servidor en modo producción
run: check static
    python manage.py runserver


# Ejecutar el servidor en modo desarrollo
rundev: static
    DEBUG=yes python3 manage.py runserver_plus 0.0.0.0:8888


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

# Ejecutar los test pasados como paræmetro (Empezará por el último que haya fallado)
test *args='.':
    python3 -m pytest --failed-first -vv -x --log-cli-level=INFO --doctest-modules -m "not slow" {{ args }}

# Muestra información del Harware / S.O. / Python / Django
info:
    @echo "This is an {{arch()}} machine"
    @echo "OS: {{os()}} / {{os_family()}}"
    python3 -V
    python3 -c "import django; print(django.__version__)"
    uptime

# Acceso al DBShell
dbshell *args='default':
    python3 manage.py dbshell --database {{ args }}

# Show migrations
showmigrations $APP='' *args='':
    python3 ./manage.py showmigrations {{APP}} {{ args }}

alias sm := showmigrations

# Make migrations
makemigrations $APP='' *args='':
    python3 ./manage.py makemigrations {{APP}} {{ args }}

alias mm := makemigrations


# Apply migrations
migrate $APP='' *args='':
    python3 ./manage.py migrate {{APP}} {{ args }}

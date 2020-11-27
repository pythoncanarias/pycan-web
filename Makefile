.PHONY: run clean

help:
	@echo "Opciones disponibles:\n"
	@echo " - clean    : Borrar ficheros temporales y espurios"
	@echo " - run      : Ejecutar el servidor en modo producción"
	@echo " - rundev   : Ejecutar el servidor en modo desarrollo"
	@echo " - check    : Ejecutar varias comprobaciones"
	@echo " - static   : Actualiza contenidos estáticos"
	@echo " - migrate  : Ejecuta las migraciones pendientes"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r "{}" \;
	find . -type d -name ".sass-cache" -exec rm -r "{}" \;

static:
	python manage.py collecstatic --no-input
	sass --sourcemap=none bulma/custom.scss:commons/static/commons/vendor.min.css
	sass --sourcemap=none about/static/about/css/main.scss:about/static/about/custom.min.css

run: static
	python manage.py runserver

rundev:
	DEBUG=yes python manage.py runserver_plus

check:
	python manage.py check
	flake8 --count **/*.py

migrate:
	python manage.py migrate

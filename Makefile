.PHONY: run clean static

help:
	@echo "Opciones disponibles:\n"
	@echo " - clean    : Borrar ficheros temporales y espurios"
	@echo " - check    : Ejecutar varias comprobaciones"
	@echo " - run      : Ejecutar el servidor en modo producción"
	@echo " - rundev   : Ejecutar el servidor en modo desarrollo"
	@echo " - static   : Actualiza contenidos estáticos"
	@echo " - migrate  : Ejecuta las migraciones pendientes"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r "{}" \;
	find . -type d -name ".sass-cache" -exec rm -r "{}" \;

check:
	python manage.py check
	flake8 --count **/*.py

static:
	python manage.py collectstatic --no-input
	#sass --sourcemap=none bulma/custom.scss:commons/static/commons/vendor.min.css
	#sass --sourcemap=none about/static/about/css/main.scss:about/static/about/custom.min.css

run: check static
	python manage.py runserver

rundev: static
	DEBUG=yes python manage.py runserver_plus

migrate:
	python manage.py migrate

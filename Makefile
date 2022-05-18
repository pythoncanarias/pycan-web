.PHONY: run clean static

help:
	@echo "Opciones disponibles:\n"
	@echo " - check    : Ejecutar varias comprobaciones"
	@echo " - clean    : Borrar ficheros temporales y espurios"
	@echo " - migrate  : Ejecuta las migraciones pendientes"
	@echo " - run      : Ejecutar el servidor en modo producción"
	@echo " - rundev   : Ejecutar el servidor en modo desarrollo"
	@echo " - shell    : Abre una shell python con el entorno de Django cargado"
	@echo " - static   : Actualiza contenidos estáticos"

check:
	python manage.py check
	flake8 --count **/*.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r "{}" \;
	find . -type d -name ".sass-cache" -exec rm -r "{}" \;

migrate:
	python manage.py migrate

run: check static
	python manage.py runserver

rundev: static
	DEBUG=yes python manage.py runserver_plus

shell:
	python manage.py shell_plus

static:
	python manage.py collectstatic --no-input
	#sass --sourcemap=none bulma/custom.scss:commons/static/commons/vendor.min.css
	#sass --sourcemap=none about/static/about/css/main.scss:about/static/about/custom.min.css

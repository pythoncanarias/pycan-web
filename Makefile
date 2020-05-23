requirements:
	pipenv lock --requirements > requirements.txt
	pipenv lock --requirements --dev > requirements-dev.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r "{}" \;
	find . -type d -name ".sass-cache" -exec rm -r "{}" \;


run:
	python manage.py runserver

rundev:
	python manage.py runserver_plus

check:
	python manage.py check

static:
	python manage.py collecstatic --no-input
	sass --sourcemap=none bulma/custom.scss:commons/static/commons/vendor.min.css
	sass --sourcemap=none about/static/about/css/main.scss:about/static/about/custom.min.css

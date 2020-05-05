requirements:
	 pipenv lock --requirements > requirements.txt
	 pipenv lock --requirements --dev > requirements-dev.txt

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -d -delete

rundev:
	python manage.py runserver

check:
	python manage.py check

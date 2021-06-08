FROM python:3.6-buster

ENV DEBIAN_FRONTEND=noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

ENV PYCAN_DIR=/var/www/pycan

ENV PYTHONPATH=/var/www/pycan
ENV PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/opt/venv

EXPOSE 8000

WORKDIR $PYCAN_DIR


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        ca-certificates \
        postgresql-client \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

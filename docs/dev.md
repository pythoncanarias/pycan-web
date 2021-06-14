# Development setup

## Docker environment

This project needs a variety of requirements and it's highly recommended to set up a development environment through [Docker](https://www.docker.com/).

1. Clone this repository.
2. Launch containers (building if proceed):
   ```console
   $ docker-compose up  # leave this running and open new tab
   ```
3. Run the database migrations:
   ```console
   $ docker-compose exec web ./manage.py migrate
   ```
4. Add initial test data to the DB (You will need this to test the web app):
   ```console
   $ docker-compose exec web ./manage.py dbload
   ```

---

> Instead of 3) and 4) you can load a (production) database dump using:

```console
$ docker-compose exec -T database /bin/bash -c \
'PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB' < /path/to/db_dump.sql
```

> If you want to reproduce this last step afterwards, first be sure to remove the database volume with: `docker volume rm pycan-web_database-data`.

---

5. Create a default superuser:
   ```console
   $ docker-compose exec web ./manage.py create_default_admin  # admin | admin
   ```

That's it, now visit http://localhost:8000/

> Note that both the database and the web app bind their ports to the host. If you have port conflicts, you can export the environment variables `PYCAN_DB_PORT` and, `PYCAN_APP_PORT` to the desired ports in the host for, respectively, the database and the app, before running `docker-compose up`.

### Administrative interface

You can access the Django administrative interface visiting http://localhost:8000/admin using credentials: `username: admin` | `password: admin`

### Media

If you have a bunch of (production) files for media, you can leave them in the folder `$PROJECT/media`. A docker volume is set up to collect them from there.

## Code style

Some hints should be followed in order to homogenize **Python** code style:

- Indenting with 4 spaces.
- Max line length: 79 chars.
- Imports ordering like in [PEP8](https://www.python.org/dev/peps/pep-0008/#imports).
- Python linter: [Flake8](https://flake8.pycqa.org/en/latest/)
- Python autoformatter: [Black](https://github.com/psf/black)

## VSCode over Docker

One of the multiple options for editing code is [Visual Studio Code](https://code.visualstudio.com/). A nice feature is to link a remote container and configure the IDE installing the required tools on it.

In order to use the Docker development environment in VSCode you have to install the extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

The folder `.devcontainer` already contains the necessary files to enable the Docker "remote" container. Just follow [these instructions](https://code.visualstudio.com/docs/remote/containers) to enable it.

> A good tutorial for setting up VSCode over Docker was broadcasted by Python Malaga. [Check it out](https://www.youtube.com/watch?v=mxpq0ntJ8T8)!

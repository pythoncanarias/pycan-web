# Development setup

## Docker environment

This project needs a variety of requirements and it's highly recommended to set up a development environment through [Docker](https://www.docker.com/).

1. Clone this repository.
2. Build the main app image and the [Gulp](https://gulpjs.com/) (build tool) image:
   ```console
   $ docker compose build
   ```
3. Run the database migrations:
   ```console
   $ docker compose run pycan_web ./manage.py migrate
   ```
4. Add initial test data to the DB (You will need this to test the web app):
   ```console
   $ docker compose run pycan_web ./manage.py dbload
   ```
5. Launch the app with the dependencies. This will start all services and keep your terminal blocked (You can Ctrl-C to stop all services):
   ```console
   $ docker compose up
   ```

That's it, now visit http://localhost:8000/

> Note that both the database and the web app bind their ports to the host. If you have port conflicts, you can export the environment variables `PYCAN_DB_PORT` and, `PYCAN_APP_PORT` to the desired ports in the host for, respectively, the database and the app, before running `docker compose up`.

## VSCode over Docker

One of the multiple options for editing code is [Visual Studio Code](https://code.visualstudio.com/). A nice feature is to link a remote container and configure the IDE installing the required tools on it.

In order to use the Docker development environment in VSCode you have to install the extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

The folder `.devcontainer` already contains the necessary files to enable the Docker "remote" container. Just follow [these instructions](https://code.visualstudio.com/docs/remote/containers) to enable it.

> A good tutorial for setting up VSCode over Docker was broadcasted by Python Malaga. [Check it out](https://www.youtube.com/watch?v=mxpq0ntJ8T8)!

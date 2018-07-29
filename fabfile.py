from fabric.api import env, local, cd, run

env.hosts = ["pythoncanarias.es"]


def deploy():
    local("git push")
    with cd("~/web"):
        run("git pull")
        run("pipenv install")
        run("npm install")
        run("gulp")
        run("pipenv run python manage.py collectstatic "
            "-i commons -i events -i homepage --noinput --clear")
        run("supervisorctl restart web")

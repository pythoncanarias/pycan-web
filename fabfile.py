from fabric.api import env, local, cd, run

env.hosts = ["pythoncanarias.es"]


def deploy():
    local("git push")
    with cd("~/web"):
        run("git pull")
        run("pipenv install")
        run("pipenv run python manage.py collectstatic --noinput")
        run("supervisorctl restart web")

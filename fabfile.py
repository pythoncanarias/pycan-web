from fabric.api import env, local, cd, run

env.hosts = ["pythoncanarias.es"]


def deploy():
    local("git push")
    with cd("~/web"):
        run("git pull")
        run("pipenv install")
        run("npm install --no-save")
        run("gulp")
        run("pipenv run python manage.py collectstatic --noinput --clear")
        run("supervisorctl restart web")

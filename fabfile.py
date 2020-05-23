from fabric.api import cd, env, local, run, prefix

env.hosts = ['pythoncanarias.es']


def deploy():
    local('git push')
    with prefix('source ~/.virtualenvs/web/bin/activate'):
        with cd('~/web'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('npm install --no-save')
            run('gulp')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput --clear')
            run('supervisorctl restart web')
            run('supervisorctl restart rq')

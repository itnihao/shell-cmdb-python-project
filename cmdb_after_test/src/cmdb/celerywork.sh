export C_FORCE_ROOT="true"
export PYTHONOPTIMIZE=1
ps -ef|grep celery|grep -v 'grep'| grep -v 'celerywork.sh'|awk '{print $2}'| xargs kill -9 
celery worker -A application.celery --loglevel=info &

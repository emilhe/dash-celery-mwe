import time
from celery import Celery

# Link the celery app to the desired broker/backend as setup in the docker-compose file.
celery_app = Celery('tasks', broker='pyamqp://guest@myapp-rabbitmq//', backend='redis://myapp-redis')


# Put all long running tasks here and annotate them with the @celery_app.task decorator.
@celery_app.task
def take_a_nap(nap_time):
    print("Falling asleep...")
    time.sleep(nap_time)
    print("... waking up!")
    return "Nap of {}s duration completed.".format(nap_time)

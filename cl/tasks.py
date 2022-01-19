import os
import time
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
# service_bus_namespace =   # TODO: WHAT IS THIS?
# queue_name_prefix = "emher-test"


sas_policy = "RootManageSharedAccessKey"
sas_key = os.getenv('AZURE_SAS_KEY')
namespace = "sb-d-vps-plantdesign2"

config = dict(
    broker=f"azureservicebus://{sas_policy}:{sas_key}@{namespace}",
    backend=f"azureblockblob://{os.getenv('AZURE_CONNECTION_STRING')}",
    azureblockblob_container_name=os.getenv("AZURE_CONTAINER_NAME"),
    # queue_name_prefix=queue_name_prefix
)
celery_app = Celery('tasks', **config)


# Put all long running tasks here and annotate them with the @celery_app.task decorator.
@celery_app.task
def take_a_nap(nap_time):
    print("Falling asleep...")
    time.sleep(nap_time)
    print("... waking up!")
    return str("Nap of {}s duration completed.".format(nap_time))

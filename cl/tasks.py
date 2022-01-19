import os
import time
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
celery_app = Celery(main='tasks',
                    broker=f"azureservicebus://{os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')}",
                    backend=f"azureblockblob://{os.getenv('AZURE_BLOB_STORAGE_CONNECTION_STRING')}",
                    azureblockblob_container_name=os.getenv("AZURE_BLOB_STORAGE_CONTAINER_NAME"))


# Put all long-running tasks here and annotate them with the @celery_app.task decorator.
@celery_app.task
def take_a_nap(nap_time):
    print("Falling asleep...")
    time.sleep(int(nap_time))
    print("... waking up!")
    return str("Nap of {}s duration completed.".format(nap_time))

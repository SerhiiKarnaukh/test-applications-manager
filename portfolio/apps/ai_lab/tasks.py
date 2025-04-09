import os
import shutil
from celery import shared_task
from django.conf import settings


@shared_task
def delete_generated_images():
    folder_path = os.path.join(settings.MEDIA_ROOT, 'generated_images')
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

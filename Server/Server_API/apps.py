from django.apps import AppConfig
import json
import threading
import time

def run_task_loop():
    """Background thread to run the function every hour."""
    from Server_API.tasks import check_tache_alerts,remind_projects_to_update  # Import here to avoid circular import issues
    while True:
        print("Running task...")
        #check_tache_alerts()  # Call the function
        #remind_projects_to_update()
        print("Task completed.")
        time.sleep(3600)  # Run every 1 hour

class ServerApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Server_API'

    def ready(self):
        import Server_API.signals

        thread = threading.Thread(target=run_task_loop, daemon=True)
        thread.start()
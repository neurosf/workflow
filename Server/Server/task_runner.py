import os
import django
import time
# not working
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')
django.setup()

# Import your function
from Server_API.tasks import check_tache_alerts  

def my_task():
    print("Running task...")
    #check_tache_alerts()  # Call your function
    print("Task completed.")

# Run the task every 1 hour
while True:
    my_task()
    time.sleep(3600)  # Wait 1 hour before running again
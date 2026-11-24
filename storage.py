import json
import os

task_file = "task_file.json"

# this function saves the tasks list to a file that exists or creates the file if it does not exist
def save_tasks(tasks, filepath = task_file):
    with open(filepath, "w") as file:
        json.dump(tasks, file, indent=2)

# this function loads the tasks list in the file and if there is a problem reading the file, it starts with an empty tasks list
def load_tasks(filepath = task_file):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                tasks = json.load(file)
                return tasks
        except (json.JSONDecodeError, IOError):
            print("Warning!!! Cannot read the task file. Creating a new file")
            return []
    else:
        return []

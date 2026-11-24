import uuid
from datetime import datetime

def generate_task_id(existing_tasks):
    task_ids = [task["Task_ID"] for task in existing_tasks]
    while True:
        task_id = uuid.uuid4().hex[:6]
        if task_id not in task_ids:
            return task_id 

def calculate_priority(due_date_str):
    date_format = "%d-%m-%Y"
    date_time = datetime.strptime(due_date_str, date_format)
    date = date_time.date()

    days = (date - datetime.today().date()).days

    if days < 0:
        return "Overdue"
    elif days < 7:
        return "Urgent"
    elif days <= 14:
        return "Important"
    else:
        return "Can Wait"

def add_task(tasks, title, description, start_date, due_date):
    task_id = generate_task_id(tasks)
    priority = calculate_priority(due_date)
    task = {
        "Task_ID": task_id,
        "Task_Title": title,
        "Description": description,
        "Start_Date": start_date,
        "Due_Date": due_date,
        "Priority": priority,
        "Status": "yet to start"
    }
    tasks.append(task)
    return tasks

def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task['Task_ID'] == task_id:
            return task
    return

def mark_task_completed(tasks, task_id):
    task = find_task_by_id(tasks, task_id)
    if task is not None:
        task["Status"] = "Completed"
        return True
    return False

def delete_task(tasks, task_id):
    task = find_task_by_id(tasks, task_id)
    if task is not None:
        tasks.remove(task)
        return True
    return False

def edit_task(tasks, task_id, new_title=None, new_start_date=None, new_due_date=None):
    task = find_task_by_id(tasks, task_id)
    if task is not None:
        if new_title is not None:
            task["Task_Title"] = new_title
        if new_start_date is not None:
            task["Start_Date"] = new_start_date
        if new_due_date is not None:
            task["Due_Date"] = new_due_date
            task["Priority"] = calculate_priority(new_due_date)
        return True
    return False

def update_task_statuses(tasks):
    date_format = "%d-%m-%Y"
    today = datetime.today().date()
    for task in tasks:
        if task.get("Status") == "yet to start":
            start_date = datetime.strptime(task["Start_Date"], date_format).date()
            if today >= start_date:
                task["Status"] = "in Progress"
                task["Priority"] = calculate_priority(task["Due_Date"])

def mark_task_in_progress(tasks, task_id):
    task = find_task_by_id(tasks, task_id)
    if task and task.get("Status") == "yet to start":
        task["Status"] = "in Progress"
        return True
    return False

def filter_tasks(tasks, status=None, priority=None):
    filtered = []
    
    for task in tasks:
        matches = True
        if status is not None and task.get("Status", "").lower() != status.lower():
            matches = False
        if priority is not None and task.get("Priority", "").lower() != priority.lower():
            matches = False
            
        if matches:
            filtered.append(task)
            
    return filtered
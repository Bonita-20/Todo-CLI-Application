import storage
import logic
from datetime import datetime

def format_cell(key, val):
    if key == "Status":
        s = str(val).strip().lower()
        if s in ("completed", "done"):
            return f"[✓] {val}"
        if s in ("pending", "in progress", "ongoing"):
            return f"[-] {val}"
        return f"[ ] {val}"
    return "" if val is None else str(val)

def calculate_col_width(tasks, target_columns, spacing=4):
    widths = {}
    for col in target_columns:
        header_len = len(col)
        
        if not tasks:
            widths[col] = header_len + spacing
            continue
            
        lengths = []
        for task in tasks:
            val = task.get(col, "")
            lengths.append(len(format_cell(col, val)))

        max_val_len = max(lengths) if lengths else 0
        widths[col] = max(header_len, max_val_len) + spacing

    return widths

def view_tasks(tasks):
    columns = ["Task_ID", "Task_Title", "Description", "Start_Date", "Due_Date", "Priority", "Status"]

    widths = calculate_col_width(tasks, columns)

    # 1. Print Header
    header_line = "".join(col.ljust(widths[col]) for col in columns)
    separator = "-" * len(header_line)
    print(header_line)
    print(separator)

    # 2. Print Rows
    for task in tasks:
        row_str = ""
        for col in columns:
            val = task.get(col, "")

            row_str += format_cell(col, val).ljust(widths[col])

        print(row_str)

def prompt_for_date(prompt_message):
    date_format = "%d-%m-%Y"

    while True:
        date = input(prompt_message).strip()
        try:
            datetime.strptime(date, date_format)
            return date
        except ValueError:
            print("Invalid date format. Please enter the date using DD-MM-YYYY (e.g., 25-12-2026).")

def print_menu():
        print("\n--To-DO CLI APPLICATION--")
        print("\n Main Menu:")
        print("[1] Add Task")
        print("[2] View All Task")
        print("[3] Start task (mark in-progress)")
        print("[4] Complete Task")
        print("[5] Edit Task")
        print("[6] Delete Task")
        print("[7] Filter Task")
        print("[8] Exit")

def main():
    tasks = storage.load_tasks()
    logic.update_task_statuses(tasks)
    storage.save_tasks(tasks)

    while True:
        print_menu()
        choice = input("Select an option (1-8):").strip()
        if choice in ["2", "3", "4", "5", "6", "7"] and not tasks:
            print("\nNo tasks recorded yet. Please add a task first.")
            continue

        if choice == "1":
            title = input("Enter the task title: ").strip().title()
            description = input("Enter the task description: ").strip().capitalize()
            start_date = prompt_for_date("Enter the task start date.")
            due_date = prompt_for_date("Enter the task due date.")
            logic.add_task(tasks, title, description, start_date, due_date)
            storage.save_tasks(tasks)
            print("Task added successfully.")

        elif choice == "2":
            logic.update_task_statuses(tasks)
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            task_id = input("Enter the task id to start: ").strip()
            if logic.mark_task_in_progress(tasks, task_id) == True:
                print("Success")
                storage.save_tasks(tasks)
            else:
                print("Error")

        elif choice == "4":
            view_tasks(tasks)
            task_id = input("Enter the task id to complete: ").strip()
            if logic.mark_task_completed(tasks, task_id) == True:
                print("Success")
                storage.save_tasks(tasks)
            else:
                print("Error")

        elif choice == "5":
            view_tasks(tasks)
            task_id = input("Enter the task id to edit: ").strip()
            field = input("What do you want to change (title, start date, or due date)? ").strip().lower()
            if field == "title":
                new_val = input("Enter new title: ").strip().title()
                logic.edit_task(tasks, task_id, new_title=new_val)
            elif field == "start date":
                new_val = prompt_for_date("Enter new start date (DD-MM-YYYY): ")
                logic.edit_task(tasks, task_id, new_start_date=new_val)
            elif field == "due date":
                new_val = prompt_for_date("Enter new due date (DD-MM-YYYY): ")
                logic.edit_task(tasks, task_id, new_due_date=new_val)
            else:
                print("Invalid field selected.")
            storage.save_tasks(tasks)

        elif choice == "6":
            view_tasks(tasks)
            task_id = input("Enter the task id you want to delete: ")
            
            while True:
                ans = input("Are you sure you want to delete this task? (y/n): ").strip().lower()
                if ans in ["y", "n"]:
                    break
                print("Enter a valid response. y or n")
                
            if ans == "y":
                if logic.delete_task(tasks, task_id):
                    print("Task deleted successfully.")
                    storage.save_tasks(tasks)
                else:
                    print("Task ID not found")
            else:
                print("Deletion canceled.")

        elif choice == "7":
            category = input("Filter by (1) Status or (2) Priority? ").strip()
            if category == "1":
                val = input("Enter status (yet to start / in progress / completed): ").strip()
                view_tasks(logic.filter_tasks(tasks, status=val))
            elif category == "2":
                val = input("Enter priority (Urgent / Important / Can Wait / Overdue): ").strip()
                view_tasks(logic.filter_tasks(tasks, priority=val))
            else:
                print("Invalid filter selection.")

        elif choice == "8":
            storage.save_tasks(tasks)
            print("Goodbye")
            break
        else:
            print("Enter a valid option (1-8).")

if __name__ == "__main__":
    main()
from datetime import datetime
import sys
import os
import json

#------------------------
# Load task from tasks.json
#------------------------

if not os.path.exists("tasks.json"):
    with open("tasks.json", "w") as file:
        json.dump([], file)


with open('tasks.json', 'r') as file:
    tasks = json.load(file)



#---------------------------
#Read command line arguments
#---------------------------

if len(sys.argv) == 1:
    print("No command provided")
    exit()

command = sys.argv[1]

if command == "add":
    if len(sys.argv) == 2:
        print("No description provided.")
        exit()


    description = sys.argv[2]
    print(f"Adding task: {description}")

    new_id = 1
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    now = datetime.now().isoformat()


    task ={
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)\

    print(f"task added successfully with id {new_id}")


if sys.argv[1] == "list":

    if not tasks:
        print("No tasks found.")
        exit()

    if len(sys.argv) == 2:
        for task in tasks:
            print(f"ID is: {task['id']}")
            print(f"Description is: {task['description']}")
            print(f"Status is: {task['status']}")
            print(f" ") 
    else:
        if len(sys.argv) > 3:
            print("Too many arguments provided.")
            exit()

        valid_status= ['todo', 'in-progress', 'done']
        status_filter = sys.argv[2]
        if status_filter not in valid_status:
            print('Invalid status.')
            exit()

        found= False

        for task in tasks:
            if sys.argv[2] == task['status']:
                found = True
                print(f"ID is: {task['id']}")
                print(f"Description is: {task['description']}")
                print(f"Status is: {task['status']}")
                print(f" ")

        if not found:
            print(f"No task found with status: {status_filter}")




if command == 'mark-done':
    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Tasd Id must be a number.")
        exit()

    


    found = False
    for task in tasks:
        if task_id == task['id']:
            found = True
            task['status'] = 'done'
            task["updatedAt"] = datetime.now().isoformat()
            break
    if not found:
        print(f"Task with ID {task["id"]} not found.")
        exit()


    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} marked as done.")





if command == 'mark-in-progress':    
    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task Id must be a number.")
        exit()

    found = False
    for task in tasks:
        if task_id == task['id']:
            found = True
            task['status'] = 'in-progress'
            task["updatedAt"] = datetime.now().isoformat()
            break
    if not found:
        print(f"Task with ID {task["id"]} not found.")
        exit()


    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} marked as in_progress.")




if command == 'update':

    if len(sys.argv) < 4:
        print("Task ID and new description are required.")
        exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task Id must be a number.")
        exit()

    new_description = sys.argv[3]

    if not new_description.strip():
        print("Description cannot be empty.")
        exit()

    found = False

    for task in tasks:

        if task_id == task['id']:

            found = True

            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()

            break

    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} updated successfully.")


if command == 'delete':
    if len(sys.argv) < 3:
        print("Task Id is required.")
        exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task Id must be a number.")
        exit()

    found = False
    for task in tasks:
        if task_id == task['id']:
            found = True
            tasks.remove(task)
            break
    if not found:
        print(f"Task with ID {task_id} not found.")
        exit()

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} deleted successfully.")


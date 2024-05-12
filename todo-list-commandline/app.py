import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
# Read environment variables
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_port = os.environ.get("DB_PORT")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    port=db_port,
    password=db_password,
    database=db_name
) #Check Connection Settings in MySQL Workbench to get these details

def add_task(task_name, description):
    cursor = db.cursor()
    sql = "INSERT INTO tasks (task_name, description) VALUES (%s, %s)"
    val = (task_name, description)
    cursor.execute(sql, val)
    db.commit()
    print("Task added successfully!")

def view_tasks():
    cursor = db.cursor()
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    tasks = cursor.fetchall()
    if (tasks):
        for task in tasks:
            print(f"Task ID: {task[0]}, Task Name: {task[1]}, Description: {task[2]}, Completed: {'Yes' if task[3] else 'No'}")
    else:
        print("No Tasks in the DataBase")  

def mark_completed(task_id):
    cursor = db.cursor()
    sql = "UPDATE tasks SET is_completed = 1 WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    db.commit()
    print("Task marked as completed!")

def update_task(task_id, task_name, description):
    cursor = db.cursor()
    sql = "UPDATE tasks SET task_name = %s, description = %s WHERE id = %s"
    val = (task_name, description, task_id)
    cursor.execute(sql, val)
    db.commit()
    print("Task details updated successfully!")

def delete_task(task_id):
    cursor = db.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    db.commit()
    print("Task deleted successfully!")

if __name__ == "__main__":
    while True:
        print("\n--- To-Do List ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Update Task Details")
        print("5. Delete Task")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            task_name = input("Enter the task name: ")
            description = input("Enter the task description: ")
            add_task(task_name, description)

        elif choice == 2:
            print("\n--- Tasks ---")
            view_tasks()

        elif choice == 3:
            task_id = int(input("Enter the task ID to mark as completed: "))
            mark_completed(task_id)

        elif choice == 4:
            task_id = int(input("Enter the task ID to update: "))
            task_name = input("Enter the new task name: ")
            description = input("Enter the new task description: ")
            update_task(task_id, task_name, description)

        elif choice == 5:
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(task_id)

        elif choice == 6:
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

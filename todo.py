import csv
import os


class Task:
    def __init__(self, title, description="", priority="Medium"):
        self.title = title
        self.description = description
        self.priority = priority


    def to_csv_row(self):
        return [self.title, self.description, self.priority]


    @staticmethod
    def from_csv_row(row):
        title = row[0] if len(row) > 0 else ""
        description = row[1] if len(row) > 1 else ""
        priority = row[2] if len(row) > 2 else "Medium"
        return Task(title, description, priority)






class ToDoList:
    def __init__(self):
        self.tasks = []


    def add_task(self, task):
        self.tasks.append(task)


    def remove_task_by_index(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks.pop(index)
        return None


    def remove_task_by_title(self, title):
        for i, t in enumerate(self.tasks):
            if t.title == title:
                return self.tasks.pop(i)
        return None


    def list_tasks(self):
        return self.tasks


    def save_to_csv(self, filename):
        """
        Save all tasks to a CSV file.
        Returns True on success, False on error.
        """
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # write header
                writer.writerow(["title", "description", "priority"])
                # write each task
                for task in self.tasks:
                    writer.writerow(task.to_csv_row())
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False


    def load_from_csv(self, filename):
        """
        Load tasks from a CSV file, replacing current tasks.
        Returns True if loaded, False if file not found or error.
        """
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                # skip header if present
                header = next(reader, None)
                self.tasks = []
                for row in reader:
                    if not row:
                        continue
                    task = Task.from_csv_row(row)
                    self.tasks.append(task)
            return True
        except Exception as e:
            print(f"Error loading from {filename}: {e}")
            return False






def print_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add task")
    print("2. Remove task (by index)")
    print("3. Remove task (by title)")
    print("4. View tasks")
    print("5. Save tasks to CSV")
    print("6. Load tasks from CSV")
    print("7. Exit")


def input_priority():
    while True:
        p = input("Priority (High / Medium / Low) [Medium]: ").strip()
        if p == "":
            return "Medium"
        p_cap = p.capitalize()
        if p_cap in ["High", "Medium", "Low"]:
            return p_cap
        else:
            print("Invalid priority. Please type High, Medium, or Low.")


def main():
    filename = "tasks.csv"
    todo = ToDoList()

    # try to load existing tasks automatically
    loaded = todo.load_from_csv(filename)
    if loaded:
        print(f"Loaded tasks from {filename}.")
    else:
        print(f"No previous tasks loaded (or {filename} not found).")

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()
        if choice == "1":
            title = input("Task title: ").strip()
            if title == "":
                print("Title cannot be empty.")
                continue
            description = input("Task description (optional): ").strip()
            priority = input_priority()
            task = Task(title, description, priority)
            todo.add_task(task)
            print("Task added.")
        elif choice == "2":
            if not todo.tasks:
                print("No tasks to remove.")
                continue
            try:
                index_str = input("Enter index of task to remove (starting from 0): ").strip()
                index = int(index_str)
                removed = todo.remove_task_by_index(index)
                if removed:
                    print(f"Removed task: {removed.title}")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid integer index.")
        elif choice == "3":
            if not todo.tasks:
                print("No tasks to remove.")
                continue
            title = input("Enter exact title of task to remove: ").strip()
            removed = todo.remove_task_by_title(title)
            if removed:
                print(f"Removed task: {removed.title}")
            else:
                print("Task with that title not found.")
        elif choice == "4":
            tasks = todo.list_tasks()
            if not tasks:
                print("No tasks.")
            else:
                print("\nCurrent tasks:")
                for i, t in enumerate(tasks):
                    print(f"[{i}] Title: {t.title} | Priority: {t.priority}")
                    if t.description:
                        print(f"     Desc: {t.description}")
        elif choice == "5":
            ok = todo.save_to_csv(filename)
            if ok:
                print(f"Tasks saved to {filename}.")
        elif choice == "6":
            ok = todo.load_from_csv(filename)
            if ok:
                print(f"Tasks loaded from {filename}.")
            else:
                print(f"Could not load from {filename} (file may not exist).")
        elif choice == "7":
            # auto-save on exit
            ok = todo.save_to_csv(filename)
            if ok:
                print(f"Tasks saved to {filename}. Exiting.")
            else:
                print("Exiting without saving due to an error.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")

if __name__ == "__main__":
    main()

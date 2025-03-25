import datetime

# ===== Load Users Function =====


def load_users():
    """
    Loads users from user.txt and returns a dictionary {username: password}.

    If the file is missing, an error is displayed.
    """
    # Dictionary to store users
    users = {}
    try:
        # Open 'user.txt' in read mode with UTF-8 encoding
        with open('user.txt', 'r', encoding="utf-8") as file:
            for line in file:

                # Extract username and password from each line
                username, password = line.strip().split(', ')

                # Store them in the dictionary
                users[username] = password
    except FileNotFoundError:
        print("\nError: 'user.txt' file not found. Please check the file location.")
    return users

# ===== Load Tasks Function =====


def load_tasks():
    """
    Reads tasks from 'tasks.txt' and returns a list of dictionaries.

    Each dictionary represents a task with relevant fields.
    """
    tasks_list = []

    try:
        with open('tasks.txt', 'r', encoding="utf-8") as file:
            for line in file:
                content = line.strip().split(', ')

                # Ensure correct format
                if len(content) == 6:
                    task = {
                        "assigned_to": content[0],
                        "title": content[1],
                        "description": content[2],
                        "date_assigned": content[3],
                        "due_date": content[4],
                        "completed": content[5]
                    }
                    tasks_list.append(task)
    except FileNotFoundError:
        print("\nError: 'tasks.txt' file not found.")

    return tasks_list


# ===== Login Section =====
users = load_users()

while True:
    username = input("\nEnter your username: ")

    # Check if username exists
    if username not in users:
        print("\nInvalid username. Please try again.")

        # Restart loop if username is invalid
        continue

    password = input("Enter your password: ")

    # Keep asking for password if password is incorrect
    while password != users[username]:
        print("\nInvalid password. Try again.")
        password = input("Enter your password: ")

    print("\nYou have successfully logged in!")
    break

# ===== Main Menu Section =====
while True:
    try:
        # Admin sees extra options such as "register user" and "display
        # statistics".
        if username == "admin":
            menu = input('''\nSelect one of the following options:
    r  - Register a new user (Admin Only)
    a  - Add a new task
    va - View all tasks
    vm - View my tasks
    ds - Display statistics (Admin Only)
    e  - Exit
Enter your choice: ''').lower()
        else:
            menu = input('''\nSelect one of the following options:
    a  - Add a new task
    va - View all tasks
    vm - View my tasks
    e  - Exit
Enter your choice: ''').lower()

        # ===== Register a New User (Admin Only) =====
        if menu == 'r':
            if username == "admin":
                new_username = input("\nEnter a new username: ")

                # Check if username already exists
                if new_username in users:
                    print("This username already exists. Please choose another.")
                    continue

                new_password = input("Enter a new password: ")
                confirm_password = input("Confirm your password: ")

                if new_password != confirm_password:
                    print("Passwords do not match. Please try again.")
                    # Restart Loop
                    continue

                # Add new user to user.txt file
                with open('user.txt', 'a', encoding="utf-8") as file:
                    file.write(f"\n{new_username}, {new_password}")

                # Update local users dictionary
                users[new_username] = new_password
                print("New user registered successfully!")
            else:
                print("Access Denied! Only the admin can register new users.")

        # ===== Add a New Task =====
        elif menu == 'a':
            task_username = input(
                'Enter the username of the person to assign the task: ')

            # Check if user exists
            if task_username not in users:
                print("User does not exist. Please enter a valid username.")
                continue

            title = input('Enter the title of the task: ')
            description = input('Enter the description of the task: ')
            due_date = input('Enter the due date of the task (DD MMM YYYY): ')
            current_date = datetime.datetime.now().strftime('%d %b %Y')

            # Save the new task in 'tasks.txt'
            with open('tasks.txt', 'a') as file:
                file.write(
                    f'{task_username}, {title}, {description}, {current_date}, {due_date}, No\n')

            print("Task has been successfully added.")

        # ===== View All Tasks =====
        elif menu == 'va':
            print("\nAll Tasks:")

            # Load tasks from file
            tasks = load_tasks()

            if not tasks:
                print("No tasks available.")
            else:
                for task in tasks:
                    print(
                        f"\nTask:          \t{task['title']}\n"
                        f"Assigned to:   \t{task['assigned_to']}\n"
                        f"Date assigned: \t{task['date_assigned']}\n"
                        f"Due date:      \t{task['due_date']}\n"
                        f"Task complete: \t{task['completed']}\n"
                        f"Description:   \t{task['description']}\n"
                    )

        # ===== View My Tasks =====
        elif menu == 'vm':
            print(f"\n{username}'s Tasks:")
            tasks = load_tasks()

            # Flag to check if the user has tasks
            task_found = False

            # Loop through all tasks and print only those assigned to the user
            for task in tasks:
                if task['assigned_to'] == username:
                    task_found = True
                    print(
                        f"\nTask:          \t{task['title']}\n"
                        f"Date assigned: \t{task['date_assigned']}\n"
                        f"Due date:      \t{task['due_date']}\n"
                        f"Task complete: \t{task['completed']}\n"
                        f"Description:   \t{task['description']}\n"
                    )

            # If no tasks were found, print a message
            if not task_found:
                print("You have no assigned tasks.")

        # ===== Display Statistics (Admin Only) =====
        elif menu == 'ds':
            if username == "admin":
                print("\n===== Statistics =====")
                print(f"Total Number of Users: {len(users)}")
                print(f"Total Number of Tasks: {len(load_tasks())}")
            else:
                print("Access Denied! Only the admin can view statistics.")

        # ===== Exit Program =====
        elif menu == 'e':
            print("\nGoodbye! Exiting the application.")
            exit()

        # ===== Invalid Input Handling =====
        else:
            print("\nInvalid selection. Please choose a valid option.")

    except FileNotFoundError:
        print("\nError: Required file not found.")
    except ValueError:
        print("\nError: Invalid input detected. Please enter valid information.")
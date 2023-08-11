import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Define global variables
command_history = []
command_index = -1

try:
    import custom_commands
except ImportError:
    print("No custom commands found.")

def start_service(service_name):
    """Starts a Windows service."""
    os.system(f'net start {service_name}')

def stop_service(service_name):
    """Stops a Windows service."""
    os.system(f'net stop {service_name}')

# Add more function definitions here

def help_command():
    """Displays help information for available commands."""
    print("Available commands:")
    for name, obj in globals().items():
        if callable(obj) and obj.__module__ == __name__ and obj.__doc__:
            print(f"{name}: {obj.__doc__}")

def main():
    username = os.getlogin()
    os.chdir(os.path.join("C:\\Users", username, "desktop"))

    completer = WordCompleter(["exit", "cd", "ls", "history", "up", "down", "help"] + list(globals().keys()))
    session = PromptSession(completer=completer, auto_suggest=AutoSuggestFromHistory())

    while True:
        try:
            user_input = session.prompt(os.getcwd() + "> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            print("Exiting...")
            break

        if user_input == "exit":
            break

        if user_input.strip():
            command_history.append(user_input)

        parts = user_input.split()
        command = parts[0]
        arguments = parts[1:]

        if command == "cd":
            if arguments:
                try:
                    os.chdir(arguments[0])
                except FileNotFoundError:
                    print("Sorry, the specified path does not exist.")
            else:
                print("Please specify a path.")

        elif command == "ls":
            contents = os.listdir(os.getcwd())
            print("\n".join(contents))

        elif command == "history":
            print("\n".join(command_history))

        elif command == "up":
            # Implement the 'up' functionality here
            if command_index >= 0:
                user_input = command_history[command_index]
                command_index -= 1
            else:
                print("No more history.")
            

        elif command == "down":
            if command_index < len(command_history) - 1:
                command_index += 1
                user_input = command_history[command_index]
            else:
                print("Already at the latest command in history.")
            

        elif hasattr(custom_commands, command):
            try:
                getattr(custom_commands, command)(*arguments)
            except Exception as e:
                print("Error executing custom command:", e)

        elif command == "help":
            help_command()

        else:
            print("Invalid command. Type 'exit' to quit.")

if __name__ == "__main__":
    main()

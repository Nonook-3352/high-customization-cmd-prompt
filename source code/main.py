import os
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from types import FunctionType
import subprocess
import datetime
import threading
import sys
import socket


# Define global variables
command_history = []
command_index = -1
time = datetime.datetime.now()

#colorama.init()

#if os.name == 'nt':
#    os.system('color')





def run_command(command):
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Start threads to continuously read and print stdout and stderr
        stdout_thread = threading.Thread(target=print_output, args=(process.stdout,))
        stderr_thread = threading.Thread(target=print_output, args=(process.stderr,))
        stdout_thread.start()
        stderr_thread.start()

        # Wait for the process to finish and threads to complete
        process.wait()
        stdout_thread.join()
        stderr_thread.join()

        return None  # No return value, as output is printed directly
    except Exception as e:
        return str(e)


def create_file(file_name):
    with open(file_name, 'w') as f:
        f.write('')



def current_date():
    print("Current date : " + str(time.day) + "/" + str(time.month) + "/" + str(time.year))

def current_time():
    print("Current time : " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second))

def run_script(script_path):
    """Execute a Python script."""
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError:
        print("Error executing the script.")





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

    command_completer = WordCompleter(["exit", "cd", "ls", "history", "up", "down", "help", "touch"])

    session = PromptSession(completer=command_completer, complete_while_typing=False, auto_suggest=AutoSuggestFromHistory())

    

    while True:
        try:
            user_input = session.prompt( os.getcwd() + "> ")
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

        if parts:
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
                

            

            elif command == "help":
                help_command()

            elif command == "touch":
                if arguments:
                    #try:
                    create_file(arguments[0])


            elif command == "cat":
                if not arguments:
                    print("Error: Usage: mkdir <folder_name>")
                elif len(arguments) == 1:
                    folder_name = arguments[0]
                    try:
                        os.mkdir(folder_name)
                    except FileExistsError:
                        print(f"Error: Folder '{folder_name}' already exists.")
                    except Exception as e:
                        print(f"Error: {e}")
                elif len(arguments) == 2 and arguments[1] == "-g":
                    folder_name = arguments[0]
                    try:
                        os.mkdir(folder_name)
                        os.chdir(folder_name)
                    except FileExistsError:
                        print(f"Error: Folder '{folder_name}' already exists.")
                    except FileNotFoundError:
                        print("Error: Invalid path.")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Error: Invalid arguments.")

            elif command == "ipconfig":
                
                # getting the hostname by socket.gethostname() method
                hostname = socket.gethostname()
                # getting the IP address using socket.gethostbyname() method
                ip_address = socket.gethostbyname(hostname)
                # printing the hostname and ip_address
                print(f"Hostname: {hostname}")
                print(f"IP Address: {ip_address}")

            elif command == "exit":
                break
            

            elif command == "cls":
                pass

            elif command == "date":
                current_date()

            elif command == "time":
                current_time()

            elif command == "run":
                if arguments:
                    run_command(" ".join(arguments))
                else:
                    print("Usage: run <command>")

            else:
                print("Invalid command. Type 'exit' to quit.")

    

if __name__ == "__main__":
    main()


""" 
Author: Anas Shakeel

run_project.py:
    A simple python script to run a django project locally {automatically}.
    Currently for Windows only!


How to use ?
    1. Place this script in root directory of a django project (where 'manage.py' is located)
    2. Open it in a text editor, and add the required libraries 'LIBRARIES' list OR change the settings in 'SETTINGS' dictionary.
    3. Run this script.
    
    (additionally, you can give the port number as command-line argument.)

"""

import random
import webbrowser
import sys
import os
from threading import Thread
from time import sleep


# This dictionary includes the settings.
SETTINGS = {
    'port': 8000,
    # Whether to ask for port number of not?
    'ASK_PORT': True,
    # Whether to select a random port for as default
    'RANDOM_PORT_AS_DEFAULT': False,
    # Whether to fetch the port number from cmd-line arguments or not
    'PORT_FROM_CMD_ARGS': False,
    # Port valid range 5,000 - 30,000
    'PORT_RANGE_MAX': 30000,
    'PORT_RANGE_MIN': 5000,
}

# This list contains the libraries required to run the project
LIBRARIES = [
    # Add your libraries here...
    'django',
]


def main():
    # Validate settings
    
    
    # Try to download all libraries (skips if already downloaded)
    try:
        for lib in LIBRARIES:
            res = os.system(f'pip install {lib}')
            if res == 1:
                print(
                    f"[ERROR] something went wrong while downloading '{lib}'")
                sys.exit(1)

    except ModuleNotFoundError as mnfe:
        print(f"[ERROR] {mnfe}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # If ask_port true, don't take cmd args
    if SETTINGS['ASK_PORT']:
        # Ask for a port number
        while True:
            try:
                inp = input("Port Number [3,000 - 30,000]: (leave empty for 8000) ")
                if inp == '':
                    if SETTINGS['RANDOM_PORT_AS_DEFAULT']:
                        SETTINGS['port'] = get_random_port()
                        print("[INFO] using default port now...")
                    break
                port = int(inp)
                if port > SETTINGS['PORT_RANGE_MAX'] or port < SETTINGS['PORT_RANGE_MIN']:
                    print(
                        "[ERROR] port number is not in a valid range (3,000 - 30,000)")
                    sys.exit(1)
                SETTINGS['port'] = port
                break
            except ValueError:
                print("[ERROR] invalid port number.")

    elif SETTINGS['PORT_FROM_CMD_ARGS']:
        # Get the command-line argument (port) if available
        if len(sys.argv) == 2:
            try:
                port = int(sys.argv[1])
                if port > SETTINGS['PORT_RANGE_MAX'] or port < SETTINGS['PORT_RANGE_MIN']:
                    print(
                        "[ERROR] port number is not in a valid range (3,000 - 30,000)")
                    sys.exit(1)
                SETTINGS['port'] = port
            except ValueError as e:
                print(f"[ERROR] {e}")
                sys.exit(1)

    elif SETTINGS['RANDOM_PORT_AS_DEFAULT']:
        # Select a random port number from a valid range
        SETTINGS['port'] = get_random_port()

    # Clear the screen
    os.system('cls')

    # Check if 'manage.py' available in the current dir
    if not os.path.exists('manage.py'):
        print(f"[ERROR] 'manage.py' not found in current directory.")
        sys.exit(1)

    # Entry point found
    print(f"[INFO] 'manage.py' found.")
    print(f"[INFO] PORT {SETTINGS['port']}.")

    # Create command and server_url
    command = f"python .\\manage.py runserver {SETTINGS['port']}"
    serve_url = f"http://127.0.0.1:{SETTINGS['port']}"

    # Start the browser thread
    server_thread = Thread(target=run_browser, args=(serve_url, 3))
    server_thread.start()

    # Run the server
    print(f"[INFO] running local http server now...")
    try:
        res = os.system(command)
        if res == 1:
            print("[ERROR] something went wrong! cannot start the server.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("[INFO] closing server now...")
        sys.exit(1)


def run_browser(url, delay=0):
    sleep(delay)
    webbrowser.open(url)


def get_random_port():
    return random.randint(SETTINGS['PORT_RANGE_MIN'], SETTINGS['PORT_RANGE_MAX'])

if __name__ == "__main__":
    main()

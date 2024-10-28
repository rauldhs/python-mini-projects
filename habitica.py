#!/usr/bin/env python
import requests
import json
import argparse
from decouple import config
import sys
from sys import stderr
from threading import Thread
from queue import Queue
from colorama import init, Fore

# Replace with your Habitica User ID and API Token
USER_ID = config("USER_ID")
API_TOKEN = config("API_TOKEN")
# API endpoint URLs
TASKS_URL = "https://habitica.com/api/v3/tasks/user"

black_wizard_ascii = """...........................................................................
...........................................................................
...........................................................................
...........................................................................
..............................................::::::.. ....................
...........................................:%@***#*%@@=:...................
.........................................%%#*=-=**%###%@@=.................
...................................  .*###=--==*#%%@%%@@@*.................
.................................==+%%+----===+*%@@*.......................
........................     .=%%**####=---=+***%@- .......................
..................:::::=%%%%%%*****#####%%%###**%%:........................
.............. =%%%####*+============+++%%%%%##%@. ........................
..............+@%###%%%%%%%#*+++====---==+***%%%@. ........................
..............-#@@%@@%@@@@@@@@@@@@%%*+++=-++*##%%@-........................
.................=##%@@@@@@@@@#@@@@@@@@@%%*++*+*##%=.......................
......................-@@@@@@%+#@@@@@%%%@@@@@#*+**##%-.....................
...................... . :%@@%+#@@@@%=-=%@@@@@@@@%###%%:...................
......................:%@@%@@@%@@@@@@#-=%@@@@@@@@@@@@@%%#-.................
......................-@%#%@@@@@@@@@@%*%%@@@%%%%%%@@@@@%#@- ...............
......................-@%##%@@@@@@@@@@@@@@%%%%%%%%%@@@@@%%- ...............
.....................  =@@%####@@@@@@**#####%@@@@@@@@@@@-  ................
.....................  =@@@@@**********#@@@@@@@#***%@@@: ..................
....................-#@#--+@@@######%%@@%##*+*#@%#**%@@@-..................
....................=%=*-=%%@@%%%%%%%%@@#=--=++#@###%%@@-..................
....................=#=-+%%%@@###%%%%%@@#*---==#@%%##%@@-..................
....................=%===*#%@@#######%%%@%---++#@%%%%%%@-..................
.....................=@%%%%@@@#########%@@%%%%@@@@%%%%#@-..................
......................-@@@@@@@%#########%@@@@@@@@@%%%%%@-..................
..................... :#@%@@@@%#########%@@@@@@@@@@%%%%@-..................
.......................=@#%@@@%%%#######%@@%@@@@@@@@%%%@-..................
.......................=@%%%@@@%%%####*##%@%%@@@@@@%%%%@-..................
.......................=@@%%@@@%%%%###*##%@%%%%%@@%%%%%@-..................
....................... -@%%@@@%%########%@@@%%%@@%@@@@@@#: ...............
....................... -@@@@@%##########%@@@@%%%@%@@@@@@@@*: .............
....................... -@@@@@############%@@@@@@@@@@@@@@@@@= .............
.........................-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=...............
..........................    .:::::::::::::::::::::::::.  ................
...........................................................................
"""

def update_completed_quests(file_path, quests_data):
    """
    Updates active quest from quests_data and writes it to the JSON file.
    """
    quest_to_check = quests_data["quests"][quests_data["active_quest"]]["name"]
    # Extract active quest name from quests_data
    
    # Set headers and parameters for the API request
    headers = {
        "x-api-user": USER_ID,
        "x-api-key": API_TOKEN
    }

    params = {
        "type": "completedTodos"
    }

    # Make the API request to get completed tasks
    response = requests.get(TASKS_URL, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        # Extract completed quest names from API response
        completed_quest_names = [quest["text"] for quest in response_data["data"]]
        if "# " + quest_to_check in completed_quest_names:
            # Update active quest from quests_data
            quests_data["active_quest"] += 1

            # Update the JSON file with modified quests_data
            with open(file_path, 'w') as json_file:
                json.dump(quests_data, json_file, indent=2)
            return
    else:
        stderr.write(Fore.RED + f"Request failed with status code: {response.status_code}")
        return False

def check_if_quest_active(quests_data):
    """
    Check if a specific quest is active and if the questline is started.
    """
    quest_to_check = quests_data["quests"][quests_data["active_quest"]]["name"]
    # Set headers and parameters for the API request
    headers = {
        "x-api-user": USER_ID,
        "x-api-key": API_TOKEN
    }

    params = {
        "type": "todos"
    }

    # Make the API request to get completed tasks
    response = requests.get(TASKS_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        response_data = response.json()
        # Extract active quest names from API response
        active_quest_names = [quest["text"] for quest in response_data["data"]]

        if "# " + quests_data["quest_line"]["name"] not in active_quest_names and quests_data["active_quest"] < len(quests_data["quests"]):
            add_quest_line(quests_data)
        if quest_to_check in active_quest_names:
             return True
    else:
        stderr.write(Fore.RED + f"Request failed with status code: {response.status_code}")
    
    return False

def add_quest_line(quest_data):
    """
    Add a new quest line using data from quests_data.
    """
    quest_data_to_add = quest_data["quest_line"]

    difficulty_values = {"Trivial": "0.1", "Easy": "1", "Medium": "1.5", "Hard": "2"}
    
    description = (
        f"## Quest Giver:\n{quest_data_to_add['quest_giver']}"
        f"\n\n## Description\n{quest_data_to_add['description']}"
        f"\n\n## Objective\n{quest_data_to_add['objective']}"
    )
    
    difficulty = difficulty_values[quest_data_to_add["difficulty"]] 

    # Set headers and parameters for the API request
    headers = {
        "x-api-user": USER_ID,
        "x-api-key": API_TOKEN
    }
    checklist = [
    {"text": quest["name"], "completed": False}
    for quest in quest_data["quests"]
    ]
    params = {
        "text": "# " + quest_data_to_add["name"],
        "notes": description,
        "type": "todo",
        "priority": difficulty,
        "checklist": checklist
    }

    # Make the API request to create a new quest line
    response = requests.post(TASKS_URL, json=params, headers=headers)
    
    if response.status_code != 201:
        stderr.write(Fore.RED + f"Failed to create a new quest, status code: '{response.status_code}'")

def add_quest(quest_data):
    """
    Add a new quest using data from quests_data.
    """
    quest_data_to_add = quest_data["quests"][quest_data["active_quest"]]
    difficulty_values = {"Trivial": "0.1", "Easy": "1", "Medium": "1.5", "Hard": "2"}
    
    description = (
        f"## Quest Giver:\n{quest_data_to_add['quest_giver']}"
        f"\n\n## Description\n{quest_data_to_add['description']}"
        f"\n\n## Objective\n{quest_data_to_add['objective']}"
    )
    
    difficulty = difficulty_values[quest_data_to_add["difficulty"]] 

    # Set headers and parameters for the API request
    headers = {
        "x-api-user": USER_ID,
        "x-api-key": API_TOKEN
    }

    params = {
        "text": "# " + quest_data_to_add["name"],
        "notes": description,
        "type": "todo",
        "priority": difficulty
    }

    # Make the API request to create a new quest
    response = requests.post(TASKS_URL, json=params, headers=headers)
    
    if response.status_code != 201:
        stderr.write(Fore.RED + f"Failed to create a new quest, status code: '{response.status_code}'")

def loading_animation(message,function_thread):
    animation = ['|', '/', '-', '\\']
    i = 0
    while function_thread.is_alive():
        sys.stdout.write(f'\r{message} {animation[i % len(animation)]}')
        sys.stdout.flush()
        i += 1
    sys.stdout.write(f'\r{message} \033[92mDone!\033[0m\n')

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-f', '--filepath', type=str, help='Path to the file')
    args = parser.parse_args()

    if args.filepath:
        # Load quests_data from the specified JSON file
        with open(args.filepath, 'r') as file:
            quests_data = json.load(file)

        print(black_wizard_ascii)

        # Call the function to process completed tasks
        # Threading update_completed_quests function
        update_completed_quests_thread = Thread(target=update_completed_quests, args=(args.filepath, quests_data))
        update_completed_quests_thread.start()
        loading_animation("Updating quests", update_completed_quests_thread)
        update_completed_quests_thread.join()
        

        result_queue = Queue()
        check_quest_thread = Thread(target=lambda q, quests_data: q.put(check_if_quest_active(quests_data)), args=(result_queue, quests_data))
        check_quest_thread.start()
        loading_animation("Checking quests", check_quest_thread)
        check_quest_thread.join()
        quest_active = result_queue.get()

        # Threading add_quest function
        if not quest_active:

            add_quest_thread = Thread(target=add_quest, args=(quests_data,))
            add_quest_thread.start()
            loading_animation("Starting new quest", add_quest_thread)
            add_quest_thread.join()
        else:
            print("Quest is active")
    else:
        
        print(black_wizard_ascii)
        print("use -f to check json files")
if __name__ == '__main__':
    main()

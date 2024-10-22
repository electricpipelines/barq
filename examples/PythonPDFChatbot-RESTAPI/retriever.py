import uuid
import time
import os
import threading
import sys
import itertools
import requests
import ollama
from colorama import Fore, Back, Style

def serialize_response(json_string, directory='./retrievals/'):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate a unique filename using timestamp and UUID
    unique_filename = f"{int(time.time())}_{uuid.uuid4()}.json"
    file_path = os.path.join(directory, unique_filename)

    # Write the JSON string to the file
    with open(file_path, 'w') as file:
        file.write(json_string)

    # Provide the link to the file
    print(Fore.LIGHTBLUE_EX + f"Retrieved info has been save to {file_path}" + Style.RESET_ALL)
    print("___")
    print()
    return file_path

def convert_prompt_to_retrieval_prompt(prompt, prompt_template, model="llama3"):
    # llm = Ollama(
    #         model=model,
    #         temperature=0
    #     )
    # response = llm.invoke(f"Take the user's prompt to create a prompt for a semantic database retriever. Only respond with a list of comma-separated keywords. DO NOT say anything before or afer the keywords.#Prompt:{prompt}")
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': f"Take the user's prompt to create a prompt for a semantic database retriever. Only respond with a list of comma-separated keywords. DO NOT say anything before or afer the keywords.#Prompt:{prompt}",
    },
    ])
    return response

def display_spinner_and_wait_message(stop_event, message=""):
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    while not stop_event.is_set():  # Check the stop event
        sys.stdout.write('\r' + Fore.YELLOW + message + next(spinner) + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.1)
        # Clear the spinner line when done
    sys.stdout.write('\r \r')  
    sys.stdout.flush()


def retrieve_data(prompt, memory_bank, query_limit=10):
    stop_event = threading.Event()
    t = threading.Thread(target=display_spinner_and_wait_message, args=(stop_event, "Retrieving info from database..."))
    t.start()

    url = "http://localhost:6568/api/silk/query"
    params = {
        "q": prompt,
        "limit": query_limit,
        "memorybank": memory_bank  # Changed from "memoryBank" to "memorybank"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        serialize_response(response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        stop_event.set()  # Signal the spinner thread to stop
        t.join()  # Wait for the spinner thread to finish
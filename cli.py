import requests
import json
import sys
import subprocess
import os
from dotenv import load_dotenv

# Check if an argument is provided
if len(sys.argv) != 2:
    print("Usage: python script_name.py <input>")
    sys.exit(1)

user_input = sys.argv[1]

# API endpoint URL
url = "https://app.cognitgpt.com/api/llm"

# API key for authorization
load_dotenv()
api_key = os.environ.get("COGNITGPT_API_KEY")

# Headers with the required `Content-Type` and `Authorization`
headers = {
    "Authorization": f"ApiKey {api_key}",
    "Content-Type": "application/json"
}

# Data payload for the POST request
data = {
    "messages": [
        {"role": "system", "content": "You respond with nothing except a directly executable linux CLI command. You respond with just 1 line. You don't use markdown."},
        {"role": "user", "content": f"{user_input}"},
    ],
    "model": "gpt-4o",
    "max_tokens": 200,
    "temperature": 0.7
}

# Make the POST request to the API
response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

# Initialize command to an empty string
command = ""

# Check if the request was successful
if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            try:
                # parse the {"type": "content", "value": " and"} data
                data = json.loads(decoded_line)
                command += data["value"]

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
    # Print the command
    print(command)

    # Execute the command using subprocess
    try:
        confirm = input("Do you want to execute this command? (y/n): ")
        if confirm.lower() == 'y':
            # Execute the command
            # Using subprocess.run to execute the command
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            print("Exiting...")
            sys.exit(1)
        # Print the result of the command execution
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")

else:
    # Print the error
    print(f"Failed to get a response, status code: {response.status_code}")
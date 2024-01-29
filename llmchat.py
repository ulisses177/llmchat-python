from openai import OpenAI
import yaml
import random
import os
import networkx as nx

# Import main function from cliquesinhistorysum
from cliquesinhistorysum import main as cliques_main

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Define default chat log content
default_content = [
    {"role": "system", "content": "You are Cleo, an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful. You are witty but not sassy, a bit even quirky, but always with good intent."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    {"role": "assistant", "content": "Hi there! I'm Cleo, your friendly intelligent assistant. I'm here to help you with any questions you have. Feel free to ask away!"}
]

# Function to load or create chat log from YAML file
def load_or_create_chatlog(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    else:
        with open(file_path, "w") as file:
            yaml.dump(default_content, file)
        return default_content

# Load or create chat history from YAML file
chatlog_path = "chatlog.yaml"
graph_path="graph.yaml"
chatlog=load_or_create_chatlog(chatlog_path)

# Run cliquesinhistorysum.py script
#cliques_main()

history = load_or_create_chatlog(graph_path)

while True:
    # Filter out messages with empty or missing 'content' field
    # Remove empty content messages from history
    history = [message for message in history if isinstance(message, dict) and message.get("content", "").strip()]

    # Filter out messages with empty or missing 'content' field
    filtered_history = [{"role": message["role"], "content": message.get("content", "")} for message in history]

    #print("Filtered History:", filtered_history)  # Debug print

    # Check if the messages array is not empty before making the API request
    if filtered_history:
        completion = client.chat.completions.create(
            model="local-model", # this field is currently unused
            messages=filtered_history,
            temperature=0.7,
            stream=True,
        )
    else:
        print("Warning: 'messages' array is empty. Skipping API request.")
        completion = []

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    print()
    user_input = input("> ")
    if user_input.strip().lower() == "exit":
        break
    
    history.append({"role": "user", "content": user_input})
    
    # Save chat log to YAML file after each interaction
    with open(chatlog_path, "w") as file:
        yaml.dump(history, file)

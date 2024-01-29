import os
import yaml
import networkx as nx
import nltk
from openai import OpenAI
import re
import matplotlib.pyplot as plt

# Load chat history
def load_chat_history():
    if os.path.exists('chatlog.yaml'):
        with open('chatlog.yaml', 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    else:
        return []

# Function to sanitize text
def sanitize_text(text):
    # Remove any characters that might cause issues in the graph
    sanitized_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove leading/trailing whitespace
    sanitized_text = sanitized_text.strip()
    return sanitized_text

# Function to call OpenAI API for summarization
def summarize_clique(clique_words, persona):
    openai = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")  # Initialize OpenAI instance with local server
    prompt = f"These are some of the co-occurrences and patterns that are found throughout my memories, considering I am {persona}. These are probably about: {', '.join(clique_words)} "
    completion = openai.completions.create(
        model="local-model",  # Use the local model
        prompt=prompt,
        temperature=0.7,
        max_tokens=252
    )
    summary_text = completion.choices[0].text.strip()
    # Sanitize the summary text
    sanitized_summary = sanitize_text(summary_text)
    return sanitized_summary

# Save graph to file
def save_graph(graph):
    graph_data = nx.node_link_data(graph)
    with open('graph.yaml', 'w') as file:
        yaml.dump(graph_data, file)

# Load or create graph
def load_or_create_graph():
    if os.path.exists('graph.yaml'):
        with open('graph.yaml', 'r') as file:
            graph_data = yaml.load(file, Loader=yaml.FullLoader)
            return nx.node_link_graph(graph_data)
    else:
        return nx.Graph()  # Initialize as a NetworkX graph

def main():
    # Create a graph
    G = load_or_create_graph()

    # Load chat history
    history = load_chat_history()

    # Filtered History
    filtered_history = [{'role': message['role'], 'content': message['content']} for message in history if message.get('content')]

    # Add nodes and edges to the graph
    for message in filtered_history:
        content = message["content"].lower()  # Convert to lowercase
        if not content.strip():  # Skip empty content
            continue
        words = nltk.word_tokenize(content)
        for word in words:
            if word not in G:
                G.add_node(word, content=content)
            for other_word in words:
                if other_word != word and other_word in G:
                    G.add_edge(word, other_word)

    # Now G is a graph where each node is a word from the chat history,
    # and there is an edge between two words if they appear in the same message.

    # Find all cliques
    cliques = list(nx.find_cliques(G))

    # Filter cliques to only include those of size greater than 2
    large_cliques = [clique for clique in cliques if len(clique) > 2]

    # Process each clique
    for i, clique in enumerate(large_cliques):
        clique_words = [word for word in clique if word in G]  # Filter out non-existing words
        if clique_words:
            # Call OpenAI API to summarize clique
            clique_summary = summarize_clique(clique_words, "current persona")

            # Add summarized clique as new vertex to the graph
            new_vertex = " ".join(clique_words)
            G.add_node(new_vertex, summary=clique_summary)
            for word in clique_words:
                for neighbor in G[word]:
                    if neighbor != new_vertex:
                        G.add_edge(new_vertex, neighbor)
                G.remove_node(word)

            # Plot the subgraph for this clique
            subgraph = G.subgraph(clique_words + [new_vertex])
            nx.draw(subgraph, with_labels=True)
            plt.savefig(f"clique_{i}.png")  # Save the plot to a file
            plt.close()

    # Save graph to file
    save_graph(G)

if __name__ == "__main__":
    main()

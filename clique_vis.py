import networkx as nx
import matplotlib.pyplot as plt
import random
import yaml

def add_random_edges(graph, num_edges):
    nodes = list(graph.nodes())
    if len(nodes) < 2:
        print("Not enough nodes to add edges.")
        return

    for _ in range(num_edges):
        edge = random.sample(nodes, 2)
        graph.add_edge(*edge)


def find_cliques(graph, min_clique_size=3):
    cliques = [clique for clique in nx.find_cliques(graph) if len(clique) >= min_clique_size]
    
     # Collapse each clique into a single vertex
    for clique in list(cliques):  # Iterate over a copy to avoid modifying the original list during iteration
        subgraph = graph.subgraph(list(clique))  # Create a subgraph of the current clique
        new_vertex = max(subgraph.nodes()) + 1
        
        graph.add_node(new_vertex)    # Add the new vertex to the graph
        
        for node in subgraph.nodes():  # Iterate over each node in the subgraph
            if node not in clique:   # If the node is not part of the original clique
                graph.add_edge(node, new_vertex)   # Add an edge from the node to the new vertex
            else:
                graph.add_edge(new_vertex, node)   # Add an edge from the new vertex to the node
        

    
    return cliques


def plot_graph(graph, cliques):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold')

    # Draw nodes with increased size and transparency for cliques
    for clique in cliques:
        nx.draw_networkx_nodes(graph, pos, nodelist=clique, node_size=800, node_color='r', alpha=0.8)

        # Draw edges of the clique with a different color
        edge_list = [(clique[i], clique[i + 1]) for i in range(len(clique) - 1)]
        edge_list.append((clique[-1], clique[0]))  # Add the last edge
        nx.draw_networkx_edges(graph, pos, edgelist=edge_list, edge_color='r', width=2)

    plt.show()

def load_graph_from_yaml(filename):
    try:
        with open(filename, "r") as f:
            graph_dict = yaml.safe_load(f)
            G = nx.from_dict_of_dicts(graph_dict)
            cliques = find_cliques(G, min_clique_size=3)
            return G, cliques
    except FileNotFoundError:
        print("File not found. Creating a new graph.")
        return None

def save_graph_to_yaml(G, filename):
    graph_dict = nx.to_dict_of_dicts(G)
    with open(filename, "w") as f:
        yaml.dump(graph_dict, f)

if __name__ == "__main__":
    filename = "graph-vis.yaml"
    G, cliques = load_graph_from_yaml(filename)
    if G is None or True:
        # Create a sample graph with nodes
        G = nx.Graph()
        G.add_nodes_from(range(1, 40))  # Add nodes 1 through 7

        # Add random edges to the graph (make sure num_edges <= len(G.nodes)/2)
        num_edges = 10*10
        add_random_edges(G, num_edges)

        # Find cliques in the graph (min_clique_size=3)
        cliques = find_cliques(G, min_clique_size=3)

        # Print the cliques
        print("Cliques:", cliques)

        # Save the graph to a YAML file
        save_graph_to_yaml(G, filename)

    # Plot the graph with cliques highlighted
    plot_graph(G, cliques)

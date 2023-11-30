#%%
import networkx as nx
import matplotlib.pyplot as plt
import collections

def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        source, target, num_edges = map(int, lines[0].split())
        edges = [tuple(map(int, line.split())) for line in lines[1:]]

    graph = nx.DiGraph()
    graph.add_nodes_from(range(source, target + 1))
    graph.add_edges_from([(u, v, {'capacity': c, 'flow': 0}) for u, v, c in edges])

    return graph, source, target

def visualize_graph(graph, levels=None, path=None, title="Graph"):
    pos = nx.spring_layout(graph)

    if levels:
        node_colors = [levels[node] for node in graph.nodes()]
        edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
        nx.draw(graph, pos, with_labels=True, font_weight='bold', node_color=node_colors, cmap=plt.cm.Blues, width=2)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    elif path:
        edge_colors = ['red' if edge in path else 'black' for edge in graph.edges()]
        nx.draw(graph, pos, with_labels=True, font_weight='bold', edge_color=edge_colors, width=2)
    else:
        edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
        nx.draw(graph, pos, with_labels=True, font_weight='bold', width=2)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

    plt.title(title)
    plt.show()

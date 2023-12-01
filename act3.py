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

def calculate_levels(graph, source):
    levels = {source: 0}
    queue = collections.deque([source])

    while queue:
        current_node = queue.popleft()
        for successor in graph.successors(current_node):
            if successor not in levels:
                levels[successor] = levels[current_node] + 1
                queue.append(successor)

    return levels

def visualize_graph_with_levels(graph, levels, title="Graph with Levels"):
    pos = nx.spring_layout(graph)
    node_colors = [levels[node] for node in graph.nodes()]
    edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_color=node_colors, cmap=plt.cm.Blues)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    for node, (x, y) in pos.items():
        plt.text(x, y, f"Level: {levels[node]}", fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.title(title)
    plt.show()
def bfs(graph, source, target):
    visited = set()
    queue = collections.deque([(source, [source])])

    while queue:
        current_node, path = queue.popleft()
        visited.add(current_node)

        for successor in graph.successors(current_node):
            if successor not in visited and graph[current_node][successor]['capacity'] > 0:
                if successor == target:
                    return path + [successor]
                queue.append((successor, path + [successor]))

    return []

def update_flow(graph, path):
    min_capacity = min(graph[u][v]['capacity'] for u, v in zip(path[:-1], path[1:]))
    
    for u, v in zip(path[:-1], path[1:]):
        graph[u][v]['capacity'] -= min_capacity
        graph[u][v]['flow'] += min_capacity

        if v in graph:
            if u in graph[v]:
                graph[v][u]['capacity'] += min_capacity
                graph[v][u]['flow'] -= min_capacity
            else:
                graph.add_edge(v, u, capacity=min_capacity, flow=-min_capacity)

def dinic(graph, source, target):
    levels = calculate_levels(graph, source)
    visualize_graph_with_levels(graph, levels, title="Graph with Levels (Before Dinic)")

    while levels[target] is not None:
        path = bfs(graph, source, target)

        if not path:
            break

        visualize_graph(graph, path=path, title="Graph with Augmenting Path")
        update_flow(graph, path)

        levels = calculate_levels(graph, source)
        visualize_graph_with_levels(graph, levels, title="Graph with Updated Levels")
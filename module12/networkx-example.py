import networkx as nx
from google.cloud import spanner

instance_id = "INSERT YOUR INSTANCE ID"
database_id = "INSERT YOUR DATABASE NAME"

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

def get_network_graph():
    G = nx.Graph()
    with database.snapshot() as snapshot:
        # Assuming you have a 'network_edges' table with 'source', 'destination', and 'latency' columns
        results = snapshot.execute_sql("""
            graph network
            match -[e]-
            return e.router_id, e.to_router_id, e.latency""")
        for row in results:
            source, destination, latency = row
            G.add_edge(source, destination, weight=latency)
    return G

def find_shortest_path(graph, source, target):
    try:
        path = nx.shortest_path(graph, source=source, target=target, weight='weight')
        path_latency = nx.shortest_path_length(graph, source=source, target=target, weight='weight')
        print(f"Shortest path from {source} to {target}: {path}")
        print(f"Total latency: {path_latency}")
    except nx.NetworkXNoPath:
        print(f"No path found from {source} to {target}.")
    except nx.NodeNotFound:
        print("Source or target node not found in the graph.")

if __name__ == "__main__":
    network_graph = get_network_graph()

    # Example usage: Find the shortest path between two nodes
    # Replace 'node_A' and 'node_B' with actual node names from your network_edges table
    find_shortest_path(network_graph, 'edge1', 'edge8')

# Module 12 - Graph Algorithms

In this module you will use an external tool to run algorithms on a graph stored in Spanner.

## Graph algorithms using NetworkX

The example identifies the path with the lowest latency between two edge routers.

The script first retrieves the graph from Spanner in the `get_network_graph` method.
The method retrieves all the edges with source, destination and latency, in tabular form.

The script retrieves the entire graph because it is particularly small. For larger graphs it is recommended to attempt extracting a subgraph, when possible.

After retrieving the graph, the script computes the shorted path, based on latency, using NetworkX's native capabilities.

Review the code in `networkx-example.py`

To run the example first edit `networkx-example.py`

- Replace `INSERT YOUR INSTANCE ID` with the ID of the Spanner instance. 
- Replace `INSERT YOUR DATABASE NAME` with the name of the database.

Run the following commands in Cloud Shell to execute the code.

```shell
cd module12
pip install -r requirements.txt
python networkx-example.py
```
# Module 13 - Agents - Activity 3

In this activity you query Spanner with the MCP Toolbox.

## Setup

Download the MCP Toolbox binary.

```shell
cd ~/agent
wget https://storage.googleapis.com/genai-toolbox/v0.16.0/linux/amd64/toolbox
chmod +x toolbox
```

Create the toolbox configuration file.

```shell
cd ~/agent
touch tools.yaml
```

## Configure MCP Toolbox

Insert the following code in `tools.yaml`.

- Replace the value of `project`
- Replace the value of `instance`

```yaml
sources:
  my-spanner:
    kind: spanner
    project: my-project
    instance: my-instance
    database: agent
tools:
  get-customer-info:
    kind: spanner-sql
    source: my-spanner
    statement: |
      SELECT *
      FROM customers
      WHERE name = @customername
    description: |
      Use this tool to get information about a customer by name. The information include customer ID, name, email and address.
    parameters:
      - name: customername
        type: string
        description: Customer name
  get-customer-tickets:
    kind: spanner-sql
    source: my-spanner
    statement: |
      SELECT
        t.*
      FROM
        customers c
        INNER JOIN support_tickets t
          ON c.customer_id = t.customer_id
      WHERE
        c.name = @customername
    description: |
      Use this tool to get the tickets opened by a customer based on customer name.
    parameters:
      - name: customername
        type: string
        description: Customer name
  get-ticket-metrics:
    kind: spanner-sql
    source: my-spanner
    statement: |
      graph access_network
      match 
        (ticket:support_ticket{ticket_id:@ticket_id})
        -[related_to]->(:customer_device)
        <-[connected]-(pt:port)
        <-[`contains`]-(an:access_node)
        return ticket,an, pt
      next
        match  (an)-[has_temperature]->(tmpr:access_node_temperature)
        where tmpr.timestamp between ticket.created_at and ticket.updated_at
        return max(tmpr.temperature_celsius) as max_temp, ticket, pt
      next
        match (pt)-[has_performance]->(ptperf:port_performance)
        where ptperf.timestamp between ticket.created_at and ticket.updated_at
        return
          max_temp,
          avg(ptperf.bytes_sent) as avg_bytes_sent,
          avg(ptperf.bytes_received) as avg_bytes_received
    description: |
      Use this tool to get temperature and performance metrics related to a ticket.
    parameters:
      - name: ticket_id
        type: string
        description: Ticket ID

toolsets:
  customer-toolset:
    - get-customer-info
    - get-customer-tickets
    - get-ticket-metrics

```

## Modify the agent to use MCP Toolbox

Modify `agent.py` to use the following code.

```python
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_agent = Agent(
    name = "root_agent",
    model = "gemini-2.5-flash",
    description = (
        "Agent to retrieve customer information"
    ),
    instruction = (
        """You are a helpful agent that can answer questions about customers,
        customer tickets
        and information about tickets (including temperatures and performance information).
        """
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='./toolbox',
                    args=[
                        "--stdio",
                        "--tools-file",
                        "./tools.yaml",
                    ]
                )
            )
        )
    ]
)
```

## Test the agent

Start ADK:

```shell
cd ~/agent
adk web
```

Run the following query in Spanner Studio to obtain some customer names to test.

```sql
SELECT c.name
FROM customers c
     INNER JOIN support_tickets t
         ON c.customer_id = t.customer_id
LIMIT 10
```

Back to ADK, try a prompt like the following, using one of the names obtained above.

> Give me the address of John Smith

> What are the tickets opened by John Smith

> give me temperature and performance metrics associated with ticket 2aa15e43-8844-44aa-8be2-732a43d7ba15

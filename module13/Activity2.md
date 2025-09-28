# Module 13 - Agents - Activity 2

In this activity you query Spanner with ADK's Built-in Tools for Spanner.

## Setup

From within module13 directory, run the following command to create a new Spanner database with schema and data.

> [!NOTE] 
> The script creates a database named `agent`. If the database already exists, it
> is dropped and recreated.

- Replace the value of `PROJECT_ID`
- Replace the value of `INSTANCE_ID`

```shell
PROJECT_ID=my-project INSTANCE_ID=my-instance DATABASE_ID=agent ./setup_spanner.sh
```

## Try Built-in Tools for Spanner

Modify `agent.py` using the following code.

```python
from google.adk.agents import Agent
from google.adk.tools.spanner.spanner_toolset import SpannerToolset

spanner_toolset = SpannerToolset()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction="""You are a helpful agent that answers 
        questions about Spanner tables and execute queries.""",
    tools=[spanner_toolset]
)
```

Start ADK:

```shell
cd ~/agents
adk web
```

Try prompts like these.

> List the tables of the agent database in instance my-instance, project my-project

> select 10 records from the customers table

> select the first 10 records from support_tickets with a corresponding record in customers. return the customer name, the ticket ID and the ticket status

### Stop the agent

1. Close the browser tab of the agent.
2. Return to the shell that is running `adk web`.
3. Press `Control+C` to stop `adk`.

## Invoke Built-in Tools for Spanner from a function tool

Modify `agent.py` using the following code.

- Replace the value of `PROJECT_ID`
- Replace the value of `INSTANCE_ID`

```python
from google.adk.agents import Agent
from google.adk.tools.google_tool import GoogleTool
from google.adk.tools.spanner import query_tool
from google.adk.tools.spanner.settings import Capabilities
from google.adk.tools.spanner.settings import SpannerToolSettings
from google.adk.tools.spanner.spanner_credentials import SpannerCredentialsConfig
from google.adk.tools.tool_context import ToolContext
from google.auth.credentials import Credentials
import google.auth

PROJECT_ID='mt-workshop'
INSTANCE_ID='spanner-ws'
DATABASE_ID='test'

application_default_credentials, _ = google.auth.default()
credentials_config = SpannerCredentialsConfig(
    credentials=application_default_credentials
)

tool_settings = SpannerToolSettings(capabilities=[Capabilities.DATA_READ])

def get_customer(
    name:str,
    credentials: Credentials,  # GoogleTool handles `credentials`
    settings: SpannerToolSettings,  # GoogleTool handles `settings`
    tool_context: ToolContext,  # GoogleTool handles `tool_context`
    ):
    """Returns information about a customer by name

    Args:
        None

    Returns:
        A single customer record including fields customer_id, name, email, address
    """

    return query_tool.execute_sql(
        project_id=PROJECT_ID,
        instance_id=INSTANCE_ID,
        database_id=DATABASE_ID,
        query=f"SELECT * FROM customers WHERE LOWER(name)=LOWER('{name}');",
        credentials=credentials,
        settings=settings,
        tool_context=tool_context,
    )

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction="""You are a helpful agent that answers 
        questions about customers.""",
    tools=[
        GoogleTool(
            func=get_customer,
            credentials_config=credentials_config,
            tool_settings=tool_settings,
        )]
)
```

Start ADK:

```shell
cd ~/agents
adk web
```

The Spanner database has been populated with random values.

In order to find existing customer names for testing, go to Spanner Studio and run a query like this.

```sql
SELECT name FROM customers LIMIT 10;
```

Back to ADK, try a prompt like the following, using one of the names obtained above.

> Give me the address of John Smith

### Stop the agent

1. Close the browser tab of the agent.
2. Return to the shell that is running `adk web`.
3. Press `Control+C` to stop `adk`.
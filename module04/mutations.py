from google.cloud import spanner

instance_id = "INSERT YOUR INSTANCE ID"
database_id = "INSERT YOUR DATABASE NAME"

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

def execute_mutation(transaction):
    transaction.insert(
        table="users",
        columns=("username", "location", "age"),
        values=[
            ('John Doe', 'US', 23),
            ('Matti Meikäläinen','Finland',71),
        ],
    )
    print("Inserted data.")

database.run_in_transaction(execute_mutation)
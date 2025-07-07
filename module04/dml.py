from google.cloud import spanner

instance_id = "INSERT YOUR INSTANCE ID"
database_id = "INSERT YOUR DATABASE NAME"

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

def execute_dml(transaction):
    row_count = transaction.execute_update("INSERT INTO users(username, location, age) VALUES('Taro Yamada','Japan',30);")
    print(f"{row_count} row(s) inserted.")

database.run_in_transaction(execute_dml)
print("DML statement executed successfully.")
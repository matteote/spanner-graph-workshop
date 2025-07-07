from google.cloud import spanner

instance_id = "INSERT YOUR INSTANCE ID"
database_id = "INSERT YOUR DATABASE NAME"

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

with database.snapshot() as snapshot:
    keyset = spanner.KeySet(all_=True)
    results = snapshot.read(
        table="users",
        columns=['user_id','username','location','age'],
        keyset=keyset
    )

    print(f"Data from table users:")
    for row in results:
        print(row)
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
import os
from google.cloud import spanner


# --- Main execution ---
def main():
    PROJECT_ID = os.environ.get('PROJECT_ID')
    INSTANCE_ID = os.environ.get('INSTANCE_ID')
    DATABASE_ID = os.environ.get('DATABASE_ID')

    if not all([PROJECT_ID, INSTANCE_ID, DATABASE_ID]):
        print("Error: Please set the environment variables PROJECT_ID, INSTANCE_ID, and DATABASE_ID.")
        exit(1)

    spanner_client = spanner.Client(project=PROJECT_ID)
    instance = spanner_client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    fake = Faker()

    # Generate data
    access_node = []
    port = []
    customer_device = []
    customer = []
    support_ticket = []
    port_performance = []
    access_node_temperature = []

    # Generate Access Nodes
    for _ in range(10):
        access_node_id = str(uuid.uuid4())
        access_node.append({
            'access_node_id': access_node_id,
            'name': f'access-node-{fake.word()}',
            'location': fake.address(),
            'ip_address': fake.ipv4(),
            'mac_address': fake.mac_address(),
        })

        # Generate Access Node Temperature Data for the last month
        for day in range(30):
            for hour in range(24):
                timestamp = datetime.now() - timedelta(days=day, hours=hour)
                access_node_temperature.append({
                    'access_node_id': access_node_id,
                    'timestamp': timestamp,
                    'temperature_celsius': random.uniform(5.0, 30.0)
                })

    # Generate Ports, Customer Devices, and Customers
    for an in access_node:
        for i in range(42):
            port_number = i + 1
            port.append({
                'access_node_id': an['access_node_id'],
                'port_number': port_number,
            })

            # Generate Port Performance Data for the last month
            for day in range(30):
                for hour in range(24):
                    timestamp = datetime.now() - timedelta(days=day, hours=hour)
                    port_performance.append({
                        'access_node_id': an['access_node_id'],
                        'port_number': port_number,
                        'timestamp': timestamp,
                        'bytes_sent': random.randint(1000000, 1000000000),
                        'bytes_received': random.randint(1000000, 1000000000),
                        'packets_sent': random.randint(1000, 1000000),
                        'packets_received': random.randint(1000, 1000000),
                        'status': random.choice(['up', 'down', 'maintenance'])
                    })

            customer_id = str(uuid.uuid4())
            customer.append({
                'customer_id': customer_id,
                'name': fake.name(),
                'email': fake.email(),
                'address': fake.address(),
            })

            device_id = str(uuid.uuid4())
            customer_device.append({
                'device_id': device_id,
                'customer_id': customer_id,
                'access_node_id': an['access_node_id'],
                'port_number': port_number,
                'model': random.choice(['ADSL', 'VDSL']),
                'serial_number': fake.ean(length=13),
                'status': random.choice(['online', 'offline']),
            })

    # Generate Support Tickets
    for _ in range(20):
        c = random.choice(customer)
        device = next((d for d in customer_device if d['customer_id'] == c['customer_id']), None)
        if device:
            created_at = datetime.now() - timedelta(days=random.randint(0, 29),
                                                    hours=random.randint(0, 23),
                                                    minutes=random.randint(0, 59),
                                                    seconds=random.randint(0, 59))
            updated_at = created_at + timedelta(hours=random.randint(0, 23),
                                                 minutes=random.randint(0, 59),
                                                 seconds=random.randint(0, 59))
            if updated_at > datetime.now():
                updated_at = datetime.now()

            support_ticket.append({
                'ticket_id': str(uuid.uuid4()),
                'customer_id': c['customer_id'],
                'device_id': device['device_id'],
                'issue_description': 'Internet connection is not working.',
                'status': random.choice(['open', 'closed', 'in_progress']),
                'created_at': created_at,
                'updated_at': updated_at,
            })

    # Insert data into Spanner
    with database.batch() as batch:
        batch.insert(
            table='access_nodes',
            columns=('access_node_id', 'name', 'location', 'ip_address', 'mac_address'),
            values=[(
                an['access_node_id'], an['name'], an['location'], an['ip_address'], an['mac_address']
            ) for an in access_node]
        )
    print("writing access_node")

    with database.batch() as batch:
        batch.insert(
            table='ports',
            columns=('access_node_id', 'port_number'),
            values=[(
                p['access_node_id'], p['port_number']
            ) for p in port]
        )
    print("writing port")

    with database.batch() as batch:
        batch.insert(
            table='customers',
            columns=('customer_id', 'name', 'email', 'address'),
            values=[(
                c['customer_id'], c['name'], c['email'], c['address']
            ) for c in customer]
        )
    print("writing customer")

    with database.batch() as batch:
        batch.insert(
            table='customer_devices',
            columns=('device_id', 'customer_id', 'access_node_id', 'port_number', 'model', 'serial_number', 'status'),
            values=[(
                cd['device_id'], cd['customer_id'], cd['access_node_id'], cd['port_number'], cd['model'], cd['serial_number'], cd['status']
            ) for cd in customer_device]
        )
    print("writing customer_device")

    with database.batch() as batch:
        batch.insert(
            table='support_tickets',
            columns=('ticket_id', 'customer_id', 'device_id', 'issue_description', 'status', 'created_at', 'updated_at'),
            values=[(
                st['ticket_id'], st['customer_id'], st['device_id'], st['issue_description'], st['status'], st['created_at'], st['updated_at']
            ) for st in support_ticket]
        )
    print("writing support_ticket")

    with database.batch() as batch:
        batch.insert(
            table='access_node_temperatures',
            columns=('access_node_id', 'timestamp', 'temperature_celsius'),
            values=[(
                ant['access_node_id'], ant['timestamp'], ant['temperature_celsius']
            ) for ant in access_node_temperature]
        )
    print("writing access_node_temperature")

    # Chunk insert for port_performance
    chunk_size = 10000
    for i in range(0, len(port_performance), chunk_size):
        chunk = port_performance[i:i + chunk_size]
        with database.batch() as batch:
            batch.insert(
                table='port_performance',
                columns=('access_node_id', 'port_number', 'timestamp', 'bytes_sent', 'bytes_received', 'packets_sent', 'packets_received', 'status'),
                values=[(
                    pp['access_node_id'], pp['port_number'], pp['timestamp'], pp['bytes_sent'], pp['bytes_received'], pp['packets_sent'], pp['packets_received'], pp['status']
                ) for pp in chunk]
            )
        print(f"writing port_performance chunk {i // chunk_size + 1}")

    print("Data inserted successfully.")

if __name__ == '__main__':
    main()

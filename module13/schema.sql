CREATE TABLE access_nodes (
    access_node_id STRING(36) NOT NULL,
    name STRING(255) NOT NULL,
    location STRING(255),
    ip_address STRING(45),
    mac_address STRING(17)
) PRIMARY KEY(access_node_id);

CREATE TABLE ports (
    access_node_id STRING(36) NOT NULL,
    port_number INT64 NOT NULL,
    CONSTRAINT fk_access_node FOREIGN KEY (access_node_id) REFERENCES access_nodes (access_node_id)
) PRIMARY KEY(access_node_id, port_number);

CREATE TABLE port_performance (
    access_node_id STRING(36) NOT NULL,
    port_number INT64 NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    bytes_sent INT64,
    bytes_received INT64,
    packets_sent INT64,
    packets_received INT64,
    status STRING(50),
    CONSTRAINT fk_port FOREIGN KEY (access_node_id, port_number) REFERENCES ports (access_node_id, port_number)
) PRIMARY KEY(access_node_id, port_number, timestamp);

CREATE TABLE access_node_temperatures (
    access_node_id STRING(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature_celsius FLOAT64,
    CONSTRAINT fk_access_node_temp FOREIGN KEY (access_node_id) REFERENCES access_nodes (access_node_id)
) PRIMARY KEY(access_node_id, timestamp);

CREATE TABLE customers (
    customer_id STRING(36) NOT NULL,
    name STRING(255) NOT NULL,
    email STRING(255),
    address STRING(1024)
) PRIMARY KEY(customer_id);

CREATE TABLE customer_devices (
    device_id STRING(36) NOT NULL,
    customer_id STRING(36) NOT NULL,
    access_node_id STRING(36) NOT NULL,
    port_number INT64 NOT NULL,
    model STRING(255),
    serial_number STRING(255),
    status STRING(50),
    CONSTRAINT fk_customer_devices FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    CONSTRAINT fk_port_devices FOREIGN KEY (access_node_id, port_number) REFERENCES ports (access_node_id, port_number)
) PRIMARY KEY(device_id);

CREATE TABLE support_tickets (
    ticket_id STRING(36) NOT NULL,
    customer_id STRING(36) NOT NULL,
    device_id STRING(36),
    issue_description STRING(MAX) NOT NULL,
    status STRING(50),
    created_at TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp = true),
    updated_at TIMESTAMP NOT NULL OPTIONS(allow_commit_timestamp = true),
    CONSTRAINT fk_customer_tickets FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    CONSTRAINT fk_device FOREIGN KEY (device_id) REFERENCES customer_devices (device_id)
) PRIMARY KEY(ticket_id);


CREATE OR REPLACE PROPERTY GRAPH access_network
NODE TABLES (
    access_node_temperatures
        LABEL access_node_temperature,
    access_nodes
        LABEL access_node,
    customer_devices
        LABEL customer_device,
    customers
        LABEL customer,
    port_performance,
    ports
        LABEL port,
    support_tickets
        LABEL support_ticket
)
EDGE TABLES (
    ports as port2
        source key(access_node_id) references access_nodes
        destination key(access_node_id, port_number) references ports
        label `contains`,
    port_performance as port_performance2
        source key(access_node_id, port_number) references ports
        destination key(access_node_id, port_number, timestamp) references port_performance
        label has_performance,
    access_node_temperatures as access_node_temperature2
        source key(access_node_id) references access_nodes
        destination key(access_node_id, timestamp) references access_node_temperatures
        label has_temperature,
    customer_devices as customer_device2
        source key(customer_id) references customers
        destination key(device_id) references customer_devices
        label owns,
    customer_devices as customer_device3
        source key(access_node_id, port_number) references ports
        destination key(device_id) references customer_devices
        label connected,
    support_tickets as support_ticket2
        source key(customer_id) references customers
        destination key(ticket_id) references support_tickets
        label opened,
    support_tickets as support_ticket3
        source key(ticket_id) references support_tickets
        destination key(device_id) references customer_devices
        label related_to
)
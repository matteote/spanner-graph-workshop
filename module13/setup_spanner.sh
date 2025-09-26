#!/bin/bash

set -e

if [ -z "$PROJECT_ID" ] || [ -z "$INSTANCE_ID" ] || [ -z "$DATABASE_ID" ]; then
    echo "Error: Please set the environment variables PROJECT_ID, INSTANCE_ID, and DATABASE_ID."
    exit 1
fi

echo "Checking if database '$DATABASE_ID' exists in instance '$INSTANCE_ID'..."

if gcloud spanner databases describe "$DATABASE_ID" --instance="$INSTANCE_ID" --project="$PROJECT_ID" &> /dev/null; then
    echo "Database '$DATABASE_ID' exists. Deleting it..."
    gcloud spanner databases delete "$DATABASE_ID" --instance="$INSTANCE_ID" --project="$PROJECT_ID" --quiet
    echo "Database '$DATABASE_ID' deleted."
fi

echo "Creating database '$DATABASE_ID' in instance '$INSTANCE_ID'..."
gcloud spanner databases create "$DATABASE_ID" --instance="$INSTANCE_ID" --project="$PROJECT_ID"
echo "Database '$DATABASE_ID' created."

echo "Applying schema from schema.sql to database '$DATABASE_ID'..."
gcloud spanner databases ddl update "$DATABASE_ID" --instance="$INSTANCE_ID" --project="$PROJECT_ID" --ddl-file=schema.sql
echo "Schema applied successfully."

echo "Spanner setup complete."

echo "Running data loader..."
uv run --with-requirements requirements.txt data_loader.py
echo "Data loader finished."
#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate


# Check applied migrations
echo "Listing applied migrations..."
python manage.py showmigrations



# Start the Django development server
echo "Starting server..."
exec "$@"

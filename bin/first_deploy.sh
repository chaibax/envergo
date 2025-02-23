#!/bin/bash
# This script is ran by scalingo upon creating new review apps

set -exv

echo ">>> Starting the first_deploy hook"

# Scalingo requires you to run this script to update postgres' version
dbclient-fetcher psql 14

# Let's seed the database
PG_OPTIONS="--clean --if-exists --no-owner --no-privileges --no-comments"
PG_EXCLUDE="-N information_schema -N ^pg_* --exclude-table=spatial_ref_sys --exclude-table-data geodata_zone "

# Note: dbclient-fetcher installs binary in $HOME/bin
$HOME/bin/pg_dump $PG_OPTIONS $PG_EXCLUDE --dbname $PARENT_DATABASE_URL --format c --file /tmp/dump.pgsql
$HOME/bin/pg_restore $PG_OPTIONS --dbname $DATABASE_URL /tmp/dump.pgsql
$HOME/bin/psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
# psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS unaccent;'

# Clean dump file
rm /tmp/dump.pgsql

# Warning! This hook replaces the `post_deploy` hook that we still want to run
bash $HOME/bin/post_deploy.sh
bash $HOME/bin/copy_polygons.sh

echo ">>> Leaving the first_deploy hook"

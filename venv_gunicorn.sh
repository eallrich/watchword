#!/bin/bash
# ============================================================================
# Utility script for starting gunicorn
# ------------------------------------
# This script is particularly useful as a command target in a Supervisor
# configuration. While Supervisor can handle activating a virtualenv, it's not
# very elegant. Here we can do everything we need to get gunicorn and django
# up and running.
# ============================================================================

SITE_ROOT=$(dirname $0)
SOCKET=$SITE_ROOT/sock/gunicorn
SOCKET_DIRECTORY=$(dirname $SOCKET)
WORKERS=3
WSGI=ww.wsgi

echo "Operating in $SITE_ROOT, socket will be at $SOCKET"

# Making sure the parent directories for the socket exist
test -d $SOCKET_DIRECTORY || mkdir -p $SOCKET_DIRECTORY

echo "Loading virtualenv"
source bin/activate

echo "Starting gunicorn"
# Using exec because the shell script doesn't need to keep running on its own
# after starting gunicorn.
exec gunicorn --workers $WORKERS --bind unix:$SOCKET $WSGI

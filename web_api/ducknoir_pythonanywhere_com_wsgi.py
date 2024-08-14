# This file contains the WSGI configuration required to serve up the
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

# The default location for this file on pythonanywhere is
# /var/www/ducknoir_pythonanywhere_com_wsgi.py
# I think it may be possible to move it, but it might require re-creating
# website. I'm just stashing it here for convenience. 

import sys

# Add path to the service application to sys.path
project_home = '/home/ducknoir/projects/synopsis-svc'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# import flask app but need to call it "application" for WSGI to work
from web_api.flask_app import app as application  # noqa

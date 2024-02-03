#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# update and upgrade
sudo apt-get update -y
sudo apt-get upgrade -y

# install nginx
sudo apt install nginx -y

# Create the folders /data/web_static/releases/test/
# and /data/web_static/shared/
# if any of them doesn’t already exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current
# linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists,
# it should be deleted and recreated every time the script is ran.
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group recursivly
sudo chown -R ubuntu: /data/

# Update the Nginx configuration to serve the content
# of /data/web_static/current/ to hbnb_static
serve_string="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n\n"

if ! grep -q "$serve_string" /etc/nginx/sites-enabled/*default;then
	sed -i "\@^\s*location / {@s@^@$serve_string@" /etc/nginx/sites-enabled/*default
fi

#  restart Nginx
service nginx start
service nginx restart

#!/bin/bash
rm -r store/html
rm -r store/sitemap.xml
curl -o store/sitemap.xml http://localhost/sitemap
docker-compose exec velvet python manage.py generatehtml
sudo chown -R "$USER:$USER" store/

#!/bin/bash
rm -r store/html
curl -o store/sitemap.xml http://localhost/sitemap
docker-compose exec velvet python manage.py generatehtml && sudo chown -R "$USER:$USER" store/
ssh polina 'rm -r ~/python/velvet/store/html'
scp -pr store/html        polina:~/python/velvet/store
scp -pr store/sitemap.xml polina:~/python/velvet/store

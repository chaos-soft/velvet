#!/bin/bash
curl -o store/sitemap.xml http://localhost/sitemap
docker-compose exec velvet python manage.py generatehtml && sudo chown -R $USER:$USER store/
ssh polina 'rm -r ~/python/velvet/store/html'
scp -pr ~/Documents/python/velvet/store/html polina:~/python/velvet/store

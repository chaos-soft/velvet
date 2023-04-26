#!/usr/bin/env python3
import requests


def main() -> None:
    r = requests.get('http://57st.net')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/html'

    r = requests.get('http://57st.net/api/articles?page=1')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/json'

    r = requests.get('http://57st.net/api/articles?page=100')
    assert r.status_code == 404
    assert r.headers['content-type'] == 'text/html'

    r = requests.get('http://57st.net/api/articles/57')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/json'

    r = requests.get('http://57st.net/api/articles/5700')
    assert r.status_code == 404
    assert r.headers['content-type'] == 'text/html'

    r = requests.get('http://57st.net/articles/57')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/html'

    r = requests.get('http://57st.net/robots.txt')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/plain'

    r = requests.get('http://57st.net/store/blog/2017/10/16/72850_screenshots_2013-05-06_00051.jpg')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'image/jpeg'

    r = requests.get('http://57st.net/store/sitemap.xml')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/xml'


if __name__ == '__main__':
    main()

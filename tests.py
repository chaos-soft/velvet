#!/usr/bin/env python3
import sys

import requests


def main() -> int:
    r = requests.get('http://57st.su', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/html; charset=utf-8'

    r = requests.get('http://57st.su/api/articles?page=1', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/json'

    r = requests.get('http://57st.su/api/articles?page=100', allow_redirects=False)
    assert r.status_code == 404
    assert r.headers['content-type'] == 'text/html; charset=utf-8'

    r = requests.get('http://57st.su/api/articles/57', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/json'

    r = requests.get('http://57st.su/api/articles/5700', allow_redirects=False)
    assert r.status_code == 404
    assert r.headers['content-type'] == 'text/html; charset=utf-8'

    r = requests.get('http://57st.su/articles/57', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/html; charset=utf-8'

    r = requests.get('http://57st.su/robots.txt', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/plain; charset=utf-8'

    r = requests.get(
        'http://57st.su/store/blog/2017/10/16/72850_screenshots_2013-05-06_00051.jpg',
        allow_redirects=False,
    )
    assert r.status_code == 200
    assert r.headers['content-type'] == 'image/jpeg'

    r = requests.get('http://57st.su/store/sitemap.xml', allow_redirects=False)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'text/xml; charset=utf-8'

    return 0


if __name__ == '__main__':
    sys.exit(main())

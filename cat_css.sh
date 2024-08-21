cat \
    store/css/reset.css \
    store/css/album.css \
    store/css/articles.css \
    store/css/rutube.css \
    store/css/slideshow.css \
    store/css/stream.css \
    store/css/style.css | \
        tr -s ' ' | tr -d '\n' > store/css/xxx.css

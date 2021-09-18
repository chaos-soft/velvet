'use strict'
/* global init, Item, Items */

class Article extends Item {
  constructor () {
    super()
    this.cover = document.getElementById('id_cover')
    this.img = `<img src="/store/thumbnails/{0}" title="{0}" data-index="{1}"
      style="max-height: 220px;" loading="lazy">`
  }

  clickImage (e) {
    if (e.ctrlKey) {
      // getAttribute для того, чтобы не был включен домен.
      this.cover.value = e.target.getAttribute('src')
    } else {
      super.clickImage(e)
    }
  }

  main () {
    super.main()
    const code = document.getElementById('id_code')
    const getYoutubeImage = document.getElementById('id_get_youtube_image')
    getYoutubeImage.addEventListener('click', () => {
      const id = code.value.split('\n').filter(Boolean)[0]
      this.cover.value = `https://img.youtube.com/vi/${id}/maxresdefault.jpg`
    })
  }
}

class Articles extends Items {
  constructor () {
    super()
    this.img = `<a href="{}">
      <img src="{}" style="max-height: 220px;" loading="lazy"></a>`
  }
}

init[0] = () => {
  const id = window.location.pathname.split('/')[5]
  if (id === 'change') {
    new Article().main()
  } else if (id === undefined) {
    new Articles().main()
  }
}

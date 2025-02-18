'use strict'

class Item {
  constructor () {
    this.imagesDelete = document.getElementById('id_images_delete')
    this.img = '<img src="/store/{0}" title="{0}" data-index="{1}" loading="lazy">'
  }

  clickImage (e) {
    const i = e.target.getAttribute('data-index')
    const indexes = new Set(this.imagesDelete.value.split(',').filter(Boolean))
    indexes.has(i) ? indexes.delete(i) : indexes.add(i)
    this.imagesDelete.value = Array.from(indexes).join(',')
    e.target.classList.toggle('selected')
  }

  main () {
    const html = ['<p>', '</p>']
    const images = document.getElementById('id_images')
    for (const [i, image] of images.value.split('\n').filter(Boolean).entries()) {
      html.splice(-1, 0, this.img.replaceAll('{0}', image).replace('{1}', i))
    }
    images.insertAdjacentHTML('afterend', html.join(''))
    for (const img of images.nextElementSibling.getElementsByTagName('img')) {
      img.addEventListener('click', (e) => this.clickImage(e))
    }
  }
}

class Items {
  constructor () {
    this.img = `<a href="/store/{}">
      <img src="/store/{}" style="max-width: 512px;" loading="lazy"></a>`
  }

  main () {
    let images = document.getElementsByClassName('field-get_cover')
    if (!images.length) {
      images = document.getElementsByClassName('field-images')
    }
    for (const td of images) {
      const html = []
      if (td.childNodes[0].textContent !== '-') {
        for (const image of td.childNodes[0].textContent.split('\n').filter(Boolean)) {
          html.push(this.img.replaceAll('{}', image))
        }
      }
      td.innerHTML = html.join('<br>')
    }
  }
}

const main = [
  () => {
    const id = window.location.pathname.split('/')[5]
    if (id === 'change') {
      new Item().main()
    } else if (id === undefined) {
      new Items().main()
    }
  }
]
document.addEventListener('DOMContentLoaded', () => {
  for (const v of main) {
    v()
  }
})

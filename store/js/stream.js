'use strict'

class Panel {
  constructor () {
    this.chat = document.getElementById('chat')
    const controls = document.getElementsByClassName('controls')[0]
    this.controls = controls.getElementsByTagName('a')
    this.fullscreen = document.getElementById('fullscreen')
    this.iframe = document.getElementsByClassName('iframe')[0]
    this.stream = document.getElementsByClassName('stream')[0]
    this.chats = this.stream.children[1]
  }

  hide () {
    this.chat.classList.add('active')
    this.fullscreen.classList.add('active')
    this.stream.classList.add('hidden')
  }

  initControls () {
    let isClick = true
    for (const a of this.controls) {
      a.addEventListener('click', (e) => {
        if (a.classList.contains('chat')) {
          if (a.classList.contains('active')) {
            this.chats.querySelector(`.${a.text}`).remove()
          } else {
            const iframe = `<iframe class="${a.text}" src="${a.href}"></iframe>`
            this.chats.insertAdjacentHTML('beforeend', iframe)
          }
          a.classList.toggle('active')
        } else if (a.classList.contains('image')) {
          this.iframe.children[0].src = 'about:blank'
          this.iframe.style.backgroundImage = `url(${a.href})`
        } else if (a.classList.contains('miranda')) {
          if (a.classList.contains('active')) {
            this.iframe.children[1].src = 'about:blank'
          } else {
            this.iframe.children[1].src = a.href
          }
          a.classList.toggle('active')
        } else if (a.classList.contains('player')) {
          this.iframe.children[0].src = a.href
        }
        e.preventDefault()
      })
      if (isClick) {
        a.click()
        isClick = false
      }
    }
  }

  main () {
    this.chat.addEventListener('click', () => {
      this.chat.classList.toggle('active')
      this.stream.classList.toggle('hidden')
    })
    this.fullscreen.addEventListener('click', () => toggleFullscreen(this.iframe))
    this.initControls()
  }

  show () {
    this.chat.classList.remove('active')
    this.fullscreen.classList.remove('active')
    this.stream.classList.remove('hidden')
  }
}

let panel

function init () {
  panel = new Panel()
  panel.main()
}

function toggleFullscreen (element) {
  if (!document.fullscreenElement) {
    element.requestFullscreen()
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
    }
  }
}

document.addEventListener('DOMContentLoaded', () => init())
document.addEventListener('fullscreenchange', () => {
  !document.fullscreenElement ? panel.show() : panel.hide()
})
document.addEventListener('keyup', (e) => {
  if (e.code === 'KeyF') {
    toggleFullscreen(panel.iframe)
  }
})

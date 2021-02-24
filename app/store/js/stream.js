'use strict'

class Panel {
  constructor () {
    this.chat = document.getElementById('chat')
    this.fullscreen = document.getElementById('fullscreen')
    this.iframe = document.getElementsByClassName('iframe')[0]
    this.stream = document.getElementsByClassName('stream')[0]
  }

  hide () {
    this.chat.classList.add('active')
    this.fullscreen.classList.add('active')
    this.stream.classList.add('hidden')
  }

  main () {
    this.chat.addEventListener('click', () => {
      this.chat.classList.toggle('active')
      this.stream.classList.toggle('hidden')
    })
    this.fullscreen.addEventListener('click', () => toggleFullscreen(this.iframe))
  }

  show () {
    this.chat.classList.remove('active')
    this.fullscreen.classList.remove('active')
    this.stream.classList.remove('hidden')
  }
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

let panel

function init () {
  panel = new Panel()
  panel.main()
  const controls = document.getElementsByClassName('controls')[0]
  const players = controls.getElementsByTagName('a')
  let isClick = true
  for (const a of players) {
    a.addEventListener('click', (e) => {
      panel.iframe.children[0].src = a.href
      e.preventDefault()
    })
    if (isClick) {
      a.click()
      isClick = false
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

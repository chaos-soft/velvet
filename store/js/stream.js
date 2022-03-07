'use strict'

class Stream {
  constructor () {
    this.chat = document.getElementById('chat')
    this.chats = document.getElementsByClassName('chats')[0]
    this.fullscreen = document.getElementById('fullscreen')
    this.panel = document.getElementsByClassName('panel')[0]
    this.controls = this.panel.querySelectorAll('.controls > a')
    this.stream = document.getElementsByClassName('stream')[0]
  }

  hide () {
    this.chat.classList.add('active')
    this.fullscreen.classList.add('active')
    this.panel.classList.add('hidden')
  }

  initControls () {
    const elements = { chat: this.chats, player: this.stream }
    let isClick = true
    for (const a of this.controls) {
      a.addEventListener('click', (e) => {
        if (a.classList.contains('chat') || a.classList.contains('player')) {
          const element = a.classList.contains('chat') ? elements.chat : elements.player
          if (a.classList.contains('active')) {
            element.querySelector(`.${a.text}`).remove()
          } else {
            const iframe = `<iframe class="${a.text}" src="${a.href}"></iframe>`
            element.insertAdjacentHTML('beforeend', iframe)
          }
          a.classList.toggle('active')
        } else if (a.classList.contains('image')) {
          this.stream.style.backgroundImage = `url(${a.href})`
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
      this.panel.classList.toggle('hidden')
    })
    this.fullscreen.addEventListener('click', () => toggleFullscreen(this.stream))
    this.initControls()
    this.resize()
  }

  show () {
    this.chat.classList.remove('active')
    this.fullscreen.classList.remove('active')
    this.panel.classList.remove('hidden')
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

let stream

document.addEventListener('DOMContentLoaded', () => {
  stream = new Stream()
  stream.main()
})
document.addEventListener('fullscreenchange', () => {
  !document.fullscreenElement ? stream.show() : stream.hide()
})
document.addEventListener('keyup', (e) => {
  if (e.code === 'KeyF') {
    toggleFullscreen(stream.stream)
  }
})
window.addEventListener('resize', () => stream.resize())

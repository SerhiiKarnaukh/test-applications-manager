// Node Modules
import 'core-js/stable'

import AOS from 'aos/dist/aos' // include css in scss 'aos/dist/aos.css'
import './index.scss'

// Components

// Layouts
import FrontPage from '../front-page/front-page'

$(document).ready(function () {
  FrontPage()

  var spinner = function () {
    setTimeout(function () {
      if ($('#spinner').length > 0) {
        $('#spinner').removeClass('show')
      }
    }, 1)
  }
  spinner()

  AOS.init({
    duration: 1000,
    easing: 'ease-out-sine',
  })
})

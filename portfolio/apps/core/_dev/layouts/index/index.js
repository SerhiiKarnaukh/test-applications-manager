// Node Modules
import 'core-js/stable'

import AOS from 'aos/dist/aos' // include css in scss 'aos/dist/aos.css'
import './index.scss'

// Components
// import '../../components/button.scss'

// Layouts
// import Store from '../store/store'
// import Contact from '../contact/contact'
// import ProductDetail from '../product-detail/product-detail'
// import Cart from '../cart/cart'
// import Checkout from '../checkout/checkout'
// import Payments from '../payments/payments'
// import Dashboard from '../dashboard/dashboard'

$(document).ready(function () {
  //   Store()
  //   Contact()
  //   ProductDetail()
  //   Cart()
  //   Checkout()
  //   Payments()
  //   Dashboard()
  var spinner = function () {
    setTimeout(function () {
      if ($('#spinner').length > 0) {
        $('#spinner').removeClass('show')
      }
    }, 1)
  }
  spinner()
  //   $(window).scroll(function () {
  //     if ($(this).scrollTop() > 100) {
  //       $('.back-to-top').fadeIn('slow')
  //     } else {
  //       $('.back-to-top').fadeOut('slow')
  //     }
  //   })
  //   $('.back-to-top').click(function () {
  //     $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo')
  //     return false
  //   })

  AOS.init({
    duration: 1000,
    easing: 'ease-out-sine',
  })
})

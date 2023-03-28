// Node Modules
import '@babel/polyfill';

import AOS from 'aos/dist/aos'; // include css in scss 'aos/dist/aos.css'
import './index.scss';

// Components
import '../../components/button.scss';

// Layouts
import Store from '../store/store';
import Contact from '../contact/contact';
import ProductDetail from '../product-detail/product-detail';
import Cart from '../cart/cart';

$(document).ready(function () {
    Store()
    Contact()
    ProductDetail()
    Cart()

    AOS.init({
        duration: 1000,
        easing: 'ease-out-sine'
    });
});

// Node Modules
import '@babel/polyfill';

import "bootstrap";
import AOS from 'aos/dist/aos'; // include css in scss 'aos/dist/aos.css'
import Swiper, {Navigation, Pagination, EffectCoverflow, Keyboard, Autoplay} from 'swiper';
import 'swiper/css';

window.Swiper = Swiper;


import './index.scss';


// Components
import '../../components/button.scss';

// Modules
import Header from '../header/header';
import FrontPage from '../../layouts/front-page/front-page';
import Footer from '../footer/footer';
import SingleProduct from '../single-product/single-product';

$(document).ready(function () {
    Swiper.use([Navigation, Pagination, EffectCoverflow, Keyboard, Autoplay]);
    Header();
    FrontPage();
    Footer();
    SingleProduct();
    AOS.init({
        duration: 1000,
        easing: 'ease-out-sine'
    });
});

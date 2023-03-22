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


// For removing google recaptcha empty div (bug with fixed height),
// and Wordpress clear: both div
function removeUselessLayers() {
    $('body>div').each(function () {
        if (
            (
                (
                    $(this).css('position') === 'absolute' &&
                    $(this).css('z-index') === '-10000' &&
                    parseInt($(this).css('top')) === 0 &&
                    parseInt($(this).css('left')) === 0 &&
                    parseInt($(this).css('right')) === 0
                ) ||
                $(this).css('clear') === 'both'
            ) &&
            !$(this).html()
        ) {
            $(this).remove();
        }
    });
}

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
    setTimeout(function () {
        removeUselessLayers();
    }, 1000);
});

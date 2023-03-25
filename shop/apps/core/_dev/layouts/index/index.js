// Node Modules
import '@babel/polyfill';


import AOS from 'aos/dist/aos'; // include css in scss 'aos/dist/aos.css'
import 'swiper/css';
import './index.scss';

// Components
import '../../components/button.scss';

// Modules
import Header from '../header/header';
import FrontPage from '../../layouts/front-page/front-page';
import Footer from '../footer/footer';
import SingleProduct from '../single-product/single-product';

$(document).ready(function () {
    // Header();
    // FrontPage();
    // Footer();
    // SingleProduct();
    AOS.init({
        duration: 1000,
        easing: 'ease-out-sine'
    });
});

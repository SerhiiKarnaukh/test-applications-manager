import Swiper, {Navigation, Pagination, EffectCoverflow, Keyboard, Autoplay} from 'swiper';

window.Swiper = Swiper;

$(document).ready(function () {
    Swiper.use([Navigation, Pagination, EffectCoverflow, Keyboard, Autoplay]);
});

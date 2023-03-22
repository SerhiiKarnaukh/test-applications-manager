import './shophair-banner.scss';

function init() {
    new Swiper('.shop-hair-swiper', {
        autoplay: {
            delay: 3000,
        },
        slidesPerView: 1,
        loop: true,
        grabCursor: true,
    })
}

export default init;
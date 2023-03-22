import './feedback.scss';

function init() {
    let feedbackSlider = new Swiper('.feedback-swiper', {
        autoplay: {
            delay: 3000,
        },
        slidesPerView: 1,
        loop: true,
        grabCursor:true
    })
}

export default init;
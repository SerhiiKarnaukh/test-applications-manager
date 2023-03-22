import './bottom-menu.scss';

function init() {
    $(window).resize(function () {
        if ($(window).width() < 992) {
            $("#secondary-menu").children().addClass('mobile-bottom-item').appendTo("#primary-menu");
        } else if ($(window).width() > 992) {
            $("#primary-menu .mobile-bottom-item").appendTo("#secondary-menu");
        }
    });
    if ($(window).width() < 992) {
        $("#secondary-menu").children().addClass('mobile-bottom-item').appendTo("#primary-menu");
    }
}

export default init;



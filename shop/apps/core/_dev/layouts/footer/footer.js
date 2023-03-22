import './footer.scss';
import Copyright from './modules/copyright/copyright'
import FooterNav from './modules/footer-nav/footer-nav'
import Subscription from './modules/subscription/subscription'
import Social from './modules/social/social'

function init() {
    Copyright();
    FooterNav();
    Subscription();
    Social();
}


export default init;
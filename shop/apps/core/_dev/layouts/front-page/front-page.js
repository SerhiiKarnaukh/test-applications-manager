import './front-page.scss';
import Discount from './modules/discount/discount'
import Intro from './modules/intro/intro'
import Texture from './modules/texture/texture'
import Features from './modules/features/features'
import ShopHairBanner from './modules/shophair-banner/shophair-banner'
import Platform from './modules/platform/platform'
import Feedback from './modules/feedback/feedback'


function init() {
   Discount();
   Intro();
   Texture();
   Features();
   ShopHairBanner();
   Platform();
   Feedback();
}

export default init;
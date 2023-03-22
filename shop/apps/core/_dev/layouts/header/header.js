import './header.scss';
import './modules/top-menu/top-menu.scss'
import Search from './modules/search/search'
import Navbar from './modules/navbar/navbar'
import Cart from './modules/cart/cart'
import CartModal from './modules/cart-modal/cart-modal'
import BottomMenu from './modules/bottom-menu/bottom-menu'
import Breadcrumbs from './modules/breadcrumbs/breadcrumbs'


function init() {
    Search();
    Navbar();
    Cart();
    CartModal();
    BottomMenu();
    Breadcrumbs();
}

export default init;
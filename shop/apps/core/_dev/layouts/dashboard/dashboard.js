import './dashboard.scss'
import DashboardSidebar from './modules/dashboard-sidebar/dashboard-sidebar'
import ChangePassword from './modules/change-password/change-password'
import EditProfile from './modules/edit-profile/edit-profile'
import MyOrders from './modules/my-orders/my-orders'

function init() {
  DashboardSidebar()
  ChangePassword()
  EditProfile()
  MyOrders()
}

export default init

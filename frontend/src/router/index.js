import { createRouter, createWebHistory } from "vue-router"

import Login from "../components/Login.vue"
import AdminDashboard from "../components/AdminDashboard.vue"
import DoctorDashboard from "../components/DoctorDashboard.vue"
import PatientDashboard from "../components/PatientDashboard.vue"
import RegisterPatient from "../components/Register.vue"
import EditProfile from "../components/EditProfile.vue"

const routes = [
  { path: "/", component: Login},
  { path: "/register", component: RegisterPatient},
  { path: "/admin", component: AdminDashboard},
  { path: "/doctor", component: DoctorDashboard},
  { path: "/patient", component: PatientDashboard},
  { path: "/edit-profile", component:EditProfile},
  {path: "/update-doctor/:id", component: () => import("../components/UpdateDoctor.vue")},
  {path: "/admin/appointments", component: () => import("../components/AdminAppointments.vue")}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("token")

  if (!token && to.path !== "/" && to.path !== "/register") {
    next("/")
  } else {
    next()
  }

})

export default router
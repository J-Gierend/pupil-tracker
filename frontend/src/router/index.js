import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ClassView from '../views/ClassView.vue'
import PupilView from '../views/PupilView.vue'
import ReportGenerator from '../views/ReportGenerator.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/class/:id',
    name: 'ClassView',
    component: ClassView,
    props: true
  },
  {
    path: '/pupil/:id',
    name: 'PupilView',
    component: PupilView,
    props: true
  },
  {
    path: '/reports',
    name: 'ReportGenerator',
    component: ReportGenerator
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

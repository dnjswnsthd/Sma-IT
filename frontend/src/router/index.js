import Vue from "vue";
import VueRouter from "vue-router";
import Cam from "../views/Cam.vue";
import CustomerHeader from "../components/common/CustomerHeader";
import AdminHeader from "../components/common/AdminHeader";
import AdminMain from "../views/AdminMain";

import CustomerRegister from "../views/CustomerRegister";
import CustomerModify from "../views/CustomerModify";

import CamPayment from "../views/CamPayment";
import CamSatisfied from "../views/CamSatisfied";

Vue.use(VueRouter);

const routes = [
  {
    // 메인화면으로 이동
    path: '/',
    name: 'Cam',
    components: { default: Cam, header: CustomerHeader },
  },
  
  {
    // 관리자페이지 이동
    path: '/adminMain',
    name: 'AdminMain',
    components: { default: AdminMain, header: AdminHeader },
  },
  {
    // 고객등록페이지 이동
    path: '/customerRegister',
    name: 'CustomerRegister',
    components: { default: CustomerRegister, header: AdminHeader },
  },
  {
    // 고객정보수정페이지 이동
    path: '/customerModify',
    name: 'CustomerModify',
    components: { default: CustomerModify, header: AdminHeader },
  },
  {
    // 결제페이지 이동
    path: '/camPayment',
    name: 'CamPayment',
    components: { default: CamPayment, header: AdminHeader },
  },
  {
    // 만족도페이지 이동
    path: '/camSatisfied',
    name: 'CamSatisfied',
    components: { default: CamSatisfied, header: AdminHeader },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;

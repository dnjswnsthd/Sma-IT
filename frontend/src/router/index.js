import Vue from "vue";
import VueRouter from "vue-router";
import Cam from "../views/Cam.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Cam",
    component: Cam
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;

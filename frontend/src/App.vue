<template>
  <v-app style="background-color: rgb(25, 37, 55)">
    <customer-header></customer-header>
    <router-view></router-view>
  </v-app>
</template>

<script>
import CustomerHeader from "./components/common/Customer_Header";

export default {
  name: "App",

  components: {
    CustomerHeader,
  },
};
</script>

<style>
* {
  font-family: "MapoFlowerIsland";
}
@font-face {
  font-family: "MapoFlowerIsland";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/MapoFlowerIslandA.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
</style>


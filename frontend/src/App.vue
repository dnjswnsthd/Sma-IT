<template>
    <v-app>
        <router-view name="header"></router-view>
        <router-view></router-view>
    </v-app>
</template>

<script>


export default {
    name: 'App',
};
</script>

<style>
@import './assets/css/reset.css';
</style>

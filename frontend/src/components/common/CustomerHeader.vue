<template>
    <header>
        <v-row>
            <div class="logoBox" @click="goMain">
                <img src="@/assets/images/logo.png" alt="Logo" class="logoImg"/>
            </div>
        </v-row>
    </header>
</template>

<script>
export default {
    data() {
        return {};
    },
    methods: {
        goMain() {
            this.$router.push({ name: 'AdminMain' });
        },
    },
};
</script>

<style scoped>
@import '../../assets/css/header.css';
</style>